import bpy

bl_info = {
    "name": "Animation in placer",
    "author": "Jakub Sygnowski",
    "blender": (2, 91, 0),
    "category": "Object",
}


class AnimationInPlacer(bpy.types.Operator):
    """AnimationInPlacer"""
    bl_idname = "object.animation_in_placer"
    bl_label = "Make animation in place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.active_object
        if selected.type != "ARMATURE":
            self.report({'ERROR'}, "Select armature first.")
        root_bone_name = self.find_root_bone(selected)
        for fcurve in selected.animation_data.action.fcurves:
            if not fcurve.data_path.startswith(f'pose.bones["{root_bone_name}"]'):
                continue
            self.in_place_fcurve(fcurve)

        return {'FINISHED'}
    
    def find_root_bone(self, obj):
        for name, bone in obj.pose.bones.items():
            if bone.parent is None:
                return name
        
    def in_place_fcurve(self, fcurve):
        x_start, x_end = fcurve.range()
        start_point = fcurve.keyframe_points[0].co
        end_point = fcurve.keyframe_points[-1].co
        assert start_point[0] == x_start and end_point[0] == x_end
        y_start, y_end = start_point.y, end_point.y
        per_x_angle = (y_end - y_start) / (x_end - x_start)
        for point in fcurve.keyframe_points:
            to_the_right = point.co[0] - x_start
            point.co[1] -= per_x_angle * to_the_right


class InPlacerSidePanel(bpy.types.Panel):
    bl_idname = "InPlacerSidePanel"
    bl_label = "Animation in placer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "In Placer"
    bl_order = 0

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_y = 1.5
        row.operator("object.animation_in_placer", icon='ARMATURE_DATA')
        

def register():
    bpy.utils.register_class(AnimationInPlacer)
    bpy.utils.register_class(InPlacerSidePanel)
    


def unregister():
    bpy.utils.unregister_class(AnimationInPlacer)
    bpy.utils.register_class(InPlacerSidePanel)


if __name__ == "__main__":
    register()
