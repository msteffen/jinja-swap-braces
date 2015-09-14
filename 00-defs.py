import jinja2
import itertools

import sys
sys.path.append('...path/to/template_utils.py')
import template_utils

def nz(s):
  return s is not None and len(s) > 0

def allnz(*ss):
  return all([ nz(s) for s in ss ])

def anynz(*ss):
  return all([ nz(s) for s in ss ])

def format_list(l, s):
  return s.format(*l)

def format_dict(d, s):
  return s.format(**d)

# class QuantifierExtension(Extension):
#   tags = set(['&&', '||', '&&/' '||/'])
#                                           
#   def parse(self, parser):
#     tok = next(parser.stream)
#
#     if (tok.value is '&&/'):
#       ast = parse_statements(['name:/&&'], drop_needle=True)
#       # TODO look at variables and if all variables are defined, print it
#     elif tok.value is '||/':
#       ast = parse_statements(['name:/||'], drop_needle=True)
#       # TODO look at variables and if any variables are defined, print it

env = jinja2.Environment(lstrip_blocks=True, trim_blocks=True,
                         extensions=['jinja2.ext.loopcontrols'])
env.filters.update({
  'nonzero': nz,
  'allnz'  : allnz,
  'anynz'  : anynz,
  'fmtl'   : format_list,
  'fmtd'   : format_dict,
})

def printglobal(key):
  print str(globals()[key])

def gencmd(cmd):
  return env.from_string(template_utils.swap_braces(cmd)).render(**globals())

# Example:
# in your ipython notebook:
# -----
# user = 'msteffen'
# instance = 'dev'
# -----
# printcmds('run_binary'
#   ' {% if instance == 'dev' %}192.168.0.1{% else %}10.0.13.2{% endif %}'
#   ' --user={user}'
#   ' --binary=${{BINARY}}',
#   BINARY='~/bin/{instance}_binary')
# -----
#
# This prints out:
#   BINARY="~/bin/dev_binary"
#   run_binary 192.168.0.1 --user=msteffen --binary=${BINARY}
# As the cell result in ipython, for easy copying and pasting (or further tweaking)
def printcmds(*cmds, **vardefs):
  print '\n\n'.join(itertools.chain(
    [ '{}={}'.format(k, gencmd(v)) for k, v in vardefs.iteritems() ],
    [ gencmd(c) for c in cmds ],
  ))
  
