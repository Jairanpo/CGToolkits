import pymel.core as pm


class MatteParams:

    def __init__(self):
        pass

    def create_matteParam_node(self, name):
        return pm.createNode('RedshiftMatteParameters', name=name)

    def send_nodes_inside_matteParam(self, name, list_of_nodes):
        matteParam_node = self.create_matteParam_node(name)
        for node in list_of_nodes:
            pm.sets(matteParam_node, forceElement=node)