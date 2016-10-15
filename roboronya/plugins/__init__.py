from os.path import dirname, basename, isfile
from operator import itemgetter
import glob, inspect

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
__all__.remove('__init__')
__all__.remove('plugin')

commands = []
meta_dict = []
run_commands = {}

from roboronya.utils import get_logger
logger = get_logger(__name__)

for imported in __all__:
    exec('from roboronya.plugins import '+imported+' as p')
    list = inspect.getmembers(p, inspect.isclass)
    
    for (name, clazz) in list:
        if issubclass(clazz, plugin.Plugin) and clazz != plugin.Plugin:
            if hasattr(clazz, 'description') and hasattr(clazz, 'name') and clazz.name not in commands:
                commands.append(clazz.name)
                run_commands[clazz.name] = clazz.run
                if hasattr(clazz, 'aliases'):
                    for alias in clazz.aliases:
                        if alias not in commands:
                            commands.append(alias)
                            run_commands[alias] = clazz.run
                            meta_dict.append({'name':alias, 'description':'Alias for **/'+clazz.name+'**'})
                        else:
                            logger.warning('Alias '+alias+' already loaded.')
                meta_dict.append({'name':clazz.name, 'description':clazz.description})
                logger.info('Module '+imported+' loaded.')
                break
            else:
                logger.error('Command '+clazz.name+' already loaded.')

meta_dict = sorted(meta_dict, key=itemgetter('name', 'description'))

def run(*args, **kwargs):
    command = kwargs['command']
    run = run_commands[command]
    run(*args, **kwargs, metadata = meta_dict)
