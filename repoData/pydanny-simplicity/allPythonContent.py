__FILENAME__ = simplicity
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Greenfeld'
__version__ = "0.6.4"

import json
import string
import sys

# Python 3 compatibility
P3K = sys.version > '3'
STRING_TYPE = str if P3K else unicode
DIVIDERS = ['~', '=', '-', '+', '_']


def file_opener(filename):
    """ I'm basically a context manager for opening files! """
    with open(filename) as f:
        text = f.read()
    return text


def text_cleanup(data, key, last_type):
    """ I strip extra whitespace off multi-line strings if they are ready to be stripped!"""
    if key in data and last_type == STRING_TYPE:
        data[key] = data[key].strip()
    return data


def rst_to_json(text):
    """ I convert Restructured Text with field lists into Dictionaries!

        TODO: Convert to text node approach.
    """
    records = []
    last_type = None
    key = None
    data = {}
    directive = False

    lines = text.splitlines()
    for index, line in enumerate(lines):

        # check for directives
        if len(line) and line.strip().startswith(".."):
            directive = True
            continue

        # set the title
        if len(line) and (line[0] in string.ascii_letters or line[0].isdigit()):
            directive = False
            try:
                if lines[index + 1][0] not in DIVIDERS:
                    continue
            except IndexError:
                continue
            data = text_cleanup(data, key, last_type)
            data = {"title": line.strip()}
            records.append(
                data
            )
            continue

        # Grab standard fields (int, string, float)
        if len(line) and line[0].startswith(":"):
            data = text_cleanup(data, key, last_type)
            index = line.index(":", 1)
            key = line[1:index]
            value = line[index + 1:].strip()
            data[key], last_type = type_converter(value)
            directive = False
            continue

        # Work on multi-line strings
        if len(line) and line[0].startswith(" ") and directive == False:
            if not isinstance(data[key], str):
                # Not a string so continue on
                continue
            value = line.strip()
            if not len(value):
                # empty string, continue on
                continue
            # add next line
            data[key] += "\n{}".format(value)
            continue

        if last_type == STRING_TYPE and not len(line):
            if key in data.keys():
                data[key] += "\n"

    return json.dumps(records)


def type_converter(text):
    """ I convert strings into integers, floats, and strings! """
    if text.isdigit():
        return int(text), int

    try:
        return float(text), float
    except ValueError:
        return text, STRING_TYPE


def command_line_runner():
    """ I run functions from the command-line! """
    filename = sys.argv[-1]
    if not filename.endswith(".rst"):
        print("ERROR! Please enter a ReStructuredText filename!")
        sys.exit()
    print(rst_to_json(file_opener(filename)))

if __name__ == "__main__":
    command_line_runner()

########NEW FILE########
__FILENAME__ = tests
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import unittest

import simplicity

# Python 3 compatibility
P3K = sys.version > '3'
STRING_TYPE = str if P3K else unicode

MULTILINE_STRING_TEST = """A fun programming language.

Used to build simplicity!"""


class Rst2Json(unittest.TestCase):
    """ I test all facets of the Rst2Json function! Cool!"""

    def setUp(self):
        with open('sample.rst') as f:
            text = simplicity.rst_to_json(f.read())
        self.data = json.loads(text)
        with open('sample2.rst') as f:
            text = simplicity.rst_to_json(f.read())
        self.data2 = json.loads(text)

    def test_number_of_records(self):
        """ I test that the right number of records are created! """
        self.assertEqual(len(self.data), 3)

    def test_types(self):
        """ I test that Simplicity makes a list and each element is a dictionary! """
        self.assertTrue(isinstance(self.data, list))
        self.assertTrue(isinstance(self.data[0], dict))
        self.assertTrue(isinstance(self.data[1], dict))
        self.assertTrue(isinstance(self.data[2], dict))

    def test_titles(self):
        """ I test that each record has it's title element as it's dictionary title!"""
        self.assertEqual(self.data[0]['title'], "Python")
        self.assertEqual(self.data[1]['title'], "Java")
        self.assertEqual(self.data[2]['title'], "GitHub")

    def test_integer(self):
        """ I test integers by looking at the age of Python! """
        self.assertTrue(isinstance(self.data[0]['age'], int))

    def test_float(self):
        """ I test floats by looking at how much it costs to download Python! """
        self.assertTrue(isinstance(self.data[0]['price'], float))

    def test_string(self):
        """ I test strings by looking at Python's mascot! """
        self.assertTrue(isinstance(self.data[0]['mascot'], STRING_TYPE))

    def test_multiline_string(self):
        self.assertEquals(self.data[0]['description'], MULTILINE_STRING_TEST)

    def test_directives(self):
        self.assertEquals(self.data2[0]['title'], u'My Title (Sample ReST document)')


class FileOpener(unittest.TestCase):

    def test_basics(self):
        """ I test that file_opener returns more than just itself!"""
        text = simplicity.file_opener("sample.rst")
        self.assertNotEqual(text, "sample.rst")
        text = simplicity.file_opener("README.rst")
        self.assertNotEqual(text, "README.rst")

    def test_open(self):
        """ I test that file_opener gets things correctly!"""
        with open("sample.rst") as f:
            text = f.read()
        self.assertEqual(text, simplicity.file_opener("sample.rst"))


class TextCleanup(unittest.TestCase):
    pass


class TypeConverter(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()

########NEW FILE########
