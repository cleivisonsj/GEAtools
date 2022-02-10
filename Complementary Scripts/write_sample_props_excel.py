import illustris_python as il
import xlsxwriter
import math
import os

cwd = os.getcwd()
dir_name = cwd+'\\Results'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

halo_id = 0 #Id do halo que se quer obter as propriedades
workbook = xlsxwriter.Workbook('Results/props_haloID='+str(halo_id)+'.xlsx')

def write_sample_props(simulation_name, snap_num):
    base_path = './'+simulation_name+'/output/'
    worksheet = workbook.add_worksheet('Snap='+str(snap_num))
    worksheet.set_column('A:P', 15)
    
    halo = il.groupcat.loadSingle(base_path,snap_num,haloID=halo_id)
    
    worksheet.write(0, 0, 'Simulação TNG50-4')
    worksheet.write(1, 0, 'Snapshot='+str(snap_num))
    worksheet.write(2, 0, 'HaloID='+str(halo_id))
    worksheet.write(4, 0,'Propriedades')
    worksheet.write(6, 0, 'Quantidade de subhalos: '+str(halo['GroupNsubs']))
    worksheet.write(8, 0, 'pos_x')
    worksheet.write(8, 1, 'pos_y')
    worksheet.write(8, 2, 'pos_z')
    worksheet.write(8, 3, 'vel_x')
    worksheet.write(8, 4, 'vel_y')
    worksheet.write(8, 5, 'vel_z')
    worksheet.write(8, 6, 'R200')
    worksheet.write(8, 7, 'R500')
    worksheet.write(8, 8, 'M200')
    worksheet.write(8, 9, 'M500')
    worksheet.write(9, 0, halo['GroupPos'][0])
    worksheet.write(9, 1, halo['GroupPos'][1])
    worksheet.write(9, 2, halo['GroupPos'][2])
    worksheet.write(9, 3, halo['GroupVel'][0])
    worksheet.write(9, 4, halo['GroupVel'][1])
    worksheet.write(9, 5, halo['GroupVel'][2])
    worksheet.write(9, 6, halo['Group_R_Crit200'])
    worksheet.write(9, 7, halo['Group_R_Crit500'])
    worksheet.write(9, 8, halo['Group_M_Crit200'])
    worksheet.write(9, 9, halo['Group_M_Crit500'])
    worksheet.write(11, 0, 'Propriedades dos subhalos')
    worksheet.write(13, 0, 'id')
    worksheet.write(13, 1, 'pos_x')
    worksheet.write(13, 2, 'pos_y')
    worksheet.write(13, 3, 'pos_z')
    worksheet.write(13, 4, 'vel_x')
    worksheet.write(13, 5, 'vel_y')
    worksheet.write(13, 6, 'vel_z')
    worksheet.write(13, 7, 'g')
    worksheet.write(13, 8, 'r')
    worksheet.write(13, 9, 'i')
    worksheet.write(13, 10, 'z')
    worksheet.write(13, 11, 'g-r')
    worksheet.write(13, 12, 'r-i')
    worksheet.write(13, 13, 'i-z')
    worksheet.write(13, 14, 'd')
    worksheet.write(13, 15, 'halfmassrad')

    for i in range(halo['GroupFirstSub'],halo['GroupFirstSub']+halo['GroupNsubs']):
         subhalo = il.groupcat.loadSingle(base_path,snap_num,subhaloID=i)
         worksheet.write(14+i, 0, i)
         worksheet.write(14+i, 1, subhalo['SubhaloPos'][0])
         worksheet.write(14+i, 2, subhalo['SubhaloPos'][1])
         worksheet.write(14+i, 3, subhalo['SubhaloPos'][2])
         worksheet.write(14+i, 4, subhalo['SubhaloVel'][0])
         worksheet.write(14+i, 5, subhalo['SubhaloVel'][1])
         worksheet.write(14+i, 6, subhalo['SubhaloVel'][2])
         
         if (subhalo['SubhaloStellarPhotometrics'][4] >= 1e36):
             filter_g = 0
         else:
             filter_g = subhalo['SubhaloStellarPhotometrics'][4]
             
         if (subhalo['SubhaloStellarPhotometrics'][5] >= 1e36):
             filter_r = 0
         else:
             filter_r = subhalo['SubhaloStellarPhotometrics'][5]
             
         if (subhalo['SubhaloStellarPhotometrics'][6] >= 1e36):
             filter_i = 0
         else:
             filter_i = subhalo['SubhaloStellarPhotometrics'][6]
             
         if (subhalo['SubhaloStellarPhotometrics'][7] >= 1e36):
             filter_z = 0
         else:
             filter_z = subhalo['SubhaloStellarPhotometrics'][7]
            
         filter_g_r = filter_g - filter_r
         filter_r_i = filter_r - filter_i
         filter_i_z = filter_i - filter_z
                
         xa = halo['GroupPos'][0]
         ya = halo['GroupPos'][1]
         za = halo['GroupPos'][2]
                
         xb = subhalo['SubhaloPos'][0]
         yb = subhalo['SubhaloPos'][1]
         zb = subhalo['SubhaloPos'][2]
         
         d = math.sqrt(math.pow(xb-xa,2)+math.pow(yb-ya,2)+math.pow(zb-za,2))
             
         worksheet.write(14+i, 7, filter_g)
         worksheet.write(14+i, 8, filter_r)
         worksheet.write(14+i, 9, filter_i)
         worksheet.write(14+i, 10, filter_z)
         worksheet.write(14+i, 11, filter_g_r)
         worksheet.write(14+i, 12, filter_r_i)
         worksheet.write(14+i, 13, filter_i_z)
         worksheet.write(14+i, 14, d)
         worksheet.write(14+i, 15, subhalo['SubhaloHalfmassRad'])

for i in range(50,77):
    write_sample_props('TNG50-4', i)
    
workbook.close()