import pymel.core as pm


class ShotRetimer():
    def __init__(self):
        pass

    @property
    def shots(self):
        result = []
        _shots = pm.sequenceManager(listShots=True)
        _start_frame_list = []

        for each in _shots:
            _start_frame_list.append(each.getStartTime())

        _start_frame_list.sort()

        for start_frame in _start_frame_list:
            for shot in _shots:
                if shot.getStartTime() == start_frame:
                    result.append({"shot": shot})
                else:
                    pass

        result = self.empty_frames(result)

        return result

    @property
    def animation_curves(self):
        result = pm.ls(type="animCurve")
        return result

    @property
    def first_frame(self):
        _anim_curves = pm.ls(type="animCurve")
        result = None

        if len(_anim_curves) > 0:
            result = _anim_curves[0].getTime(0)
            for curve in _anim_curves:
                if curve.getTime(0) < result:
                    result = curve.getTime(0)
        else:
            result = "No keyframes in scene"

        return result

    @property
    def last_frame(self):
        _anim_curves = pm.ls(type="animCurve")
        result = None
        if len(_anim_curves) > 0:
            result = _anim_curves[0].getTime(_anim_curves[0].numKeys() - 1)
            for curve in _anim_curves:
                _num_keys_index_total = curve.numKeys() - 1
                if curve.getTime(_num_keys_index_total) > result:
                    result = curve.getTime(_num_keys_index_total)
        else:
            result = "No keyframes in scene"

        return result

    def move_keyframes(self, amount, time_range):
        _curves = self.animation_curves()

        if len(_curves) > 0:
            for curve in _curves:
                pm.keyframe(curve, edit=True, relative=True,
                            timeChange=amount, time=time_range)

    def move_shots(self, amount):
        result = {"status": "", "message": ""}

        _shots_in_scene = self.shots
        _shots = pm.ls(sl=True, type="shot")
        _range = ShotRetimer.selected_shots_range_index(
            _shots, _shots_in_scene)
        print(_range)

        if ShotRetimer.are_overlapping_shots(_shots_in_scene):
            result["status"] = "error"
            result["message"] = "You have overlapping shots in the scene."
            return result

        for i, each in enumerate(_shots_in_scene):
            if i in _range:
                each["moveIt"] = amount
            else:
                each["moveIt"] = 0

        for i, each in enumerate(_shots_in_scene):
            if each["moveIt"] > each["emptyFramesAfter"]:
                _next_shot = _shots_in_scene[i + 1]
                _delta = amount - each["emptyFramesAfter"]
                _next_shot["moveIt"] = 0 if _delta < 1 else _delta

        return _shots_in_scene

    def empty_frames(self, list_of_shots):
        '''

        Summary:
            Get empty frames between this shot and the previous and following shots.

        Arguments:
            - shot: The source shot (default = pm.ls(sl=True, type="shot")[0])

        '''
        result = []

        if len(list_of_shots) > 1:

            for i, each in enumerate(list_of_shots):

                if each == list_of_shots[0]:  # If it is the first one
                    each["emptyFramesBefore"] = "infinite"
                    each["emptyFramesAfter"] = abs(
                        list_of_shots[i + 1]["shot"].getStartTime() - each["shot"].getEndTime())

                    each["emptyFramesAfter"] -= 1

                elif each == list_of_shots[-1]:  # If it is the last one
                    each["emptyFramesAfter"] = "infinite"
                    each["emptyFramesBefore"] = abs(
                        list_of_shots[i - 1]["shot"].getEndTime() - each["shot"].getStartTime())
                    each["emptyFramesBefore"] -= 1

                else:
                    each["emptyFramesBefore"] = abs(
                        list_of_shots[i - 1]["shot"].getEndTime() - each["shot"].getStartTime())
                    each["emptyFramesAfter"] = abs(
                        list_of_shots[i + 1]["shot"].getStartTime() - each["shot"].getEndTime())

                    each["emptyFramesBefore"] -= 1
                    each["emptyFramesAfter"] -= 1

                result.append(each)

        else:
            list_of_shots[0]["emptyFramesAfter"] = "infinite"
            list_of_shots[0]["emptyFramesBefore"] = "infinite"
            result = list_of_shots

        return result

    @classmethod
    def are_overlapping_shots(cls, list_of_shots):
        for shot in list_of_shots:
            if shot["emptyFramesAfter"] < 0 or shot["emptyFramesBefore"] < 0:
                return True

        return False

    @staticmethod
    def move_shot_sequencer(shot, amount):
        shot.sequenceStartFrame.set(
            shot.sequenceStartFrame.get() + amount)
        shot.sequenceEndFrame.set(
            shot.sequenceEndFrame.get() + amount)
        shot.startFrame.set(
            shot.startFrame.get() + amount)
        shot.endFrame.set(
            shot.endFrame.get() + amount)

    @classmethod
    def selected_shots_range_index(cls, selected_shots, list_of_shots):
        range = []
        for i, each in enumerate(list_of_shots):
            for shot in selected_shots:
                if shot == each["shot"]:
                    range.append(i)

        range.sort()
        return range
