import pymel.core as pm


class ShotRetimer():
    def __init__(self):
        pass

    @property
    def shots(self):
        return pm.ls(type="shot")

    @property
    def animation_curves(self):
        result = pm.ls(type="animCurve")
        return result

    @property
    def first_shot(self):
        self.shots = pm.ls(type="shot")

        def _find_first_shot():
            _shots = self.shots
            _first_shot = None

            if len(_shots) > 0:
                _first_shot = _shots[0]
                _first_frame = _shots[0].getStartTime()
                for each in _shots:
                    if each.getStartTime() < _first_frame:
                        _first_shot = each
            else:
                _first_shot = "No first shot in the scene."

            return _first_shot

        return _find_first_shot()

    @property
    def last_shot(self):
        self.shots = pm.ls(type="shot")

        def _find_last_shot():
            _shots = self.shots
            _last_shot = None

            if len(_shots) > 0:
                _last_shot = _shots[0]
                _last_frame = _shots[0].getEndTime()
                for each in _shots:
                    if each.getStartTime() > _last_frame:
                        _last_shot = each
            else:
                _last_shot = "No last shot in the scene."

            return _last_shot

        return _find_last_shot()

    @property
    def first_frame(self):
        _anim_curves = pm.ls(type="animCurve")
        result = _anim_curves[0].getTime(0)

        for curve in _anim_curves:
            if curve.getTime(0) < result:
                result = curve.getTime(0)

        return result

    @property
    def last_frame(self):
        self.shots = pm.ls(type="shot")
        _anim_curves = pm.ls(type="animCurve")
        result = _anim_curves[0].getTime(_anim_curves[0].numKeys() - 1)
        print(result)
        for curve in _anim_curves:
            _num_keys_index_total = curve.numKeys() - 1
            if curve.getTime(_num_keys_index_total) > result:
                result = curve.getTime(_num_keys_index_total)

        return result

    def move_keyframes(self, amount, time_range):
        _curves = self.animation_curves()

        if len(_curves) > 0:
            for curve in _curves:
                pm.keyframe(curve, edit=True, relative=True,
                            timeChange=amount, time=time_range)

    def move_shots(self, amount):
        result = {"status": "", "message": ""}
        _first_frame = self.first_frame
        _last_frame = self.last_frame
        shot = pm.ls(sl=True, type="shot")

        if len(shot) == 1 and amount != 0:
            shot = shot[0]
            _shots_to_move = self.get_shots_ahead(
                shot) if amount > 0 else self.get_shots_behind(shot)

            for each_shot in _shots_to_move[::-1]:
                each_shot.sequenceStartFrame.set(
                    each_shot.sequenceStartFrame.get() + amount)
                each_shot.sequenceEndFrame.set(
                    each_shot.sequenceEndFrame.get() + amount)
                each_shot.startFrame.set(
                    each_shot.startFrame.get() + amount)
                each_shot.endFrame.set(
                    each_shot.endFrame.get() + amount)
            result["status"] = "success"
            result["message"] = "Shots moved by {0} frames.".format(amount)
        else:
            result["status"] = "warning"
            result["message"] = "You have to select only one shot or your amount to move was 0."

        return result

    def get_shots_ahead(self, current_shot):
        _ordered_shots = pm.sequenceManager(listShots=True)
        starting_index = None
        for index, shot in enumerate(_ordered_shots):
            if current_shot == shot:
                starting_index = index

        return _ordered_shots[starting_index:]

    def get_shots_behind(self, current_shot):
        _ordered_shots = pm.sequenceManager(listShots=True)
        _last_index = None
        for index, shot in enumerate(_ordered_shots):
            if current_shot == shot:
                _last_index = index

        return _ordered_shots[:_last_index + 1]
