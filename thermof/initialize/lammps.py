# Date: September 2017
# Author: Kutay B. Sezginel
"""
Initialize Lammps simulation using lammps_interface
"""
import os
import glob
from lammps_interface.lammps_main import LammpsSimulation
from lammps_interface.structure_data import from_CIF
from . import read_lines, write_lines
from thermof.sample import lammps_input
from thermof.parameters import Parameters


def write_lammps_files(simdir, parameters, verbose=True):
    """
    Write Lammps files using lammps_interface.

    Args:
        - simdir (str): Directory to write Lammps simulation files
        - parameters (Parameters): Lammps simulation parameters

    Returns:
        - None: Writes Lammps simulation files to simulation directory
    """
    print('I. Writing Lammps input and data files...') if verbose else None
    lammpspar = Parameters(parameters.lammps)
    sim = LammpsSimulation(lammpspar)
    cell, graph = from_CIF(lammpspar.cif_file)
    sim.set_cell(cell)
    sim.set_graph(graph)
    sim.split_graph()
    sim.assign_force_fields()
    sim.compute_simulation_size()
    sim.merge_graphs()
    sim.write_lammps_files(simdir)


def write_lammps_input(simdir, parameters, lammps_input=lammps_input, verbose=True):
    """
    Write Lammps simulation input file.

    Args:
        - simdir (str): Directory to write Lammps input file
        - parameters (Parameters): Lammps simulation parameters

    Returns:
        - None: Rewrites Lammps simulation input file to simulation directory
    """
    simpar = parameters.thermof
    inp_file = glob.glob(os.path.join(simdir, 'in.*'))[0]
    print('II. Updating Lammps input file -> %s' % inp_file) if verbose else None
    input_lines = read_lines(inp_file)
    data_file = glob.glob(os.path.join(simdir, 'data.*'))[0]
    simpar['atom_list'] = get_atom_list(data_file)
    simpar_lines = get_simpar_lines(simpar, simpar_file=lammps_input['simpar'])
    input_lines += '\n'
    input_lines += simpar_lines
    print('Adding fixes: %s' % ' | '.join(simpar['fix'])) if verbose else None
    for fix in simpar['fix']:
        fix_lines = get_fix_lines(fix, simpar, lammps_input=lammps_input)
        input_lines += '\n'
        input_lines += fix_lines
    write_lines(inp_file, input_lines)
    print('Updating simulation parameters...') if verbose else None
    parameters.thermof['kpar']['log_file'] = 'log.%s' % parameters.thermof['mof']['name']
    parameters.thermof['kpar']['fix'] = None
    parameters.thermof['kpar']['temp'] = parameters.thermof['temperature']
    parameters.thermof['kpar']['thermo_style'] = parameters.thermof['thermo_style']


def get_fix_lines(fix, simpar, lammps_input=lammps_input):
    """
    Get lines for selected fix.
    """
    if fix == 'NPT':
        fix_lines = get_npt_lines(simpar, npt_file=lammps_input['npt'])
    elif fix == 'NVE':
        fix_lines = get_nve_lines(simpar, nve_file=lammps_input['nve'])
    elif fix == 'NVT':
        fix_lines = get_nvt_lines(simpar, nvt_file=lammps_input['nvt'])
    elif fix == 'MIN':
        fix_lines = get_min_lines(simpar, min_file=lammps_input['min'])
    elif fix == 'TC':
        fix_lines = get_tc_lines(simpar, tc_file=lammps_input['thermal_conductivity'])
    elif fix == 'THEXP':
        fix_lines = get_thexp_lines(simpar, thexp_file=lammps_input['thermal_expansion'])
    elif fix == 'NVE_ANGLE':
        fix_lines = get_nve_improved_angle_lines(simpar, nve_file=lammps_input['nve_improved_angle'])
    return fix_lines


def get_simpar_lines(simpar, simpar_file=lammps_input['simpar']):
    """
    Get input lines for Lammps simulation parameters using thermof_parameters.
    """
    simpar_lines = read_lines(simpar_file)
    simpar_lines[1] = 'variable        T equal %i\n' % simpar['temperature']
    simpar_lines[2] = 'variable        dt equal %.1f\n' % simpar['dt']
    simpar_lines[3] = 'variable        seed equal %i\n' % simpar['seed']
    simpar_lines[4] = 'variable        p equal %i\n' % simpar['correlation_length']
    simpar_lines[5] = 'variable        s equal %i\n' % simpar['sample_interval']
    simpar_lines[12] = 'thermo          %i\n' % simpar['thermo']
    simpar_lines[13] = 'thermo_style    custom %s\n' % ' '.join(simpar['thermo_style'])
    if simpar['dump_xyz'] != 0:
        simpar_lines[7] = 'variable        txyz equal %i\n' % simpar['dump_xyz']
        simpar_lines[9] = 'dump_modify     1 element %s\n' % ' '.join(simpar['atom_list'])
    else:
        del simpar_lines[7:10]
    return simpar_lines


def get_npt_lines(simpar, npt_file=lammps_input['npt']):
    """
    Get input lines for NPT simulation using thermof_parameters.
    """
    npt_lines = read_lines(npt_file)
    npt_lines[1] = 'variable        pdamp      equal %i*${dt}\n' % simpar['npt']['pdamp']
    npt_lines[2] = 'variable        tdamp      equal %i*${dt}\n' % simpar['npt']['tdamp']
    npt_lines[4] = 'run             %i\n' % simpar['npt']['steps']
    if simpar['npt']['restart']:
        npt_lines.append('write_restart   restart.npt\n')
    return npt_lines


