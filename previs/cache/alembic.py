# System
import os

# Third party
import pymel.core as pm

# Local
import agnostics.cache as agCache


class Alembic():
    def __init__(self):
        self.cache_objects = pm.ls(sl=True, type='transform')
        self.selected_shot = pm.ls(sl=True, type='shot')
        self.geometry_folder = 'ReferenceGeometry'

    def selected_objects_root_flags(self):
        root_flags = ''
        for each in self.cache_objects:
            root_flags = root_flags + '-root ' + each.longName() + ' '
        return root_flags

    def object_root_flag(self, node):
        return '-root ' + node.longName() + ' '

    def are_cache_objects_selected(self):
        result = {
            "status": False,
            "message": ""
        }
        if len(self.cache_objects) == 0:
            result["message"] = "You did not select any objects in the scene"
        else:
            result["status"] = True
            result["message"] = "Scene object are selected"

        return result

    def is_one_shot_selected(self):
        result = {
            "status": False,
            "message": ""
        }
        if len(self.selected_shot) != 1:
            result["message"] = "You have to select only one shot"
        else:
            result["status"] = True
            result["message"] = "One shot selected"

        return result

    def create_paths(self):
        scene_path = pm.sceneName().split('/')[:-1]
        scene_path = "\\".join(scene_path)
        geo_path = os.path.join(scene_path, self.geometry_folder)
        cam_path = scene_path
        paths = {
            "scene": scene_path,
            "camera": cam_path,
            "geometry": geo_path
        }

        return paths

    def get_shot_name(self, shot_node):
        return shot_node.name().split('_')[1]

    def export(self, path):
        are_selected_objects = self.are_cache_objects_selected()
        is_shot_selected = self.is_one_shot_selected()

        if are_selected_objects["status"] and is_shot_selected["status"]:
            start = self.selected_shot[0].getSequenceStartTime()
            end = self.selected_shot[0].getSequenceEndTime()

            for each in self.cache_objects:
                root_flag = self.object_root_flag(each)
                base_name = each.longName().split(
                    "|")[1].replace(':', '_').replace("|", "_")
                file_path = os.path.join(path, base_name)
                agCache.export_alembic(start, end, root_flag, file_path)
        else:
            return pm.warning('Check script editor for error details')
