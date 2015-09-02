"""Tests for 00-defs.py"""

import unittest
from template_utils import *
import jinja2

def gencmd(cmd):
  print swap_braces(cmd)
  return jinja2.Template(swap_braces(cmd)).render(**globals())

class TemplateUtilsTest(unittest.TestCase):
  def test_swap_braces(self):
    self.assertEquals(swap_braces("{param}"), "{{param}}")

  def test_swap_braces_block(self):
    self.assertEquals(swap_braces("block{{ }}"), "block{ }")

  def test_swap_braces_start_end(self):
    self.assertEqual(swap_braces("start_block {  "), "start_block {  ")
    self.assertEqual(swap_braces("     }"), "     }")

  def test_swap_braces_parens(self):
    self.assertEqual(swap_braces("a {% directive {% test %}%}"),
                     "a {% directive {% test %}%}")

  def test_swap_braces_complex(self):
    self.assertEqual(swap_braces("a{{{first}{second}}}"),
                     "a{{{first}}{{second}}}")
    self.assertEqual(swap_braces("a{{{first}}{{second}}}"),
                     "a{{{first}{second}}}")
    self.assertEqual(swap_braces("a{{{%first%}{%second%}}}"),
                     "a{{%first%}{%second%}}")

  def test_gencmd(self):
    globals()['param1'] = 'value1'
    self.assertEqual(gencmd("Print {param1}"), "Print value1")

if __name__ == '__main__':
  unittest.main()
