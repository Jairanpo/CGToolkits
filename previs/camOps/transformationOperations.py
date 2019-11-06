import pymel.core as pm


def align():
    result = {"status": "", "message": ""}

    list_of_nodes = pm.ls(sl=True, type='transform')

    if len(list_of_nodes) < 2:
        result["status"] = "error"
        result["message"] = "You have to select xform node sources to apply alignment, and your target as your last selection"
        return result

    def get_last_node_transformations():
        last_node = list_of_nodes[-1]
        t = pm.xform(last_node, t=True, query=True, ws=True)
        r = pm.xform(last_node, ro=True, query=True, ws=True)
        return {"position": t, 'rotation': r}

    target_position_dictionary = get_last_node_transformations()
    list_of_nodes.pop()
    for each_node in list_of_nodes:
        pm.xform(each_node, t=target_position_dictionary.get('position'), ws=True)
        pm.xform(each_node, ro=target_position_dictionary.get(
            'rotation'), ws=True)

    result["status"] = "success"
    result["message"] = "Your sources where aligned."
    return result


def reset_transform():
    result = {"status": "", "message": ""}

    list_of_transform_nodes = pm.ls(sl=True, type='transform')

    if len(list_of_transform_nodes) == 0:
        result["status"] = "error"
        result["message"] = "You didn\'t select any xform node to reset"
        return result

    axis = ['X', 'Y', 'Z']
    for element in list_of_transform_nodes:
        for coord in axis:
            if not pm.getAttr(element + '.translate' + coord, lock=True):
                pm.setAttr(element + '.translate' + coord, 0)
            if not pm.getAttr(element + '.rotate' + coord, lock=True):
                pm.setAttr(element + '.rotate' + coord, 0)
            if not pm.getAttr(element + '.scale' + coord, lock=True):
                pm.setAttr(element + '.scale' + coord, 1)

    result["status"] = "success"
    result["message"] = "Your xform nodes transformations where set to 0"
    return result
