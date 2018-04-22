import bpy
import sys
import pkgutil
import inspect
import functools


bl_info = {
    'name': 'Simple meshes collection',
    'category': 'All',
    'author': 'Your name here',
    'version': (1, 0, 0),
    'blender': (2, 78, 0)
}


class Settings:
    @staticmethod
    def root_menu_icon(id_str=None):
        if id_str == 'simple':               # Add condition for custom icon for specific object
            return 'MOD_SCREW'
        return 'MOD_SCREW'

    @staticmethod
    def root_menu_name():
        # Change this name for specific root menu name
        return __name__

    @staticmethod
    def menu_icon(id_str=None):
        if id_str == 'simple.menu.example':  # Add condition for custom icon for specific object
            return 'FILESEL'
        return 'FILE_FOLDER'

    @staticmethod
    def operator_icon(id_str=None):
        if id_str == 'simple.Cylinder':      # Add condition for custom icon for specific object
            return 'MOD_SHRINKWRAP'
        elif id_str == 'simple.menu.example.Monkey':
            return 'IPO'
        return 'IPO_EASE_IN_OUT'


class PackageUtils:
    @staticmethod
    def split_parent_and_name(module):
        if '.' in module:
            return module[0:module.rfind('.')], module[module.rfind('.') + 1:]
        return '', module

    @staticmethod
    def get_package_entries(package_name):
        module = __import__(package_name, fromlist="dummy")
        modules = []
        classes = []
        prefix = package_name + '.'
        for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
            module = __import__(prefix + modname, fromlist="dummy")
            if getattr(module, '__path__', None):
                modules.append(module)
            else:
                classes += [cl[1] for cl in inspect.getmembers(module, inspect.isclass)]
        classes += [cl[1] for cl in inspect.getmembers(sys.modules[package_name], inspect.isclass)]
        return {'modules': modules, 'classes': classes}


class IndentedLogger:
    _indent = -1

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        IndentedLogger.indent()
        res = self.f(*args, **kwargs)
        IndentedLogger.dedent()
        return res

    def __get__(self, instance, cls):
        return functools.partial(self.__call__, instance)

    @staticmethod
    def indent():
        IndentedLogger._indent += 1

    @staticmethod
    def dedent():
        if IndentedLogger._indent > -1:
            IndentedLogger._indent -= 1

    @staticmethod
    def log(*args, **kwargs):
        if 'indent' not in kwargs.keys() or kwargs['indent']:
            print('|   ' * (IndentedLogger._indent), end='')
        for arg in args:
            print(arg + ' ', end='')

        if 'end' in kwargs.keys():
            print('', end=kwargs['end'])
        else:
            print()


class Entry:
    def __init__(self, parent):
        self.blender_id = 'INFO_MT_mesh_'
        self.blender_label = 'No label'
        self.entry = None
        self.parent = parent

    def register(self):
        if self.entry:
            try:
                bpy.utils.register_class(self.entry)
            except ValueError:
                bpy.utils.unregister_class(self.entry)
                bpy.utils.register_class(self.entry)

    def unregister(self):
        if self.entry:
            try:
                bpy.utils.unregister_class(self.entry)
            except ValueError:
                pass


class Operator(Entry):
    def __init__(self, cl, parent):
        super(self.__class__, self).__init__(parent)
        self.entry = cl

    @IndentedLogger
    def register(self):
        IndentedLogger.log('|-> registering operator \"' + str(self.entry.bl_label) + '\"...', end='')
        super(self.__class__, self).register()
        IndentedLogger.log('ok!', indent=False)

    @IndentedLogger
    def unregister(self):
        IndentedLogger.log('|-> unregistering opeartor \"' + str(self.entry.bl_label) + '\"...', end='')
        super(self.__class__, self).unregister()
        IndentedLogger.log('ok!', indent=False)


