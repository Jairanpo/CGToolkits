import pymel.core as pm


def create(shader_type, shader_name, connect=True):
    shader = pm.shadingNode(
        shader_type,
        name=shader_name,
        asShader=True)

    shading_group = pm.sets(
        name=shader_name + '_SG',
        empty=True,
        renderable=True,
        noSurfaceShader=True)

    if connect:
        shader.connectAttr(
            'outColor',
            shading_group.surfaceShader)

    return shader, shading_group



