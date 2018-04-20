import bpy

class Cylinder(bpy.types.Operator):
    bl_idname = 'mesh.' + __name__.replace('.', '_')
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=2, location=(0, 0, 0))
        return {'FINISHED'}
 
