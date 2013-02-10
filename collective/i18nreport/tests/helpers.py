import os


TEST_EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'example')


def make_absolute(path):
    return os.path.join(TEST_EXAMPLE_PATH, path)


def make_relative(path):
    start = TEST_EXAMPLE_PATH + '/'

    if path.startswith(start):
        return path[len(start):]

    else:
        return path


def make_relative_recursively(data):
    if isinstance(data, (unicode, str)):
        return make_relative(data)

    elif isinstance(data, dict):
        new = {}

        for key, value in data.items():
            new[make_relative_recursively(key)] = make_relative_recursively(value)

        return new

    if isinstance(data, list):
        new = [make_relative_recursively(item) for item in data]
        return list(sorted(new))

    elif data is None or isinstance(data, int):
        return data

    else:
        raise ValueError('Unexpected data type %s (%s)' % (type(data), str(data)))
