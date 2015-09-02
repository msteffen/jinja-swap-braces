import jinja2
import template_utils

def gencmd(cmd):
  return jinja2.Template(template_utils.swap_braces(cmd)).render(**globals())

def printcmds(*cmds, **vardefs):
  spcr = template_utils.Spacer();
  for k, v in vardefs.iteritems():
    print str(spcr) + k + '=' + gencmd(v)
  for c in cmds:
    print str(spcr) + gencmd(c)
