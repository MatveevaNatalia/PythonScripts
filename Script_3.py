# This script prepares the files for my numerical simulation


import numpy as np
import os, subprocess
import shutil
import Input_uk_omegak as Inp

def func_write_param(npar, rs, nkact, beta):
    f=open('param.txt', 'w')
    f.write('np\n')
    f.write("{0}\n".format(npar))
    f.write('rs\n')
    f.write("{0}\n".format(rs))
    f.write('nkact\n')
    f.write("{0}\n".format(nkact))
    f.write('beta\n')
    f.write("{0}\n".format(beta))
    f.close()
    return

#---------------------------------------------------------------------#

def Potential(path, npar, rs, nkact):
    os.chdir( path )
    beta = 0.0
    func_write_param(npar,rs,nkact,beta)
    name='rs_'+str(rs)+'_np_'+str(npar)
    if not os.path.exists(name):
        os.mkdir(name)
    subprocess.call("./effpot") 
    path1=name+'/pot_sr.dat'
    path2=name+'/pot_lr.dat'
    shutil.move('fort.1', path1)
    shutil.move('fort.2', path2)
    os.chdir( '..' )
    return

#-----------------------------------------------------------------------#

def Jastrow_T_0(path, npar, rs, nkact):
    os.chdir( path )
    beta = 0.0
    func_write_param(npar,rs,nkact,beta)
    name='rs_'+str(rs)+'_np_'+str(npar)
    if not os.path.exists(name):
        os.mkdir(name)
    subprocess.call("./effpot") 
    path1=name+'/jast_sr.dat'
    path2=name+'/jast_lr.dat'
    shutil.move('fort.1', path1)
    shutil.move('fort.2', path2)
    os.chdir( '..' )
    return

#-----------------------------------------------------------------------#



def Jastrow_beta(path, npar, rs, nkact, beta_ref, i_rew, ratio_rew, string, kr_shels, num_beta, beta_cut):
    os.chdir( path )
    os.getcwd()
    if i_rew == 0:
        beta_list_tot = [beta_ref]
    if i_rew == 1:
        beta_list_tot = [beta_ref, beta_ref+beta_ref*ratio_rew, beta_ref-beta_ref*ratio_rew]
    for beta in beta_list_tot:
        func_write_param(npar,rs,nkact,beta)
        Inp.In_Uk_Omegak(kr_shells=kr_shels, rs=rs, npar=npar, beta=beta, num_beta=num_beta, string=string)
        name1='beta_'+str(beta)
        if not os.path.exists(name1):
            os.mkdir(name1)
        subprocess.call("./effpot")
        if string == "Jastrow":
            copy_jast_beta(name1)
        if string == "Omega":
            copy_omega(name1)
        if string == "Omega" and beta_ref >= beta_cut:
            omega_zeros(name1, kr_shels)
            
    os.chdir( '..' )
    return

#-----------------------------------------------------------------------#

def copy_jast_beta(name1):
    path1=name1+'/jast_sr_beta.dat'
    path2=name1+'/jast_lr_beta.dat'
    shutil.move('fort.1', path1)
    shutil.move('fort.2', path2)
    return

#-----------------------------------------------------------------------#

def copy_omega(name1):
    path1=name1+'/omega_sr.dat'
    path2=name1+'/omega_lr.dat'
    shutil.move('fort.1', path1)
    shutil.move('fort.2', path2)
    return

#-----------------------------------------------------------------------#

def omega_zeros(name1, kr_shels):
    path1=name1+'/omega_sr.dat'
    f=open(path1, 'w')
    num_shels = len(kr_shels)
    for i in range(num_shels):
        k = kr_shels[i]
        f.write("{0} {1} {2}\n".format(k, 0.0, 0.0))  
    f.close()
    return


#-----------------------------------------------------------------------#


def param_break_up(num_sr, nkact, norb_max):
    f=open('Break_up/param_break_up.dat', 'w')
    #f.write('np\n')
    f.write("{0} {1}\n".format('num_srJ', num_sr))
    f.write("{0} {1}\n".format('num_sr_omega', num_sr))
    f.write("{0} {1}\n".format('num_srPot', num_sr))
    f.write("{0} {1}\n".format('nkact_J', nkact))
    f.write("{0} {1}\n".format('nkact_omega', nkact))
    f.write("{0} {1}\n".format('nkact_Pot', nkact))   
    f.write("{0} {1}\n".format('norb_max', norb_max))
    f.close()
    return

#-----------------------------------------------------------------------#

def Break_up(rs, npar, beta, num_sr, nkact, norb_max):
#    os.chdir('../')
    name='rs_'+str(rs)+'_np_'+str(npar)+'_files'
    name_T_0='rs_'+str(rs)+'_np_'+str(npar)
    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)
#for beta in beta_list:
    name1='beta_'+str(beta)
    if not os.path.exists(name1):
        os.mkdir(name1)
    os.chdir(name1)
    if not os.path.exists('Break_up'):
        os.mkdir('Break_up')
    param_break_up(num_sr, nkact, norb_max)    
    path = '../../uk_T_0/'+name_T_0
    shutil.copy(path+'/jast_sr.dat','Break_up')
    shutil.copy(path+'/jast_lr.dat','Break_up')
    path = '../../pot_energy/'+name_T_0
    shutil.copy(path+'/pot_sr.dat','Break_up')
    shutil.copy(path+'/pot_lr.dat','Break_up')
    path1 = '../../uk_beta/beta_'+str(beta)
    shutil.copy(path1+'/jast_sr_beta.dat','Break_up')
    shutil.copy(path1+'/jast_lr_beta.dat','Break_up')
    path2='../../omegak_beta/beta_'+str(beta)
    shutil.copy(path2+'/omega_sr.dat','Break_up')
    shutil.copy(path2+'/omega_lr.dat','Break_up')
    os.chdir('..')
    return

#-----------------------------------------------------------------------#

def Reweight(rs, npar, beta_ref, ratio_rew):
    #os.chdir('../../')
    #os.chdir('../')
    retval = os.getcwd()
    print "Current working directory %s" % retval
    #name='rs_'+str(rs)+'_np_'+str(np)+'_files'
    #if not os.path.exists(name):
    #    os.mkdir(name)
    name ='beta_' + str(beta_ref)
    print  name
    os.chdir(name)
    retval = os.getcwd()
    print "Current working directory %s" % retval

    if not os.path.exists('Reweight'):
        os.mkdir('Reweight')
    os.chdir('Reweight')
    
    beta_list = [beta_ref + beta_ref*ratio_rew, beta_ref - beta_ref*ratio_rew ]
    
    f=open('param_rew.dat', 'w')
    f.write ('beta_values ',)
    for beta in beta_list:
        f.write(str(beta))
        f.write(" ")
    f.write ("\n")    
    for beta in beta_list:
        f.write ('beta_'+str(beta))
        f.write("\n")
    f.close()

    for beta in beta_list:
        name1='beta_'+str(beta)
        if not os.path.exists(name1):
            os.mkdir(name1)
        retval = os.getcwd()
        print "Current working directory %s" % retval
        path1 = '../../../uk_beta/beta_'+str(beta)
        shutil.copy(path1+'/jast_sr_beta.dat', name1)
        shutil.copy(path1+'/jast_lr_beta.dat', name1)
        path2='../../../omegak_beta/beta_'+str(beta)
        shutil.copy(path2+'/omega_sr.dat',name1)
        shutil.copy(path2+'/omega_lr.dat',name1)
    #os.chdir('..')
    return






















