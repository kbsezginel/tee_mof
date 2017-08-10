# Thermoelectrically Entangled MOFs (tee_mof)
Investigating effect of interpenetration on the thermal conductivity of metal-organic frameworks

![alt text][Fig1]

- a) Idealized porous crystal (8 × 8 × 8 cubic unit cells), single unit cell highlighted in red
- b) Bonding arrangement for single unit cell using Morse potential (red bonds are modeled stronger than blue bonds)
- c) Doubly interpenetrated unit cells with framework depicted as red and blue (initial frameworks in each simulation are 5 Å apart in each dimension
- d) Interpenetrated idealized porous crystal (8 × 8 × 8 cubic unit cells).

## Installation

Clone the repository, enter the main repository directory and run:

`python setup.py install`

## Usage
teemof library can be used to initialize, run, and analyze simulation results to investigate thermal transport in porous crytals. Here sample files for an idealized cubic MOF along with an interpenetrated version are provided (see Figure 1). Using these files Molecular Dynamics simulations can be run with [Lammps].

### Sample
Sample [Lammps] input files for thermal conductivity calculations can be found in *~/sample*

- in3_ipmof.cond.sample: Interpenetrated MOF simulation parameters with 3D thermal flux
- in3_single.cond.sample: Single MOF simulation parameters with 3D thermal flux
- in_ipmof.cond.sample: Interpenetrated MOF simulation parameters with 1D thermal flux
- lammps_ipmof.data.sample: Interpenetrated MOF structure file
- lammps_ipmof_metal.data.sample: Interpenetrated MOF with differemt corner atoms structure file
- lammps_single.data.sample: Single MOF structure file
- lammps_single_metal.data.sample: Single MOF with differemt corner atoms structure file
- lammps_qsub.sh.sample: Job submission script for lammps simulations on [Frank] 

### Notebooks
Example jupyter notebooks can be found in *~/notebooks*

- change_trajectory: Change xyz trajectory atoms names
- initialize: Initialize lammps simulation files according to selected simulation parameters
- interpenetrate: Create interpenetrated structure
- read_kt: Read thermal conductivity from simulation results
- read_thermo: Read thermodynamic data from simulation results


[Fig1]: https://github.com/kbsezginel/tee_mof/blob/master/docs/Fig1.png "Structures"
[Lammps]: http://lammps.sandia.gov/ "Lammps home page"
[Frank]: http://core.sam.pitt.edu/frank "Frank home page"