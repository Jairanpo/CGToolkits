import pymel.core as pm


class ShotRetimer():
    def __init__(self):
        pass

    @property
    def shots(self):
        return pm.sequenceManager(listShots=True)

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
        _first_frame = self.first_frame
        _last_frame = self.last_frame
        shot = pm.ls(sl=True, type="shot")

        if len(shot) == 1 and amount != 0:
            shot = shot[0]
            _shots_to_move = None

            if amount > 0:
                _shots_to_move = self.get_shots_ahead(shot)
            else:
                _shots_to_move = self.get_shots_behind(shot)

            # self.enrich_shot_data(_shots_to_move, amount)
            # self.move_shot_sequencer(each_shot, amount)

        '''
            result["status"] = "success"
            result["message"] = "Shots moved by {0} frames.".format(amount)
        else:
            result["status"] = "warning"
            result["message"] = "You have to select only one shot or your amount to move was 0."
        '''

        return self.enrich_shot_data(_shots_to_move, amount)

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

    def empty_frames(self, shot=None):
        '''

        Summary:
            Get empty frames between this shot and the previous and following shots.

        Arguments:
            - shot: The source shot (default = pm.ls(sl=True, type="shot")[0])

        '''
        result = {"shot": shot, "before": 0, "after": 0}
        _shots_in_scene = self.shots
        _shot_before = None
        _shot_after = None

        if shot is None:
            shot = pm.ls(sl=True, type="shot")[0]
            result["shot"] = shot

        if len(self.get_shots_behind(shot)) > 1:
            _shot_before = self.get_shots_behind(shot)[-2]
            result["before"] = abs(
                shot.getStartTime() - _shot_before.getEndTime())
        else:
            result["before"] = None
        if len(self.get_shots_ahead(shot)) > 1:
            _shot_after = self.get_shots_ahead(shot)[1]
            result["after"] = abs(
                _shot_after.getStartTime() - shot.getEndTime())
        else:
            result["after"] = None

        return result

    def enrich_shot_data(self, list_of_shots, amount=0):
        '''
        Summary:
            This method will create an enriched list with the name of the shot,
            empty frames before and after

        Arguments:
            list_of_shots: The list of shots that require or might require to be moved.
                            The list should enter has a moving precendence hierarch:
                            - If shots had to move forward, then the they are ordered as lasts to first.
                            - If shots had to move backward, then they are ordered as first to last.

        Returns:
            list of shots[
                {
                   "shot": Name of the shot,
                   "before": Amount of empty frames before
                   "after": Amount of empty frames after
                   "move": how much frames the shot has to be moved
                }...
            ]
        '''
        result = []

        for each in list_of_shots:
            result.append(self.empty_frames(each))

        for index, each in enumerate(result):
            if index == 0:
                each["move"] = amount
                if (each["after"] - amount) > 1:
                    if index + 1 == len(result):
                        each["move"] = False
                    else:
                        result[index + 1]["move"] = False

        return result

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
