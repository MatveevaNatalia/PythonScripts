# This script prepares the input files for my numerical simulations
# and runs the simulations on the claster 


import numpy as np
import os, subprocess
import time

ncomp = 2
npar = 5

VMC_init_copy = 0 # if 1 copies in2Dprev.dat from VMC folder to DMC folder

i_OBDM = 0


#name_main_folder= 'Nc_2_Np_20'
name_main_folder= 'Nc_' + str(ncomp) + '_Np_' + str(npar)
#name_file_opt = 'param_Nc_2_Np_20.txt'
name_file_opt = 'param_Nc_'+str(ncomp)+'_Np_'+str(npar)+'.txt'

pow_max = 5
param_opt = [0]*pow_max
temp = 0
f = open(name_file_opt,'r')
for i in range (0,pow_max):
    ll = (f.readline()).split()
    param_opt[i] = ll[1]
    print("{0} {1}\n".format(i, param_opt[i]))
ll = (f.readline()).split()
a_min = float(ll[1])
ll = (f.readline()).split()
a_max = float(ll[1])
ll = (f.readline()).split()
na = int(ll[1])
ll = (f.readline()).split()
dt_VMC = ll[1]
ll = (f.readline()).split()
dt_DMC = ll[1]

f.close()

print(" a_min={0} a_max={1} na={2} dt_VMC={3}".format(a_min, a_max, na, dt_VMC))

a_list = [0]*(na+1)
da = (a_max-a_min)/na
for i in range(0,na+1):
        a_list[i] = a_min + i*da
        print i, a_list[i]



i_param = 1 # if 1 writes param.dat file

#----------------------------------------------------------------#
param_list=['i_VMC', 1,
            'i_FNDMC', 0,
            'ncomp', ncomp,
            'np', npar,
            'width', 0.0,
            'aB', 0.0,
            'a', 0.0,
            'dt', dt_VMC,
            'niter', 10000,
            'nblck', 1,
            'npop', 100,
            'init', 1,
            'nwrite', 1000,
            'icrit', 100,
            'i_OBDM', i_OBDM,
            'mgr_g(r)', 200,
            'mgr_OBDM', 200,
            'mgr_dens', 200,
            'Lmax_gr', 6.0,
            'Lmax_OBDM', 3.0,
            'Lmax_dens', 3.0,
            'numks', 200,
            'kmax', 4.0,
            'Lmax_McM', 4.0]
#-------------------------------------------------------------#
def Opt_fun(param_opt, x):
    return float(param_opt[0]) + float(param_opt[1])*x + float(param_opt[2])*x*x + float(param_opt[3])*x*x*x + float(param_opt[4])*x*x*x*x

def write_param(param_list, a, b):
    param_list[9]=b
    param_list[13]=a
    f=open('Data/param.dat','w')
    ll=len(param_list)
    for i in range(0,ll,2):
            f.write("{0} {1}\n".format(param_list[i], param_list[i+1]))
            #print("{0} {1}\n".format(param_list[i], param_list[i+1]))
    f.close()
    return
#-------------------------------------------------------------#



#------------------------------------------------------------#

if not os.path.exists(name_main_folder):
    os.mkdir(name_main_folder)
os.chdir(name_main_folder)

for a in a_list:
    name_folder_a = 'a_m_'+str(abs(a))
    if not os.path.exists(name_folder_a):
        os.mkdir(name_folder_a)
    os.chdir(name_folder_a)

    if not os.path.exists('VMC'):
        os.mkdir('VMC')
    os.chdir('VMC')

    os.system('cp ../../../qmc.pbs ./qmc.pbs')

    if not os.path.exists('Data'):
        os.mkdir('Data')

    gamma = Opt_fun(param_opt, a)

    write_param(param_list, a, gamma)

    if not os.path.exists('Measur'):
        os.mkdir('Measur')

    subprocess.Popen("qsub qmc.pbs", shell=True)
    #subprocess.Popen("nohup nice -10 ../../../QMC &", shell=True)
    #time.sleep(3)

    os.chdir('../../')





