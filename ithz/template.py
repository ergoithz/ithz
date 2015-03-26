from os.path import join, dirname
from ithz.lib import template
from ithz.utils import u

templatedir = join(dirname(dirname(__file__)),"templates")
def getTemplate(name,values):
    return u(template.render(join(templatedir, name), values))
