import jinja2
import template_utils

def gencmd(cmd):
  return jinja2.Template(template_utils.swap_braces(cmd)).render(**globals())

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
  
def printcmds(*cmds, **vardefs):
  print '\n'.join(flatten([
    [ '{}={}'.format(k, gencmd(v)) for k, v in vardefs.iteritems() ],
    [ gencmd(c) for c in cmds ],
  ]))
