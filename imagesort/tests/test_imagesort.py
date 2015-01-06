import pytest
import py
import os
from imagesort import imagesort
import filecmp


@pytest.fixture
def testdir():
    return py.path.local().join('imagesort', 'tests', 'testdata')


def touch(path):
    """Create empty file."""
    with open(path, 'a'):
        os.utime(path, None)


def filecount(d):
    n = 0
    for root, subdir, files in os.walk(d):
        n += len(files)
    return n


def test_should_not_work_with_nondirs(tmpdir):
    nodir = tmpdir.join('none')
    with pytest.raises(IOError):
        imagesort.process_dir(str(nodir), str(tmpdir))


def test_should_not_work_with_subdirs(tmpdir):
    subdir = tmpdir.join('sub')
    subdir.ensure(dir=True)
    with pytest.raises(imagesort.SubdirError):
        imagesort.process_dir(str(tmpdir), str(subdir))
    with pytest.raises(imagesort.SubdirError):
        imagesort.process_dir(str(subdir), str(tmpdir))


def test_dryrun(tmpdir, testdir):
    imagesort.process_dir(str(testdir), str(tmpdir), dry_run=True)
    assert len(tmpdir.listdir()) == 0


def test_we_have_correct_filenumber(tmpdir, testdir):
    imagesort.process_dir(str(testdir), str(tmpdir))
    assert filecount(str(tmpdir)) == 3


def test_files_are_placed_correctly(tmpdir, testdir):
    imagesort.process_dir(str(testdir), str(tmpdir), dry_run=False)

    path1 = tmpdir.join('2014', '2014_04_13', '1.jpg')
    assert path1.check()
    testdata1 = testdir.join('1.jpg')
    assert filecmp.cmp(str(path1), str(testdata1), shallow=False)

    path2 = tmpdir.join('2014', '2014_03_22', '2.jpg')
    assert path2.check()
    testdata2 = testdir.join('2.jpg')
    assert filecmp.cmp(str(path2), str(testdata2), shallow=False)

    unknown_path = tmpdir.join('unknown', 'invalid.jpg')
    assert unknown_path.check()


def test_handle_existing_path_with_different_content(tmpdir, testdir):
    olddir = tmpdir.join('2014', '2014_03_22')
    oldpath = olddir.join('2.jpg')
    os.makedirs(str(olddir))
    touch(str(oldpath))

    imagesort.process_dir(str(testdir), str(tmpdir), dry_run=False)

    path = tmpdir.join('2014', '2014_03_22', '2-1.jpg')
    assert os.path.exists(str(path))

    imagesort.process_dir(str(testdir), str(tmpdir), dry_run=False)

    # Should recognize existing file
    path = tmpdir.join('2014', '2014_03_22', '2-2.jpg')
    assert not os.path.exists(str(path))

    assert filecount(str(tmpdir)) == 4