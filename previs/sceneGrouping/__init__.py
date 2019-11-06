import pymel.core as pm

GROUPS = {
    'characters': {'name': 'CHARACTERS_GRP', 'color': (.8, .6, .4)},
    'environments': {'name': 'ENVIRONMENT_GRP', 'color': (.4, .8, .4)},
    'lights': {'name': 'LIGHTS_GRP', 'color': (.7, .7, .3)},
    'cameras': {'name': 'CAMERAS_GRP', 'color': (.5, .6, .9)},
    'assets': {'name': 'ASSETS_GRP', 'color': (.65, .5, .9)},
    'FX': {'name': 'FX_GRP', 'color': (.8, .5, .6)},
    'tracking': {'name': 'TRACKING_GRP', 'color': (.4, .7, .6)},
}

ASSETS = {
    'graphics': {'name': 'graphics_GRP', 'color': (.7, .5, .7)},
    'mattePainting': {'name': 'mattePaingint_GRP', 'color': (.7, .5, .7)},
    'setDressing': {'name': 'setDressing_GRP', 'color': (.7, .5, .7)},
    'props': {'name': 'props_GRP', 'color': (.7, .5, .7)},
    'vehicles': {'name': 'vehicles_GRP', 'color': (.7, .5, .7)},
}

FX = {
    'simulations': {'name': 'simulations_GRP', 'color': (.8, .4, .5)},
    'character': {'name': 'characterFX_GRP', 'color': (.8, .4, .5)},
    'crowds': {'name': 'crows_GRP', 'color': (.8, .4, .5)}
}

CHARACTER = {
    'main': {'name': 'main_GRP', 'color': (.8, .6, .4)},
    'extras': {'name': 'extras_GRP', 'color': (.8, .6, .4)},
}

ENVIRONMENT = {
    'interior': {'name': 'interior_GRP', 'color': (.4, .8, .4)},
    'exterior': {'name': 'exterior_GRP', 'color': (.4, .8, .4)},
}

LIGHTING = {
    'lightRig': {'name': 'lightRig_GRP', 'color': (.7, .7, .3)},
    'characterIlumination': {'name': 'charIlumination_GRP', 'color': (.7, .7, .3)},
}


def group_already_exists(group_name):
    if len(pm.ls(group_name)) != 0:
        return True
    else:
        return False


def create_child_groups(parent_grp, child_groups_dict):
    subgroups_list = []
    for name, properties in child_groups_dict.items():
        subgroup = pm.group(name=properties['name'], empty=True)
        subgroup.useOutlinerColor.set(True)
        subgroup.outlinerColor.set(properties["color"])
        subgroup.setParent(parent_grp)
        subgroups_list.append(subgroup)


def create_childrens(parent_grp):
    if parent_grp.name() == 'CHARACTERS_GRP':
        create_child_groups(parent_grp, CHARACTER)
    elif parent_grp.name() == 'ENVIRONMENT_GRP':
        create_child_groups(parent_grp, ENVIRONMENT)
    elif parent_grp.name() == 'ASSETS_GRP':
        create_child_groups(parent_grp, ASSETS)
    elif parent_grp.name() == 'FX_GRP':
        create_child_groups(parent_grp, FX)
    elif parent_grp.name() == 'LIGHTS_GRP':
        create_child_groups(parent_grp, LIGHTING)
    else:
        pass


def create_groups():
    for element in GROUPS.items():
        if not group_already_exists(element[1]["name"]):
            current = pm.group(name=element[1]["name"], empty=True)
            current.useOutlinerColor.set(True)
            current.outlinerColor.set(element[1]["color"])
            create_childrens(current)
        else:
            current = pm.ls(element[1]["name"])[0]
            current.useOutlinerColor.set(True)
            current.outlinerColor.set(element[1]["color"])