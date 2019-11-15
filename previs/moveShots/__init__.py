import pymel.core as pm


def move_shots(list_of_shots, amount):
    result = {"status": "", "message": ""}
    if len(list_of_shots) > 0 and amount != 0:
        for each_shot in list_of_shots:
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
        result["status"] = "error"
        result["message"] = "You didn\'t select any node or your amount was 0."

    return result


def move_keyframes(
        list_of_animation_curves,
        amount,
        time_range):
    result = {"status": "", "message": ""}

    if list_of_animation_curves > 0:
        for each_curve in list_of_animation_curves:
            print(result)
            if result["status"] == "error":
                return result
            else:
                pass

            try:
                pm.keyframe(
                    each_curve,
                    edit=True,
                    relative=True,
                    timeChange=amount,
                    time=time_range)
            except:
                result["status"] = "error"
                result["message"] = '''
                    Unable to move your animation curves, please make sure that
                    you are using an appropiate method, shots should be moved as blocks:
                    - You can't move a shot individually that it's in between two other shots,
                      this is because animation keys had to overlap and that it's not a valid
                      operation in Maya.
                    - To move one shot that exists between other shots, you should pick the following
                      shots too if you want to move foward in time or the preceding shots if you want to move it
                      backwards in time.
                    - Look for overshooting keyframes outside your shots ran 
                '''
                print(result)

    result["status"] = "success"
    result["message"] = "Keyframe(s) moved successfully."

    return result


def get_min_frame(list_of_shots):
    start = list_of_shots[0].startFrame.get()
    for each_shot in list_of_shots:
        shot_start_frame = each_shot.startFrame.get()
        if shot_start_frame < start:
            start = shot_start_frame
        else:
            continue
    return start


def get_max_frame(
        list_of_shots):
    end = list_of_shots[0].endFrame.get()
    for each_shot in list_of_shots:
        shot_end_frame = each_shot.endFrame.get()
        if shot_end_frame > end:
            end = shot_end_frame
        else:
            continue
    return end


def are_shots_selected(list_of_shots):
    if len(list_of_shots) > 0:
        return True
    else:
        return False


def retime_shots(amount):
    shot_list = pm.ls(sl=True, type="shot")
    animation_list = pm.ls(type="animCurve")
    result = {"status": "", "message": ""}

    if are_shots_selected(shot_list):
        result = move_keyframes(amount=amount,
                                time_range=(
                                    get_min_frame(shot_list),
                                    get_max_frame(shot_list)),
                                list_of_animation_curves=animation_list)
        print(result)

        if result["status"] == "success":
            move_shots(
                list_of_shots=shot_list,
                amount=amount)
            result["message"] = "Shots moved by {0} frames.".format(amount)

        return result
    else:
        result["status"] = "error"
        result["message"] = "You didn\'t select shots in the sequencer."

    return result
