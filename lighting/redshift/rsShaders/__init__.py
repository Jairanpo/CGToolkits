
import pymel.core as pm

import lighting.shaders as shd

def create_with_redshift_sprite(shader_type, shader_name):
    shader, shading_group = shd.create_shader(shader_type, shader_name, connect=False)

    sprite = pm.shadingNode('RedshiftSprite', name=shader_name + '_rsSprite', asShader=True)

    shader.connectAttr('outColor', sprite.input)
    sprite.connectAttr('outColor', shading_group.surfaceShader)

    return shader, shading_group, sprite