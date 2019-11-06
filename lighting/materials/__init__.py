import pymel.core as pm
import re


def get_source_sets(node):
    return node.listSets(
        extendToShape=1,
        type=1)


def get_members(set_node):
    return set_node.members()


def remove_third_value(list_of_string_indexes):
    new_list = []
    splitted_indexes = list_of_string_indexes.splitlines()
    for each in splitted_indexes:
        splitted_string = each.split(":")
        
        if len(splitted_string) == 1:
            new_list.append("{0}".format(splitted_string[0]))
        elif len(splitted_string) > 1:
            new_list.append("{0}:{1}".format(splitted_string[0], splitted_string[1]))
        
    return new_list 


def reciprocal_faces(mesh_faces_node, target_shape_long_name):
    str_faces=re.search(r"\..*", mesh_faces_node.name()).group()
    list_of_indexes=re.search(
        r"(?<=\[).*(?=\])", str_faces).group().split(",")

    separated_values = []
    for each in list_of_indexes:
        list_of_splitted_indexes = remove_third_value(each)
        for index_range in list_of_splitted_indexes:
            separated_values.append(index_range)


    list_of_faces_plus_indexes=[]
    for index in separated_values:
        list_of_faces_plus_indexes.append("{0}.f[{1}]".format(
            target_shape_long_name, index))



    return list_of_faces_plus_indexes


def is_mesh(node):
    if type(node) == pm.nodetypes.Mesh:
        return True
    else:
        return False


def create_SG_node_and_members_dictionary(list_of_SG_nodes):
    SG_nodes_and_members_dictionary={}
    for i, each in enumerate(list_of_SG_nodes, 1):
        SG_nodes_and_members_dictionary["SG_" + str(i)]={
            "sg_node": each,
            "members": get_members(each)
        }
    return SG_nodes_and_members_dictionary


def transfer(source, target):
    '''
        Transfer materials from source
        to target
    '''

    target_shape=target.getShape()
    target_shape_long_name=target_shape.longName()
    source_SG_nodes=get_source_sets(source)
    sources_dict=create_SG_node_and_members_dictionary(source_SG_nodes)

    for each in sources_dict.values():
        SG_node=each['sg_node']
        for node in each["members"]:

            if is_mesh(node):
                pm.sets(
                    SG_node, forceElement=target_shape)

            else:
                list_of_faces = reciprocal_faces(node, target_shape_long_name)
                for each in list_of_faces:
                    pm.sets(
                        SG_node, forceElement=each)
