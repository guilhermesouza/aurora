from django.test import TestCase
from virtualenv import expected_exe
from lib.fabfile_parser import get_source


class FabFileParsing(TestCase):
    def test_import(self):
        code = """import fabfile
from fabric.api import run, local"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = "import fabfile\nfrom fabric.api import run, local"
        self.assertEqual(expected, actual[0])

    def test_def(self):
        code = """def test(n1, n2):
    return n1 + n2"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("", [{'body': "def test(n1, n2):    return n1 + n2", 'name': "test"}])
        self.assertEqual(expected, actual)

    def test_def_with_decorator(self):
        code = """@local('asd')
def test(n1, n2):
    return n1 + n2"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("", [{'body': "@local('asd')def test(n1, n2):    return n1 + n2", 'name': "test"}])
        self.assertEqual(expected, actual)


    def test_def_with_two_decorators(self):
        code = """@local('asd')
@run('ad')
def test(n1, n2):
    return n1 + n2"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("", [{'body': "@local('asd')@run('ad')def test(n1, n2):    return n1 + n2", 'name': "test"}])
        self.assertEqual(expected, actual)

    def test_def_and_import(self):
        code = """from fabric.api import local
def test(n1, n2):
    local('echo test')
    return n1 + n2"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("from fabric.api import local", [{'body': "def test(n1, n2):    local('echo test')    return n1 + n2", 'name': "test"}])
        self.assertEqual(expected, actual)

    def test_with_noise_code(self):
        code = """from fabric.api import local
def test(n1, n2):
    local('echo test')
    return n1 + n2

x = 5
print x"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("from fabric.api import local", [{'body': "def test(n1, n2):    local('echo test')    return n1 + n2", 'name': "test"}])
        self.assertEqual(expected, actual)

    def test_with_empty_code(self):
        code = """"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("", [])
        self.assertEqual(expected, actual)

    def test_with_two_functions_and_noise(self):
        code = """from fabric.api import local, run
def test(n1, n2):
    local('echo test')
    return n1 + n2

x = 5
print x

def test2(arg):
    run('uname -a')
    return arg

for i in code:
    print i

class lol():
    self.init = 'asda'"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("from fabric.api import local, run", [{'body': "def test(n1, n2):    local('echo test')    return n1 + n2", 'name': "test"}, {'body': "def test2(arg):    run('uname -a')    return arg", 'name': "test2"}])
        self.assertEqual(expected, actual)