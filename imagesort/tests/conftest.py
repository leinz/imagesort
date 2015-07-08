from imagesort import imagesort


def pytest_generate_tests(metafunc):
    if 'operation' in metafunc.funcargnames:
        metafunc.parametrize(
            'operation',
            (op for op in imagesort.OPERATIONS.values()))
