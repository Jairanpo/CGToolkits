import lighting.layers as lyr
import lighting.redshift.rsShaders as shd

def create_redshift_shader_override_layer(
        name,
        shader_type,
        list_of_objects=None,
        sprite=False):
    
    
    layer = lyr.Layers() 

    layer_setup_object = {
        "shader":None,
        "sg":None,
        "layer":None,
        "collection":None,
        "sprite":None}

    shader = []

    layer_config = layer.create(name)

    if sprite:
        shader = shd.create_with_redshift_sprite(
            shader_type=shader_type,
            shader_name=name + '_' + shader_type)
        layer_setup_object["sprite"] = shader[2]
        layer.create_shader_override(layer_config['collection'], shader[2], name + '_override')
    else:
        shader = shd.create(
            shader_type=shader_type,
            shader_name=name + '_' + shader_type)
        layer.create_shader_override(layer_config['collection'], shader[0], name + '_override')

    layer_setup_object["shader"] = shader[0]
    layer_setup_object["sg"] = shader[1]
    layer_setup_object["layer"] = layer_config["layer"]
    layer_setup_object["collection"] = layer_config["collection"]

    if list_of_objects == None:
        return layer_setup_object
    else:
        layer.add_objects_to_collection(layer["collection"], list_of_objects)
        return layer_setup_object