def get_nvt_lines(simpar, nvt_file=lammps_input['nvt']):
    """
    Get input lines for NVT simulation using thermof_parameters.
    """
    nvt_lines = read_lines(nvt_file)
    nvt_lines[2] = 'run             %i\n' % simpar['nvt']['steps']
    if simpar['nvt']['restart']:
        nvt_lines.append('write_restart   restart.nvt\n')
    return nvt_lines


def get_nve_lines(simpar, nve_file=lammps_input['nve']):
    """
    Get input lines for NVE simulation (including thermal conductivity calc.) using thermof_parameters.
    """
    nve_lines = read_lines(nve_file)
    if simpar['nve']['equilibration'] >= 0:
        nve_lines[2] = 'run             %i\n' % simpar['nve']['equilibration']
    else:
        nve_lines = nve_lines[4:]
    nve_lines[42] = 'run             %i\n' % simpar['nve']['steps']
    if simpar['nve']['restart']:
        nve_lines.append('write_restart   restart.nve\n')
    return nve_lines


def get_nve_improved_angle_lines(simpar, nve_file=lammps_input['nve_improved_angle']):
    """
    Get input lines for NVE simulation (including thermal conductivity calc.) using thermof_parameters.
    """
    nve_lines = read_lines(nve_file)
    if simpar['nve']['equilibration'] >= 0:
        nve_lines[2] = 'run             %i\n' % simpar['nve']['equilibration']
    else:
        nve_lines = nve_lines[4:]
    nve_lines[29] = 'run             %i\n' % simpar['nve']['steps']
    if simpar['nve']['restart']:
        nve_lines.append('write_restart   restart.nve\n')
    return nve_lines


def get_min_lines(simpar, min_file=lammps_input['min']):
    """
    Get input lines for minimization using thermof_parameters.
    """
    mof = simpar['mof']['name']
    min_lines = read_lines(min_file)
    min_lines[2] = 'print           "MinStep,CellMinStep,AtomMinStep,FinalStep,Energy,EDiff" file %s.min.csv screen no\n' % mof
    min_lines[3] = 'variable        min_eval   equal %.1e\n' % simpar['min']['edif']
    min_lines[9] = 'minimize        %.1e %.1e %i %i\n' % (simpar['min']['etol'], simpar['min']['ftol'], simpar['min']['maxiter'], simpar['min']['maxeval'])
    min_lines[14] = 'minimize        %.1e %.1e %i %i\n' % (simpar['min']['etol'], simpar['min']['ftol'], simpar['min']['maxiter'], simpar['min']['maxeval'])
    min_lines[18] = 'print           "${iter},${CellMinStep},${AtomMinStep},${AtomMinStep},$(pe),${min_E}" append %s.min.csv screen no\n' % mof
    if simpar['min']['restart']:
        nve_lines.append('write_restart   restart.min\n')
    return min_lines


def get_tc_lines(simpar, tc_file=lammps_input['thermal_conductivity']):
    """
    Get thermal conductivity calculation Lammps input lines

    Args:
        - parameters (Parameters): Lammps parameters (see thermof.parameters)
        - tc_file (str): Sample thermal conductivity Lammps input file

    Returns:
        - list: List of Lammps input lines for thermal conductivity calculations
    """
    tc_lines = read_lines(tc_file)
    tc_lines[1] = 'variable        T equal %.1f\n' % simpar['temperature']
    tc_lines[2] = 'variable        dt equal %.1f\n' % simpar['dt']
    tc_lines[3] = 'variable        seed equal %i\n' % simpar['seed']
    return tc_lines


def get_thexp_lines(simpar, thexp_file=lammps_input['thermal_expansion']):
    """
    Get thermal expansion calculation Lammps input lines

    Args:
        - parameters (Parameters): Lammps parameters (see thermof.parameters)
        - thexp_file (str): Sample thermal expansion Lammps input file

    Returns:
        - list: List of Lammps input lines for thermal expansion calculation
    """
    thexp_lines = read_lines(thexp_file)
    thexp_lines[1] = 'variable        pdamp      equal %i*${dt}\n' % simpar['thexp']['pdamp']
    thexp_lines[2] = 'variable        tdamp      equal %i*${dt}\n' % simpar['thexp']['tdamp']
    thexp_lines[4] = 'fix             thexp all print %i "$(step),$(vol),$(enthalpy)" file %s screen no title "Step,Volume,Enthalpy"\n' % (simpar['thexp']['print'], simpar['thexp']['file'])
    thexp_lines[5] = 'run             %i\n' % simpar['thexp']['steps']
    return thexp_lines


def get_atom_list(data_file):
    """
    Reads list of atoms from the data file created by lammps_interface for dump_modify command.
    """
    with open(data_file, 'r') as ld:
        ld_lines = ld.readlines()
    atom_lines = ld_lines[ld_lines.index('Masses\n') + 2:ld_lines.index('Bond Coeffs\n') - 1]
    atoms = [line.split()[3][:2].replace('_', '') for line in atom_lines]
    return atoms
