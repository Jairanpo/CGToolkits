import pymel.core as pm
import json
import os

with open(os.path.join(os.path.dirname(__file__), 'controls.json')) as json_data:
    anim_curves = json.load(json_data)['control_curves']


def create(shot_data):
    shot_number = shot_data["shot"]
    main_anim = pm.curve(name='{}_main_CTL'.format(shot_number), degree=1, point=anim_curves['main'])
    main_anim.overrideEnabled.set(1)
    main_anim.overrideColor.set(27)
    main_anim.setRotationOrder('ZXY', 1)
    main_anim.addAttr('focalLength', keyable=True)
    main_anim.focalLength.set(35)
    main_anim.useOutlinerColor.set(True)
    main_anim.outlinerColor.set(.5, .6, .9)

    translate_anim = pm.curve(name='{}_translate_CTL'.format(shot_number), degree=1, point=anim_curves['translate'])
    translate_anim.overrideEnabled.set(1)
    translate_anim.overrideColor.set(28)
    translate_anim.setRotationOrder('ZXY', 1)
    translate_anim.rx.set(lock=True, keyable=False)
    translate_anim.ry.set(lock=True, keyable=False)
    translate_anim.rz.set(lock=True, keyable=False)
    translate_anim.sx.set(lock=True, keyable=False)
    translate_anim.sy.set(lock=True, keyable=False)
    translate_anim.sz.set(lock=True, keyable=False)
    translate_anim.v.set(lock=True, keyable=False)

    rotate_anim = pm.curve(name='{}_rotate_CTL'.format(shot_number), degree=1, point=anim_curves['rotate'])
    rotate_anim.overrideEnabled.set(1)
    rotate_anim.overrideColor.set(29)
    rotate_anim.setRotationOrder('ZXY', 1)
    rotate_anim.tx.set(lock=True, keyable=False)
    rotate_anim.ty.set(lock=True, keyable=False)
    rotate_anim.tz.set(lock=True, keyable=False)
    rotate_anim.sx.set(lock=True, keyable=False)
    rotate_anim.sy.set(lock=True, keyable=False)
    rotate_anim.sz.set(lock=True, keyable=False)
    rotate_anim.v.set(lock=True, keyable=False)

    shake_anim = pm.curve(name='{}_shake_CTL'.format(shot_number), degree=1, point=anim_curves['shake'])
    shake_anim.overrideEnabled.set(1)
    shake_anim.overrideColor.set(2)
    shake_anim.setRotationOrder('ZXY', 1)
    shake_anim.sx.set(lock=True, keyable=False)
    shake_anim.sy.set(lock=True, keyable=False)
    shake_anim.sz.set(lock=True, keyable=False)
    shake_anim.v.set(lock=True, keyable=False)

    camera = pm.camera()
    camera[0].rename('{}_CAM'.format(shot_number))
    camera[0].overrideEnabled.set(1)
    camera[0].overrideColor.set(1)
    camera[0].setRotationOrder('ZXY', 1)
    camera[0].tx.set(lock=True, keyable=False)
    camera[0].ty.set(lock=True, keyable=False)
    camera[0].tz.set(lock=True, keyable=False)
    camera[0].rx.set(lock=True, keyable=False)
    camera[0].ry.set(lock=True, keyable=False)
    camera[0].rz.set(lock=True, keyable=False)
    camera[0].sx.set(lock=True, keyable=False)
    camera[0].sy.set(lock=True, keyable=False)
    camera[0].sz.set(lock=True, keyable=False)
    camera[0].v.set(lock=True, keyable=False)
    # Create focal length
    main_anim.connectAttr('focalLength', '{}.focalLength'.format(camera[1]))

    camera[0].setParent(shake_anim)
    shake_anim.setParent(rotate_anim)
    rotate_anim.setParent(translate_anim)
    translate_anim.setParent(main_anim)
    return camera
