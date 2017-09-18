"""
Sample input files for predicting thermal conductivity of porous crystals using Lammps
"""
import os
from thermof import Simulation, Trajectory
from thermof.parameters import k_parameters


sample_dir = os.path.abspath(os.path.dirname(__file__))
# Lammps input file with thermal flux measured in single direction
single_inp_path = os.path.join(sample_dir, 'in_single.cond.sample')        # Single MOF
# Lammps input file with thermal flux measured in three directions
single_inp3_path = os.path.join(sample_dir, 'in3_single.cond.sample')      # Single MOF
ipmof_inp3_path = os.path.join(sample_dir, 'in3_ipmof.cond.sample')        # Interpenetrated MOF
thermal_flux_file = os.path.join(sample_dir, 'in.thermal_flux')            # Thermal flux calculation
# Lammps structure files
single_data_path = os.path.join(sample_dir, 'lammps_single.data.sample')   # Single MOF
ipmof_data_path = os.path.join(sample_dir, 'lammps_ipmof.data.sample')     # Interpenetrated MOF
# Job submission file for Frank
qsub_path = os.path.join(sample_dir, 'lammps_qsub.sh.sample')

samples = dict(ideal_mof=dict(inp=single_inp3_path, data=single_data_path, qsub=qsub_path),
               ideal_interpenetrated_mof=dict(inp=ipmof_inp3_path, data=ipmof_data_path, qsub=qsub_path))


tests_dir = os.path.join(sample_dir, '..', '..', 'tests')


def load_sample_simulation(mof='single', setup='run', tests_dir=tests_dir, parameters=k_parameters.copy()):
    """ Load a sample simulation object from the tests directory """
    if mof == 'single':
        trial = os.path.join(tests_dir, 'ideal-mof-trial')
        if setup == 'run':
            sample_simulation = Simulation(read=os.path.join(trial, 'Run1'), setup='run', parameters=parameters)
        elif setup == 'trial':
            sample_simulation = Simulation(read=trial, setup='trial', parameters=parameters)
    else:
        trial = os.path.join(tests_dir, 'ip-mof-trial')
        if setup == 'run':
            sample_simulation = Simulation(read=os.path.join(trial, 'Run1'), setup='run', parameters=parameters)
        elif setup == 'trial':
            sample_simulation = Simulation(read=trial, setup='trial', parameters=parameters)
    return sample_simulation


def load_sample_trajectory(mof='single', tests_dir=tests_dir):
    """ Load a sample trajectory file from tests directory """
    if mof == 'single':
        sample_traj = Trajectory(read=os.path.join(tests_dir, 'ideal-mof-trial', 'Run1', 'traj.xyz'))
    else:
        sample_traj = Trajectory(read=os.path.join(tests_dir, 'ip-mof-trial', 'Run1', 'traj.xyz'))
    return sample_traj
