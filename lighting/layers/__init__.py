import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup


class Layers():
    def __init__(self):
        self.layer_dict = {
            'layer': None,
            'collection': None
        }

    def create(self, name):
        rs = renderSetup.instance()
        layer = rs.createRenderLayer(
            name + "_RYR")
        collection = layer.createCollection(
            name + "_COL")

        self.layer_dict["layer"] = layer
        self.layer_dict["collection"] = collection
        return self.layer_dict

    def create_shader_override(self, collection, material, name):
        collection.createOverride(name, 'shaderOverride')
        collection.getCollections()[0].getOverrides()[0].setShader(material)

    def add_objects_to_collection(self, collection, list_of_objects):
        selector = collection.getSelector()
        long_names_list = []
        for each in list_of_objects:
            long_names_list.append(each.longName())

        selector.staticSelection.add(long_names_list)
