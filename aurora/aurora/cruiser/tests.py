from django.test import TestCase
from lib.fabfile_parser import get_source


class FabFileParsing(TestCase):
    def test_import(self):
        code = """import fabfile
from fabric.api import run, local"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("import fabfile\nfrom fabric.api import run, local", [])
        self.assertEqual(expected, actual)

    def test_def(self):
        code = """def test(n1, n2):
    return n1 + n2"""
        lines = code.split("\n")
        actual = get_source(lines)
        expected = ("", [{'body': "def test(n1, n2):    return n1 + n2", 'name': "test"}])
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
