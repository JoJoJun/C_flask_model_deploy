import unittest

test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*test*.py')

if __name__ == '__main__':
    with open('UnittestTextReport.txt', 'a') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(discover)
