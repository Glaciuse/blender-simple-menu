# The blender simple menu

This plugin collect all classes inherited from bpy.types.Operator and push them to blender's menu for easy use

How it looks like:

![Alt text](doc/menu-example.png?raw=true "Menu example")

## Overview

This plugin consists of only one file: __init__.py
To run this plugin you need to create folder with any name in blender's plugin directory and put this __init__.py file to it.
After that you can create any classes/modules in that folder and plugin automatically will find all Operators and put them to menu.

## Getting Started

1. Copy content from src directory to blender's plugin path.

On Linux:
```
/home/your-name/.config/blender/blender-version/scripts/addons/
```

On Windows:
```
C:\Users\%username%\AppData\Roaming\Blender Foundation\Blender\blender-version\scripts\addons\
```
2. Enable plugin in blender's settings ( Ctrl + Alt + U )

![Alt text](doc/blender-settings.png?raw=true "Blender settings")

3. Change files for your own purpose!

4. Enjoy!

## Some settings

1. Change your meshes collection name and author in bl_info located in the __init__.py file

![Alt text](doc/bl-info.png?raw=true "bl_info")

2. You can change the name of root menu or add custom icons for your operators by adding Settings class in __init__.py file

![Alt text](doc/plugin-settings.png?raw=true "Plugin settings")

## New features

Make a request!

## Licence

MIT