class Menu(Entry):
    def __init__(self, name=None, module=None, parent=None):
        super(self.__class__, self).__init__(parent)

        self.subitems = []

        if module:
            self._path = module.__path__
            self._name = module.__name__
        else:
            self._path = __path__
            self._name = __name__

        self.blender_id += self._name.replace('.', '_')
        if not name:
            self.blender_label = PackageUtils.split_parent_and_name(self._name)[1]
        else:
            self.blender_label = str(name)
        self.entry = self._create_blender_menu_type(self.blender_id, self.blender_label)

        entries = PackageUtils.get_package_entries(self._name)
        for module in entries['modules']:
            submenu = Menu(None, module, self)
            self.subitems.append(submenu)
            submenu_name = getattr(submenu.entry, 'bl_label', None)
            if not submenu_name:
                submenu_name = module.__name__.replace(self._name + '.', '')
                submenu.entry.bl_label = submenu_name
            self.entry.add_submenu(self.entry, submenu.entry, module.__name__, submenu_name)

        for cl in entries['classes']:
            if issubclass(cl, bpy.types.Operator):
                suboperator = Operator(cl, self)
                self.subitems.append(suboperator)
                operator_name = getattr(suboperator.entry, 'bl_label', None)
                if not operator_name:
                    operator_name = cl.__name__.replace(self._name + '.', '')
                    suboperator.entry.bl_label = operator_name
                self.entry.add_operator(self.entry, suboperator.entry, self._name + '.' + cl.__name__, operator_name)

    def menu(self, bpy_self, context):
        if self.entry:
            bpy_self.layout.menu(self.entry.bl_idname, text=self.entry.bl_label, icon=Settings.root_menu_icon(self._name))

    @IndentedLogger
    def register(self):
        IndentedLogger.log('|-- registering menu \"' + str(self.blender_label) + '\"')
        super(self.__class__, self).register()
        for si in self.subitems:
            si.register()
        IndentedLogger.log('|')
        IndentedLogger.log('|-> ok!')

    @IndentedLogger
    def unregister(self):
        IndentedLogger.log('|-- unregistering menu \"' + str(self.blender_label) + '\"')
        super(self.__class__, self).unregister()
        for si in self.subitems:
            si.unregister()
        IndentedLogger.log('|')
        IndentedLogger.log('|-> ok!')

    @staticmethod
    def _create_blender_menu_type(blender_id, blender_label):
        menu_type = type(blender_id, (bpy.types.Menu,),
                         {'bl_idname': blender_id,
                          'bl_label': blender_label})
        menu_type.operators = []
        menu_type.menus = []

        def draw(self, context):
            layout = self.layout
            layout.operator_context = 'INVOKE_REGION_WIN'

            for menu in self.menus:
                layout.menu(menu['object'].bl_idname, text=menu['text'], icon=Settings.menu_icon(menu['id']))

            for operator in self.operators:
                opid = operator['object'].bl_idname
                layout.operator(opid, text=operator['text'], icon=Settings.operator_icon(operator['id']))

        def add_submenu(self, bl_id, id_str, label):
            self.menus.append({'object': bl_id, 'id': id_str, 'text': label})

        def add_operator(self, bl_id, id_str, label):
            self.operators.append({'object': bl_id, 'id': id_str, 'text': label})

        menu_type.draw = draw
        menu_type.add_submenu = add_submenu
        menu_type.add_operator = add_operator
        return menu_type


def load_unload_nice_print(text):
    def dec(fun):
        def wrapper(*args, **kwargs):
            def p(mes, w, ind):
                m = ('=' * ind) + ' ' + mes + ' ' + ('=' * ind)
                if len(m) > w:
                    w = len(m)
                print('=' * w)
                print(m)
                print('=' * w)
            width = 48
            message = text + ' ' + bl_info['name']
            if len(message) >= width - 12:
                width = len(message) + 12
            indents = int((width - len(message)) / 2)

            p(message, width, indents)
            res = fun(*args, **kwargs)

            message = text + ' finished!'
            indents = int((width - len(message)) / 2)
            p(message, width, indents)
            print()
            return res
        return wrapper
    return dec


rootMenu = Menu(Settings.root_menu_name())


@load_unload_nice_print('loading')
def register():
    rootMenu.register()
    bpy.types.INFO_MT_mesh_add.append(rootMenu.menu)


@load_unload_nice_print('unloading')
def unregister():
    rootMenu.unregister()
    bpy.types.INFO_MT_mesh_add.remove(rootMenu.menu)
