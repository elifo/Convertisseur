# -*- mode: perl -*-

# job fname
run_name  = "DENEMELER";

# duration of the run
sim_time  = 0.3 ;

# input mesh file
mesh_file = "mesh4spec";
mat_file  = "material.input";

# dimension
dim = 3;

# Description des capteurs
save_traces   = true;
traces_format = hdf5;

capteurs "SC3D" {
    type   = points;
    file   = "stations.txt";
    period = 1;
};

# snapshots
snapshots {
    save_snap     = false;
    snap_interval = 1;
    select all;
};

# Nonlinear
nonlinear = 0;

# Fichier protection reprise
prorep       = false;
prorep_iter  = 100000;
restart_iter = 000000;

# introduce a source

#extended fault source
extended_source {
    # Moment or Force
    is_force = 1; 
    # Kinematic rupture file
    kine_file = "XXX";
    # Moment History (moment VS temps)
    slip_file = "XXX";
};


#source {
#     coords = 0.0 0.0 0.0;
#     type = impulse;
#     dir = 0. -1. 0.;
#     func = dm ;
#     Q = 6250.0;
#     Y = 2.0;
#     X = 0.7158;
#     L = 3.0;
#     v = 90.0;
#     d = 0.6;
#     a = 3.0;
#     tau = 0.0016666666666666666;
#};



time_scheme {
    accel_scheme = false;  # Acceleration scheme for Newmark
    veloc_scheme = true;   # Velocity scheme for Newmark
    alpha = 0.5;           # alpha (Newmark parameter)
    beta =  0.5;           # beta (Newmark parameter)
    gamma = 1;             # gamma (Newmark parameter)
    courant = 0.3;
};

out_variables {
    dis  = 1 ;
    vel  = 1 ;
    acc  = 1 ;
    pre  = 0 ;
};
