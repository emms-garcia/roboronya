from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
__all__.remove('__init__')

meta_dict = []

from roboronya.utils import get_logger
logger = get_logger(__name__)

for imported in __all__:
    exec('import roboronya.plugins.'+imported)
    name = None
    description = None
    try:
        exec('name = "'+imported+'"')
        exec('description = '+imported+'.description')
        logger.info('Module '+imported+' loaded.')
        meta_dict.append({'name':name, 'description':description})
    except AttributeError:
        pass

def run(*args, **kwargs):
    command = kwargs['command']
    if command in __all__:
        exec("if issubclass("+command+".Command, roboronya.plugins.plugin.Plugin):"+
             "\n\t"+command+".Command.run(*args, **kwargs, metadata = meta_dict)"+
             "\nelse:"+
             "\n\tlogger.error('Invalid Module "+command+".')")
