#Contador de aglomerados e grupos lendo os arquivos

import illustris_python as il
import numpy as np
base_path = './TNG100-1/output/'
halos = il.groupcat.loadHalos(base_path,50)
halos_mass = halos['GroupMass']
#halos_mass_stars = halos['GroupMassType'][:,4]
max_halo_mass = np.nanmax(halos_mass)
max_halo_index = np.argmax(halos_mass)

quant_cluster = 0
quant_group = 0
i = 0
tol = 20
halos_id_cluster = []
halos_id_group = []

for mass in halos_mass:
    if ((mass*(1e10/0.6774))>1e14):
        quant_cluster += 1
        halos_id_cluster.append(i)
    
    elif ((mass*(1e10/0.6774))>1e13):
        quant_group += 1
        halos_id_group.append(i)
    else:
        tol += 1
        
    if (tol>20):
        break;
        
    i += 1
        
print (quant_cluster)
print (quant_group)

"""
#Contador de aglomerados e grupos usando a API
from datetime import datetime
import requests

baseUrl = 'http://www.tng-project.org/api/'
headers = {"api-key":"ecdec434ff4a3bd35fe104a00544c427"}

def get(path, params=None):
    # make HTTP GET request to path
    r = requests.get(path, params=params, headers=headers)

    # raise exception if response code is not HTTP SUCCESS (200)
    r.raise_for_status()

    if r.headers['content-type'] == 'application/json':
        return r.json() # parse json responses automatically
   
    if 'content-disposition' in r.headers:
        filename = r.headers['content-disposition'].split("filename=")[1]
        with open(filename, 'wb') as f:
            f.write(r.content)
        return filename # return the filename string

    return r

simulations = ['TNG300-1']

for simulation_name in simulations:
    start_time = datetime.now()
    
    snap_num = 50
    quant_cluster = 0
    quant_group = 0
    tol = 0
    halos_id_cluster = []
    halos_id_group = []
    
    simulation_details = get('http://www.tng-project.org/api/'+simulation_name+'/snapshots/'+str(snap_num)+'/')
    halos_count = simulation_details['num_groups_fof']
    
    for halo_id in range(2513, halos_count):
        halo_info = get('http://www.tng-project.org/api/'+simulation_name+'/snapshots/'+str(snap_num)+'/halos/'+str(halo_id)+'/info.json')
        halo_mass = halo_info['GroupMass']
        
        if ((halo_mass*(1e10/0.6774))>1e14):
            quant_cluster += 1
            halos_id_cluster.append(halo_id)
    
        elif ((halo_mass*(1e10/0.6774))>1e13):
            quant_group += 1
            halos_id_group.append(halo_id)
            
        else:
            tol += 1
            
        if (tol>20):
            break;
        
    print (simulation_name)    
    print (quant_cluster)
    print (quant_group)
        
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    print ('\n')
"""