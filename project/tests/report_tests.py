import unittest
import project
from project.tests.HTMLTestRunner import HTMLTestRunner
app = project.create_app()
test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*test*.py')

if __name__ == '__main__':
    with open('HtmlReport.html', 'wb') as f:
        runner = HTMLTestRunner(stream=f, title='test report', description='', verbosity=2)
        runner.run(discover)
