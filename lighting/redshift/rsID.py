import pymel.core as pm
import math


class RedShiftIDs:

    def __init__(self):
        self.scene_ids = None
        self.ids_map = None
        self.update_id_map_and_set()
        self.ids_aovs = []

    def map_nodes_by_ids(self):
        id_nodes = {}

        for each in self.scene_ids:
            id_nodes[str(each)] = []

        for mesh in pm.ls(type='mesh'):
            mesh_id = mesh.rsObjectId.get()
            id_nodes[str(mesh_id)].append(mesh)

        return id_nodes

    def validate_sequence_of_ids(self):
        self.update_id_map_and_set()
        _sorted_ids = sorted(self.scene_ids)
        _length = len(_sorted_ids)

        if 1 in self.scene_ids:
            pass
        else:
            return False

        for index, each in enumerate(_sorted_ids):
            if index + 1 != _length:
                if each + 1 != _sorted_ids[index + 1]:
                    return False
                elif each + 1 == _sorted_ids[index + 1]:
                    continue
            return True

    def select_by_ids(self, id_value):
        mesh_shapes = self.ids_map[str(id_value)]
        transforms = []
        for mesh in mesh_shapes:
            transforms.append(mesh.getParent())
        pm.select(transforms)

    def assign_id(self, list_of_nodes, id_value):
        for each in list_of_nodes:
            each.rsObjectId.set(id_value)
        self.update_id_map_and_set()

    def update_id_map_and_set(self):
        self.scene_ids = self.set_of_ids()
        self.ids_map = self.map_nodes_by_ids()

    def delete_aovs(self):
        pm.delete(self.ids_aovs)

    @staticmethod
    def set_of_ids():
        ids = set()

        for mesh in pm.ls(type='mesh'):
            try:
                ids.add(mesh.rsObjectId.get())
            except:
                pm.warning('{} has no shape or is not a geometry'.format(mesh))
        return ids

    @staticmethod
    def new_aov(name, id_object):
        node = pm.createNode('RedshiftAOV', name=name)
        node.aovType.set('Puzzle Matte')
        node.filePrefix.set('<BeautyPath>/<BeautyFile>.<RenderPass>')
        node.fileFormat.set(1)
        node.dataType.set(1)
        node.setAttr('name', name)
        node.addAttr('mode', at='enum', enumName='Material ID=0:Object ID=1', defaultValue=1)
        node.addAttr('redId', at='long', minValue=1, maxValue=30, defaultValue=id_object['red'])
        node.addAttr('greenId', at='long', minValue=1, maxValue=30, defaultValue=id_object['green'])
        node.addAttr('blueId', at='long', minValue=1, maxValue=30, defaultValue=id_object['blue'])
        node.addAttr('enableReflectionRefraction', type='bool')
        return node

    @staticmethod
    def create_aovs(name, id_list):
        node = pm.createNode('RedshiftAOV', name=name)
        node.aovType.set('Puzzle Matte')
        node.filePrefix.set('<BeautyPath>/<BeautyFile>.<RenderPass>')
        node.fileFormat.set(1)
        node.dataType.set(1)
        node.setAttr('name', name)
        node.addAttr('mode', at='enum', enumName='Material ID=0:Object ID=1', defaultValue=1)
        node.addAttr('redId', at='long', minValue=1, maxValue=48, defaultValue=id_list[0])
        node.addAttr('greenId', at='long', minValue=1, maxValue=48, defaultValue=id_list[1])
        node.addAttr('blueId', at='long', minValue=1, maxValue=48, defaultValue=id_list[2])
        node.addAttr('enableReflectionRefraction', type='bool')
        return node
