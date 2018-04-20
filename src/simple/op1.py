import bpy

class Cube(bpy.types.Operator):
    bl_idname = 'mesh.' + __name__.replace('.', '_')
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(radius=1.0, location=(0, 0, 0))
        return {'FINISHED'}
