"""
  Utils used by 00-defs.py, to make using jinja2 for command and boilerplate
  templates a little more compact.
"""

import re

ws_regex = re.compile(r'^(\s*)(.*?)(\s*)$')
# Dear Future Matthew:
# I'm quite proud of this regex smithing, but it is really weird. The idea is
# that the (}?) and ({?) subexpressions aren't processed by
# _swap_braces_recursive, but the stuff in the larger expression is. Since I
# want leading and trailing braces to be processed if they're part of a pair,
# I need to force braces into the larger expression if they're part of a pair,
# and into the smaller expression if they're not.
#
# The way I accomplished this was to put start-of-line and end-of-line tokens
# in the large expression (i.e. the one that's processed).
#
# Now, there are two types of string that don't end in a brace:
# a nonempty string that ends in a non-brace character, and an empty string.
#
# Therefore, the larger expression always has three clauses:
# 1) a nonempty string that ends in a non-brace (rbrace_regex; starts
#    with a non-brace for lbrace_regex)
# 2) an empty string ($ in lbrace_regex and ^ in rbrace regex)
# 3) a nonempty string that includes the whole line, including any
#    leading/trailing braces, so that they can be processed (this includes
#    the start-of-line/end-of-line characters, which it seems can match more
#    than once)
#
# If 1) or 2) match, then the leading/trailing brace will be captured by the
# small capture group and not processed. If 3 matches, then there is either no
# leading/trailing brace, or it's part of a pair and should be processed anyway.
#
# This seems to work, and I'm weirdly proud of it, for like 100 bytes of code.
lbrace_regex = re.compile('^(}?)([^}].*?|$|^.*?)$')
rbrace_regex = re.compile('^(.*?[^{]|^|.*?$)({?)$')

def _swap_braces_recursive(tok, line):
  """ Recursive utility method used by swap_braces """
  if tok == '' and line == '': return ''
  elif tok in ['{%','%}','{#','#}','{}']:  # Case 1 and 2 in swap_braces
    return tok + _swap_braces_recursive(line[:2],line[2:])
  elif tok in ['{{','}}']:       # }} -> } and {{ -> {
    return tok[0] + _swap_braces_recursive(line[:2],line[2:])
  elif tok[0] in ['{','}']:      # } -> }} and { -> {{
    return (tok[0]*2) + _swap_braces_recursive(tok[1:]+line[:1], line[1:])
  else:                          # default (do nothing)
    return tok[0] + _swap_braces_recursive(tok[1:]+line[:1], line[1:])

def swap_braces(template_str):
  """
    Swap single and double curly braces (except in a few cases enumerated below)
    to convert a command string to a jinja2 template. I thought this would be
    useful because I use parameters a lot more than I use parentheses, and that
    this would make my command templates clearer.

    Special cases:
      1a) '...{%...' -> '...{%...' and '...%}...' -> '...%}...'
      1b) '...{#...' -> '...{#...' and '...#}...' -> '...#}...'
      This is necessary as {% and {# are part of the jinja syntax.

      2) '...{}...' -> '...{}...'
      This is convenience, since {} is used in C++ constructors a lot (which I
      expect to use in templates a lot) and "{}" doesn't make sense as a
      parameter

      3) '...{  ' -> '...{  ' and '   }...' -> '   }...'
      This is also convenience. Typically C++/Java blocks start with a line with
      '{' as the final character and end with '}' led by whitespace. This lets
      me avoid writing "{{" at the start of all such blocks. Also, there's no
      way e.g. a '{' at the end of the line could be opening a parameter, so
      this exception doesn't introduce any ambiguity

    Except as noted above, all instances of '{' convert to '{{', and all
    instances of '{{' convert to '{'. Same for '}' and '}}'.
  """
  new_template_lines = []
  for line in template_str.splitlines():
    # Extract leading whitespace and braces (to support special case 3 above)
    leading_ws, line, trailing_ws = ws_regex.match(line).groups()
    l_brace, line = lbrace_regex.match(line).groups()
    line, r_brace = rbrace_regex.match(line).groups()
    # Process string (leaving leading/trailing ws & braces unprocessed)
    new_template_lines.append(''.join([
        leading_ws,
        l_brace,
        _swap_braces_recursive(line[:2], line[2:]),
        r_brace,
        trailing_ws,
    ]))
  return '\n'.join(new_template_lines)
