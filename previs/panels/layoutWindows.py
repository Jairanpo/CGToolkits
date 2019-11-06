import pymel.core as pm


def create_window(title):
    w = pm.window('{0}_{1}'.format(title, 'window'), title=title)
    w.setHeight(540)
    w.setWidth(960)
    pm.paneLayout(configuration='vertical2')
    mp = pm.modelPanel('{0}_{1}'.format(title, 'modelPanel'))
    mp.setLabel('{0}_{1}'.format(title, 'modelPanel'))
    return w, mp


# ----------------------------------------------------------------------------------------------------------------------

class LayoutCamera:

    def __init__(self):
        self.all_cameras_in_scene = pm.ls(type='camera')

    #                           ................................................

    def create(self, camera_name):
        cams = self.get_cameras_with_prefix(camera_name)
        if self.is_more_than_one_camera(cams):
            return keep_only_first_item_from_list(cams)[0]
        elif self.one_camera_exists(cams):
            return cams[0]
        else:
            return self.create_camera(camera_name)

    #                           ................................................

    def get_cameras_with_prefix(self, camera_prefix):
        cam_list = []
        for each_camera in self.all_cameras_in_scene:
            if camera_prefix in each_camera.name():
                cam_list.append(pm.listRelatives(each_camera, parent=True)[0])
            else:
                continue
        return cam_list

    @staticmethod
    def create_camera(camera_name):
        camera = pm.camera(orthographic=False)[0]
        camera.rename(camera_name)
        return camera

    @staticmethod
    def one_camera_exists(list_of_cameras):
        if len(list_of_cameras) == 1:
            return True
        else:
            return False

    @staticmethod
    def is_more_than_one_camera(list_of_cameras):
        if len(list_of_cameras) > 1:
            return True
        else:
            return False


# ----------------------------------------------------------------------------------------------------------------------

def keep_only_first_item_from_list(list_of_nodes):
    list_of_nodes.sort()
    n = list_of_nodes.pop(0)
    print n
    for each_node in list_of_nodes:
        pm.delete(each_node)
    return n