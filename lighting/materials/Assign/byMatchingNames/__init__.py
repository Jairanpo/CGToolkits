import pymel.core as pm

####################################################################################
## Format agent sources material names 
CHARACTER = "Tanya"

def name_material(name, node):
    # Get object material
    shape = node.getShape()
    sets_it_belongs = shape.listSets()
    SG_node = None
    for each in sets_it_belongs:
        if each.type() == "shadingEngine":
            SG_node = each
    
    material = None
    for each in SG_node.listConnections():
        if each.type() == "RedshiftMaterial":
            material = each
            
    material.rename("{0}_{1}_SHD".format(name, node.name()))
    
for each in pm.ls(sl=True):
    name_material(CHARACTER, each)
    
#######################################################################################
## Rename Geometry
    
def name_xform_from_shape(node):
    shape = node.getShape()
    node.rename(shape.name().replace("SHP", "GEO"))
    
for each in pm.ls(sl=True, type="transform"):
    name_xform_from_shape(each)
    
########################################################################################
## Assign Materials
materials = pm.ls(type="RedshiftMaterial")

for each in materials:
    SG_Node = pm.createNode("shadingEngine", name = each.name().replace("SHD","SGN"))
    each.connectAttr("outColor", SG_Node.surfaceShader)
    base_name = each.name().replace("_SHD", "_GEO")
    x_form = pm.ls('*{0}*'.format(base_name), type="transform")[0]
    shape = x_form.getShape()
    shape.disconnectAttr("instObjGroups")
    shape.connectAttr("instObjGroups", SG_Node.dagSetMembers[0])
    
    
    
    
    
    
    
    
    
    
    
    
    
    