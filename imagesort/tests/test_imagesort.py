import pytest
import py
import os
from imagesort import imagesort
import filecmp


@pytest.fixture
def datadir(tmpdir):
    return py.path.local().join('imagesort', 'tests', 'testdata')


@pytest.fixture
def inputdir(datadir, tmpdir):
    indir = tmpdir.join('input')
    indir.ensure(dir=True)
    for p in datadir.visit():
        p.copy(indir.join(p.basename))
    return indir


@pytest.fixture
def outputdir(tmpdir):
    outdir = tmpdir.join('output')
    outdir.ensure(dir=True)
    return outdir


def touch(path):
    """Create empty file."""
    with open(path, 'a'):
        os.utime(path, None)


def filecount(d):
    n = 0
    for root, subdir, files in os.walk(d):
        n += len(files)
    return n


def test_should_not_work_with_nondirs(tmpdir, operation):
    nodir = tmpdir.join('none')
    with pytest.raises(IOError):
        imagesort.process_images(str(nodir), str(tmpdir), operation)


def test_outputdir_created_if_not_present(tmpdir, operation):
    src = tmpdir.join('src')
    dest = tmpdir.join('dest')
    src.ensure(dir=True)
    imagesort.process_images(str(src), str(dest), operation)
    assert dest.check(dir=1)


def test_should_not_work_with_subdirs(tmpdir, operation):
    subdir = tmpdir.join('sub')
    subdir.ensure(dir=True)
    with pytest.raises(imagesort.SubdirError):
        imagesort.process_images(str(tmpdir), str(subdir), operation)
    with pytest.raises(imagesort.SubdirError):
        imagesort.process_images(str(subdir), str(tmpdir), operation)


def test_dryrun(inputdir, outputdir, operation):
    imagesort.process_images(str(inputdir), str(outputdir),
                             operation, dry_run=True)
    assert len(outputdir.listdir()) == 0


def test_we_have_correct_filenumber(inputdir, outputdir, operation):
    imagesort.process_images(str(inputdir), str(outputdir), operation)
    assert filecount(str(outputdir)) == 6


def test_files_are_placed_correctly(datadir, inputdir, outputdir, operation):
    imagesort.process_images(str(inputdir), str(outputdir),
                             operation, dry_run=False)

    def verify(*path):
        result = outputdir.join(*path)
        testdata = datadir.join(path[-1])
        assert result.check()
        assert filecmp.cmp(str(result), str(testdata), shallow=False)

    verify('2014', '2014_04_13', '1.jpg')
    verify('2014', '2014_03_22', '2.jpg')
    verify('2014', '2014_04_13', '1.tiff')
    verify('2014', '2014_03_22', '2.tiff')

    unknown_path1 = outputdir.join('unknown', 'invalid.jpg')
    assert unknown_path1.check()

    unknown_path2 = outputdir.join('unknown', 'invalid.tiff')
    assert unknown_path2.check()


def test_move_operation_works(inputdir, outputdir, operation):
    imagesort.process_images(str(inputdir), str(outputdir),
                             operation, dry_run=False)

    n = len(inputdir.listdir())
    if operation.desc == 'Moving':
        assert n == 0
    else:
        assert n > 0


def test_hardlink_operation_works(inputdir, outputdir, operation):
    imagesort.process_images(str(inputdir), str(outputdir),
                             operation, dry_run=False)

    for root, _, files in os.walk(str(outputdir)):
        for f in files:
            n = os.stat(os.path.join(root, f)).st_nlink
            if operation.desc == 'Hardlinking':
                assert n > 1
            else:
                assert n == 1


def test_handle_existing_path_with_different_content(inputdir, outputdir,
                                                     operation):
    olddir = outputdir.join('2014', '2014_03_22')
    oldpath = olddir.join('2.jpg')
    os.makedirs(str(olddir))
    touch(str(oldpath))

    imagesort.process_images(str(inputdir), str(outputdir),
                             operation, dry_run=False)

    path = outputdir.join('2014', '2014_03_22', '2-1.jpg')
    assert os.path.exists(str(path))

    imagesort.process_images(str(inputdir), str(outputdir),
                             operation, dry_run=False)

    # Should recognize existing file
    path = outputdir.join('2014', '2014_03_22', '2-2.jpg')
    assert not os.path.exists(str(path))

    assert filecount(str(outputdir)) == 7
