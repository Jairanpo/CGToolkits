import layoutWindows
import pymel.core as pm

pm.headsUpDisplay('HUDFocalLength', visible=True, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
pm.headsUpDisplay('HUDCurrentFrame', visible=True, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
pm.headsUpDisplay('HUDCameraNames', visible=False, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
pm.headsUpDisplay('HUDFrameRate', visible=False, edit=True)
pm.headsUpDisplay('HUDViewAxis', visible=False, edit=True)


# ----------------------------------------------------------------------------------------------------------------------
class Window:

    def __init__(self):
        self.win = 'Playblast_window'
        self.panel = 'Playblast_modelPanel'

    #                         ...........................................

    def delete_playblast_window_trash(self):
        if pm.modelPanel(self.panel, exists=True):
            pm.deleteUI(self.panel, panel=True)
            self.delete_existing_playblast_window()
        else:
            print
            'No playblast_window trash found'

    def delete_existing_playblast_window(self):
        if pm.window(self.win, exists=True):
            pm.deleteUI(self.win, window=True)
        else:
            print
            'Previous Playblast_window was deleted'

    #                         ...........................................

    @staticmethod
    def create_playblast_cam():
        playblast_window = layoutWindows.create_window('Playblast')
        playblast_window[1].setCamera(pm.modelPanel(playblast_window[1], camera=True, query=True))
        setup_playblast_model_editor(playblast_window[1])
        setup_camera_settings(playblast_window[1])
        playblast_window[0].show()

    #                         ...........................................

    def create(self):
        self.delete_playblast_window_trash()
        self.create_playblast_cam()


# ----------------------------------------------------------------------------------------------------------------------


def setup_playblast_model_editor(model_panel):
    camera = pm.modelPanel(model_panel, camera=True, query=True)
    pm.modelEditor(model_panel, allObjects=False, edit=True)
    pm.modelEditor(model_panel, polymeshes=True, edit=True)
    pm.modelEditor(model_panel, imagePlane=True, edit=True)
    pm.modelEditor(model_panel, headsUpDisplay=True, edit=True)
    pm.modelEditor(model_panel, nParticles=True, edit=True)
    pm.modelEditor(model_panel, nurbsSurfaces=True, edit=True)
    pm.modelEditor(model_panel, grid=False, edit=True)
    pm.modelEditor(model_panel, selectionHiliteDisplay=False, edit=True)
    pm.modelEditor(model_panel, displayAppearance='smoothShaded', edit=True)
    pm.modelEditor(model_panel, displayTextures=True, edit=True)
    pm.modelEditor(model_panel, manipulators=False, edit=True)


def setup_camera_settings(model_panel):
    camera = pm.modelPanel(model_panel, camera=True, query=True)
    pm.setAttr(camera + ".displayGateMaskColor", 0, 0, 0)
    pm.setAttr(camera + ".displayGateMaskOpacity", 1)
    pm.setAttr(camera + ".displayGateMask", 1)
    pm.setAttr(camera + ".displayResolution", 1)
    pm.setAttr(camera + ".overscan", 1.1)
    pm.setAttr(camera + ".displaySafeAction", 1)
    pm.setAttr(camera + ".displaySafeTitle", 1)
