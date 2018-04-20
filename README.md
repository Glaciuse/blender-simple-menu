# The blender simple mesh menu operators

This plugin collect all classes inherited from bpy.types.Operator and push them to blender's menu for easy use

How it looks like:

![Alt text](doc/menu-example.png?raw=true "Menu example")

## Getting Started

### 1. Copy content from src directory to blender's plugin path.

On Linux:
```
/home/your-name/.config/blender/blender-version/scripts/addons/
```

On Windows:
```
C:\Users\%username%\AppData\Roaming\Blender Foundation\Blender\blender-version\scripts\addons\
```
### 2. Enable plugin in blender's settings ( Ctrl + Alt + U )

![Alt text](doc/blender-settings.png?raw=true "Blender settings")

## Some settings

### 1. Change your meshes collection name and author in bl_info located in the __init__.py file

![Alt text](doc/bl-info.png?raw=true "bl_info")

### 2. You can change the name of root menu or add custom icons for your operators by adding Settings class in __init__.py file

![Alt text](doc/plugin-settings.png?raw=true "Plugin settings")


