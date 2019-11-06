import layoutWindows
import pymel.core as pm


# ----------------------------------------------------------------------------------------------------------------------
class Window:

    def __init__(self):
        self.win = 'Storyboard_window'
        self.panel = 'Storyboard_modelPanel'

    #                         ...........................................

    def delete_storyboard_window_trash(self):
        if pm.modelPanel(self.panel, exists=True):
            pm.deleteUI(self.panel, panel=True)
            self.delete_existing_storyboard_window()
        else:
            print 'No Storyboard_window trash found'

    def delete_existing_storyboard_window(self):
        if pm.window(self.win, exists=True):
            pm.deleteUI(self.win, window=True)
        else:
            print 'Previous Storyboard_window was deleted'

    #                         ...........................................

    @staticmethod
    def create_storyboard_cam():
        storyboard_camera = layoutWindows.LayoutCamera().create('Storyboard_CAM')
        print '----------- Storyboard Camera:{0}-----------'.format(storyboard_camera.name())
        storyboard_window = layoutWindows.create_window('Storyboard')
        storyboard_window[1].setCamera(storyboard_camera.name())
        setup_model_editor(storyboard_window[1])
        storyboard_window[0].show()

    #                         ...........................................

    def create(self):
        self.delete_storyboard_window_trash()
        self.create_storyboard_cam()


# ----------------------------------------------------------------------------------------------------------------------


def setup_model_editor(model_panel):
    pm.modelEditor(model_panel, allObjects=False, edit=True)
    pm.modelEditor(model_panel, imagePlane=True, edit=True)
    pm.modelEditor(model_panel, grid=False, edit=True)
