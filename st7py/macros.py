import os
import ctypes
import numpy as np
from St7API import *
from st7py.core import *


def get_coord(uid, node):
    """gets XYZ coordinates at node id"""
    coord = (ctypes.c_double*3)()
    chkErr(St7GetNodeXYZ(uid, int(node), coord))
    return coord[:]


def set_coord(uid,node,value):
    """sets XYZ coordinates to node id"""
    coord = (ctypes.c_double*3)()
    coord[:] = value
    chkErr(St7SetNodeXYZ(uid, node, coord))


def get_beam_material(uid,propnum):
    """gets beam material property data and returns as array of doubles"""
    data = (ctypes.c_double*9)()
    chkErr(St7GetBeamMaterialData(uid,propnum,data))
    return data


def set_beam_material(uid, propnum, value, propname='modulus'):
    """sets a beam material data for propnum. defaults to elastic modulus"""
    data = (ctypes.c_double*9)()
    chkErr(St7GetBeamMaterialData(uid,propnum,data))
    data[beamMaterialData[propname]] = value
    chkErr(St7SetBeamMaterialData(uid,propnum,data))


def set_plate_thickness(uid, propnum, value, disp=False):
    """
    sets plate thickness. if single value given, function assumes membbrane and
    bending thicknesses are the same and broadcasts the value given.
    that is:
        value = 8 -> assigns membrane and bending thickness to 8
        value = [8,4] -> assigns membrane thickness to 8 and bending to 4
    """
    if not isinstance(value,list): value=[value,value]
    data = (ctypes.c_double*2)()
    chkErr(St7GetPlateThickness(uid, propnum, data))
    if disp: print('({}) old thickness: {}'.format(uid,data[:]))
    data[:] = value
    chkErr(St7SetPlateThickness(uid, propnum, data))
    if disp: print('({}) new thickness: {}'.format(uid,data[:]))


def set_plate_material_iso(uid, propnum, value, propname='modulus'):
    """sets desired material data to isotropic plate. defaults to modulus"""
    data = (ctypes.c_double*8)()
    chkErr(St7GetPlateIsotropicMaterial(uid, propnum, data))
    data[plateIsoMaterialData[propname]] = value
    chkErr(St7SetPlateIsotropicMaterial(uid, propnum, data))


def set_plate_material_ortho(uid, propnum, value, propname='modulus1'):
    """sets desired material data to orthotropic plate. defaults to modulus1"""
    data = (ctypes.c_double*18)()
    chkErr(St7GetPlateOrthotropicMaterial(uid, propnum, data))
    data[plateOrthoMaterialData[propname]] = value
    chkErr(St7SetPlateOrthotropicMaterial(uid, propnum, data))


def get_node_stiffness(uid=1,node=1,fcase=1):
    trans = (ctypes.c_double*3)()
    rot = (ctypes.c_double*3)()
    ucs = ctypes.c_long(1)
    # don't wrap in chkErr - throws error code 10 if no restraint originally assigned (so stupid)
    St7GetNodeKTranslation3F(uid, node, fcase, ucs, trans)
    St7GetNodeKRotation3F(uid, node, fcase, ucs, rot)
    return np.hstack((trans, rot))


def set_node_stiffness(uid=1,node=1,fcase=1,value=[0,0,0,0,0,0],disp=False):
    # get original node stiffness (for correct data type). do this directly instead of calling get_node_stiffness function bc it returns as np.hstacked
    kt = (ctypes.c_double*3)()
    kr = (ctypes.c_double*3)()
    ucs = ctypes.c_long(1)
    St7GetNodeKTranslation3F(uid, node, fcase, ucs, kt)
    St7GetNodeKRotation3F(uid, node, fcase, ucs, kr)
    if disp: print('Model-ID {} : Node {} : Original Stiffness {}'.format(uid,node,np.hstack((kt,kr))))
    #k = get_node_stiffness(uid,node,fcase)
    kt[:] = value[:3]
    kr[:] = value[3:]
    chkErr(St7SetNodeKTranslation3F(uid, node, fcase, ucs, kt))
    chkErr(St7SetNodeKRotation3F(uid, node, fcase, ucs, kr))
    if disp: print('Model-ID {} : Node {} : Updated Stiffness {}'.format(uid,node,np.hstack((kt,kr))))


def get_node_restraint(uid=1,node=1,fcase=1):
    restraint = (ctypes.c_long*6)()
    displacement = (ctypes.c_double*6)()
    # don't use chkErr wrapper to avoid throwing 'missing data' error 10
    St7GetNodeRestraint6(uid,node, fcase, ctypes.c_long(1), restraint, displacement)
    return restraint


def set_node_restraint(uid=1,node=1,fcase=1, value=[1,1,1,0,0,0]):
    # get current restraint and displacement on node for proper c data type
    restraint = get_node_restraint(uid,node,fcase)
    displacement = get_node_initial_displacement(uid, node, fcase)
    # replace values w/ those given
    restraint[:] = value
    chkErr(St7SetNodeRestraint6(uid, node, fcase, ctypes.c_long(1), restraint, displacement))


def get_node_initial_displacement(uid=1,node=1,fcase=1):
    restraint = (ctypes.c_long*6)()
    displacement = (ctypes.c_double*6)()
    # don't use chkErr wrapper to avoid throwing 'missing data' error 10
    St7GetNodeRestraint6(uid,node, fcase, ctypes.c_long(1), restraint, displacement)
    return displacement


def set_node_initial_displacement(uid=1,node=1,fcase=1, value=[1,1,1,0,0,0]):
    # get current restraint and displacement on node for proper c data type
    restraint = get_node_restraint(uid,node,fcase)
    displacement = get_node_initial_displacement(uid, node, fcase)
    # replace values w/ those given
    displacement[:] = value
    chkErr(St7SetNodeRestraint6(uid, node, fcase, ctypes.c_long(1), restraint, displacement))


def gen_result_name(base_name, uid,result_ext,log_ext):
    """
    adds *_<uid>* to model file name for nfa results and log files
    """
    result_file = os.path.splitext(base_name)[0] + '_{}'.format(uid) + result_ext.upper()
    log_file = os.path.splitext(base_name)[0] + '_{}'.format(uid) + log_ext.upper()
    return result_file, log_file


def scale_para(para,value):
    """
    returns scaled parameter based on value, scale type (log/linear), and base
    """
    if para['scale'] == 'log':
        x = para['base']*10**value
    elif para['scale'] == 'linear':
        x = para['base']*value
    return x
