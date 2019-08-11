import os
try:
    import importlib.util
except:
    import imp
from xdg import BaseDirectory

from vit import env

DEFAULT_VIT_DIR = '~/.vit'

class Loader(object):
    def __init__(self):
        vit_dir = DEFAULT_VIT_DIR
        xdg = BaseDirectory.load_first_config('vit')
        if 'VIT_DIR' in env.user:
            vit_dir = env.user['VIT_DIR']
        elif xdg:
            vit_dir = xdg
        self.user_config_dir = os.path.expanduser(vit_dir)

    def load_user_class(self, module_type, module_name, class_name):
        module = '%s.%s' % (module_type, module_name)
        filepath = '%s/%s/%s.py' % (self.user_config_dir, module_type, module_name)
        try:
            mod = self.import_from_path(module, filepath)
        except:
            return None
        return getattr(mod, class_name)

    def import_from_path(self, module, filepath):
        try:
            spec = importlib.util.spec_from_file_location(module, filepath)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        except:
            mod = imp.load_source(module, filepath)
            return mod
