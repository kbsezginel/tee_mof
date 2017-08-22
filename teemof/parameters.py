"""
Parameters for reading and plotting thermal flux
"""

k_parameters = dict(kb=0.001987,
                    conv=69443.84,
                    dt=5,
                    volume=80 * 80 * 80,
                    temp=300,
                    prefix='J0Jt_t',
                    isotropic=True,
                    average=True,
                    traj='traj.xyz',
                    read_info=False,
                    read_thermo=False)

plot_parameters = {
    'k': dict(limit=(0, 2000),
              size=(5, 3),
              fontsize=8,
              lw=1.5,
              dpi=200,
              avg=True,
              cmap='Spectral_r',
              save=None,
              legendloc=(1.02, 0),
              ncol=1,
              title=None,
              xlabel='Time',
              ylabel='k (W/mK)'),
    'thermo': dict(size=(20, 10),
                   dpi=200,
                   save=None,
                   title=None,
                   fontsize=8,
                   scilimits=(-4, 4),
                   subplots_adjust=(0.3, 0.25),
                   xlabel='Timesteps',
                   fix=['NVT', 'NVE1'],
                   colors=dict(NVT='r', NVE1='g', NVE2='b'),
                   variable=['temp', 'e_pair', 'tot_eng', 'e_mol', 'press'],
                   fig_height=3),
    'k_sub': dict(limit=(0, 10000),
                  size=(20, 6),
                  dpi=200,
                  subplot=(2, 5),
                  subplots_adjust=(.4, .3),
                  fontsize=9,
                  lw=2.5,
                  k_est=True,
                  k_est_color='r',
                  k_est_loc=(5, 0.1),
                  k_est_t0=5,
                  k_est_t1=10,
                  ylim=(0, 1.2),
                  save=None,
                  xlabel='Time',
                  ylabel='k (W/mK)'),
    'f_dist': dict(subplot=(2, 5),
                   size=(14, 6),
                   dpi=200,
                   space=(0.2, 0.1),
                   grid_size=10,
                   bin_size=1.5,
                   vmax=40,
                   vmin=1.1,
                   cmap='YlOrRd',
                   grid_limit=10,
                   ticks=False,
                   cbar=[0.92, 0.135, 0.02, 0.755],
                   save=None,
                   selections=None,
                   traj='traj.xyz',
                   traj_start=0,
                   traj_end=1e6)
}
