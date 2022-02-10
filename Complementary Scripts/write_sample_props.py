import illustris_python as il
import os

def write_sample_props(simulation_name, snap_num, halo_id):
    base_path = './'+simulation_name+'/output/'
    name = "props_"+str(snap_num)+"_haloID="+str(halo_id)
    
    halo = il.groupcat.loadSingle(base_path,snap_num,haloID=halo_id)
    
    # if ((halo['GroupMass']*(1e10/0.6774))>1e14):
    if (True):
        cwd = os.getcwd()
        dir_name = cwd+'\\Results'
    
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
       
        file = open('Results/'+name+'.txt', 'w') #O arquivo com os dados serão salvos na pasta 'Resultados'
    
        file.write('Simulação '+simulation_name+'\n')
        file.write('Snapshot='+str(snap_num)+'\n')
        file.write('HaloID='+str(halo_id)+'\n\n')
        file.write('Propriedades'+'\n\n')
        file.write('Massa: '+str(halo['GroupMass'])+'\n')
        file.write('Quantidade de subhalos: '+str(halo['GroupNsubs'])+'\n\n')
        #file.write('pos_x\tpos_y\tpos_z\tvel_x\tvel_y\tvel_z\n')
        file.write('id,pos_x,pos_y,pos_z,vel_x,vel_y,vel_z\n')
        #file.write(str(halo['GroupPos'][0]).replace('.',',')+'\t'+str(halo['GroupPos'][1]).replace('.',',')+'\t'+str(halo['GroupPos'][2]).replace('.',',')+'\t'+str(halo['GroupVel'][0]).replace('.',',')+'\t'+str(halo['GroupVel'][1]).replace('.',',')+'\t'+str(halo['GroupVel'][2]).replace('.',','))
        file.write(str(halo['GroupPos'][0])+','+str(halo['GroupPos'][1])+','+str(halo['GroupPos'][2])+','+str(halo['GroupVel'][0])+','+str(halo['GroupVel'][1])+','+str(halo['GroupVel'][2]))
       
        file.write('\n\nPropriedades dos subhalos\n\n')
        #file.write('id\tpos_x\tpos_y\tpos_z\tvel_x\tvel_y\tvel_z\n')
        file.write('id,pos_x,pos_y,pos_z,vel_x,vel_y,vel_z,g,r,g-r,mass_stars,gasmetallicity,starmetallicity,halfmassrad,halfmassrad_gas\n')
    
        for i in range(halo['GroupFirstSub'],halo['GroupFirstSub']+halo['GroupNsubs']):
             subhalo = il.groupcat.loadSingle(base_path,snap_num,subhaloID=i)
             subhalo_mass_stars = subhalo['SubhaloMassType'][4]
             subhalo_mass = subhalo['SubhaloMass']
             #file.write(str(i)+'\t'+str(subhalo['SubhaloPos'][0]).replace('.',',')+'\t'+str(subhalo['SubhaloPos'][1]).replace('.',',')+'\t'+str(subhalo['SubhaloPos'][2]).replace('.',',')+'\t'+str(subhalo['SubhaloVel'][0]).replace('.',',')+'\t'+str(subhalo['SubhaloVel'][1]).replace('.',',')+'\t'+str(subhalo['SubhaloVel'][2]).replace('.',',')+'\n')
             
             if (subhalo_mass_stars>0 and ((subhalo_mass*(1e10/0.6774))>=1e9)):
                 if (subhalo['SubhaloStellarPhotometrics'][4] >= 1e36):
                     filter_g = 0
                 else:
                     filter_g = subhalo['SubhaloStellarPhotometrics'][4]
                     
                 if (subhalo['SubhaloStellarPhotometrics'][5] >= 1e36):
                     filter_r = 0
                 else:
                     filter_r = subhalo['SubhaloStellarPhotometrics'][5]
                     
                 filter_g_r = filter_g - filter_r
                 
                 file.write(str(i)+','+str(subhalo['SubhaloPos'][0])+','+str(subhalo['SubhaloPos'][1])+','+str(subhalo['SubhaloPos'][2])+','+str(subhalo['SubhaloVel'][0])+','+str(subhalo['SubhaloVel'][1])+','+str(subhalo['SubhaloVel'][2])+','+str(filter_g)+','+str(filter_r)+','+str(filter_g_r)+','+str(subhalo['SubhaloMassType'][4])+','+str(subhalo['SubhaloGasMetallicity'])+','+str(subhalo['SubhaloStarMetallicity'])+','+str(subhalo['SubhaloHalfmassRad'])+','+str(subhalo['SubhaloHalfmassRadType'][0])+'\n')
    
        file.close()
    
for i in range(80,81):
    write_sample_props('TNG100-3', i, 39)