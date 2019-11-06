import pymel.core as pm

deletable_nodes = ['delete', 'Delete', 'Deletable', 'deletable', 'borrar', 'Borrar', 'Eliminar', 'eliminar']


def delete_unknown_nodes():
    unknown_nodes = pm.ls(type='unknown')
    pm.delete(unknown_nodes)


def delete_named_nodes():
    for each in deletable_nodes:
        pm.delete(pm.ls('*{}*'.format(each)))


def cleanup():
    delete_unknown_nodes()
    delete_named_nodes()
