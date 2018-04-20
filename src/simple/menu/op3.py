import bpy

class Torus(bpy.types.Operator):
    bl_idname = 'mesh.' + __name__.replace('.', '_')
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute(self, context):
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0))
        return {'FINISHED'}
 
