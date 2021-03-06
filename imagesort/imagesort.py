import sys
import exifread
import os
from datetime import datetime
import shutil
import filecmp
import logging

logger = logging.getLogger(__name__)


class Operation(object):
    def __init__(self, func, desc):
        self.func = func
        self.desc = desc


def _valid_operations():
    ops = dict(
        copy=Operation(shutil.copy, 'Copying'),
        move=Operation(shutil.move, 'Moving'),
    )

    if hasattr(os, 'link'):
        ops['hardlink'] = Operation(os.link, 'Hardlinking')

    return ops


OPERATIONS = _valid_operations()


def process_images(inputdir, outputdir, operation, dry_run=False):
    _validate_directories(inputdir, outputdir)

    # Create destination directory if not present
    if not os.path.isdir(outputdir):
        os.makedirs(outputdir)

    for imagepath in _get_images(inputdir):
        destdir = os.path.join(outputdir,
                               _get_destdir(imagepath))

        if not os.path.isdir(destdir):
            logger.info("Creating directory %s", destdir)
            _execute(dry_run, os.makedirs, destdir)

        destpath = _get_valid_destpath(imagepath, destdir)
        if destpath:
            logger.info("%s %s to %s", operation.desc, imagepath, destpath)
            try:
                _execute(dry_run, operation.func, imagepath, destpath)
            except OSError:
                logger.exception('Could not perform operation.')
                sys.exit(1)


def _get_images(path):
    for root, _, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg', '.tiff'):
                yield os.path.join(root, f)


def _validate_directories(src, dest):
    if not os.path.isdir(src):
        raise IOError('{} is not a directory.'.format(src))
    if _is_subdir(src, dest):
        raise SubdirError("{0} is subdirectory of {1}".format(src, dest))
    if _is_subdir(dest, src):
        raise SubdirError("{0} is subdirectory of {1}".format(dest, src))


def _execute(dry_run, func, *args):
    if not dry_run:
        func(*args)


def _is_subdir(dir1, dir2):
    """Check if p1 is subdir of p2."""
    r1 = os.path.realpath(dir1)
    r2 = os.path.realpath(dir2)
    if r1.startswith(r2):
        return True
    return False


def _get_valid_destpath(srcpath, destdir):
    p = os.path.join(destdir, os.path.basename(srcpath))
    n = 1
    while os.path.exists(p):
        if filecmp.cmp(srcpath, p, shallow=False):
            logger.info("Ignoring identical files: %s %s",
                        srcpath, p)
            p = None
            break
        base, ext = os.path.splitext(p)
        base = "{0}-{1}".format(base, n)
        p = ''.join([base, ext])
        n += 1
    return p


def _get_destdir(image_path):
    TAG = 'EXIF DateTimeOriginal'
    with open(image_path, 'rb') as image:
        tags = exifread.process_file(
            image,
            stop_tag=TAG,
            details=False)
        try:
            d = _date_path(datetime.strptime(str(tags[TAG]),
                                             "%Y:%m:%d %H:%M:%S"))
        except (KeyError, ValueError):
            d = 'unknown'

    return d


def _date_path(date):
    return os.path.join(
        str(date.year),
        "{0}_{1:02d}_{2:02d}".format(date.year, date.month, date.day))


class SubdirError(Exception):
    pass


def main():
    logging.basicConfig(level=logging.INFO)

    import argparse
    parser = argparse.ArgumentParser(
        description='Organize image files by date taken.')
    parser.add_argument('operation', choices=[name for name in OPERATIONS],
                        help='file operation')
    parser.add_argument('inputdir', type=str, help='input directory')
    parser.add_argument('outputdir', type=str, help='output directory')
    parser.add_argument('--dry-run', action='store_true',
                        help="log actions without writing anything to disk")
    args = parser.parse_args()

    op = OPERATIONS[args.operation]

    process_images(args.inputdir, args.outputdir, op, dry_run=args.dry_run)
