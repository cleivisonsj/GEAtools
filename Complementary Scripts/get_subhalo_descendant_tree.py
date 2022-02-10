from datetime import datetime
start_time = datetime.now()

import requests
import os

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

def get_halo_total_subhalos(simulation_name, snap_num, halo_id):
    halo = get('http://www.tng-project.org/api/'+simulation_name+'/snapshots/'+str(snap_num)+'/halos/'+str(halo_id)+'/')
    return halo['child_subhalos']['results'][0]['id'], halo['child_subhalos']['count']

def get_subhalo_descendant_tree(simulation_name, start_snap_num, subhalo_id):
    subhalo = get('http://www.tng-project.org/api/'+simulation_name+'/snapshots/'+str(start_snap_num)+'/subhalos/'+str(subhalo_id)+'/')
    
    if (subhalo['mass_stars']>0 and ((subhalo['mass']*(1e10/0.6774))>=1e9)):
        sublink_descendant = subhalo['related']['sublink_descendant']
    
        cwd = os.getcwd()
        dir_name = cwd+'\\Auxiliary Data\\'+simulation_name+'\\'+str(start_snap_num)
    
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        file = open('Auxiliary Data/'+simulation_name+'/'+str(start_snap_num)+'/subhaloID='+str(subhalo_id)+'.txt', 'w')
        #file.write(str(start_snap_num)+'\n')
        
        while (sublink_descendant!=None):
            subhalo = get(sublink_descendant)
            halo_info = get(subhalo['related']['parent_halo'])
            
            file.write(str(subhalo['snap'])+':'+str(subhalo['id'])+':'+str(halo_info['halo_id'])+'\n')
            sublink_descendant = subhalo['related']['sublink_descendant']
            
        file.close()
                        
      
simulation_name = 'TNG50-4'

snaps = [50]
halos = [4]

for halos_id in halos:
    for snap_num in snaps:
        first_subhalo, total_subhalos = get_halo_total_subhalos(simulation_name, snap_num, halos_id)
        
        for subhalo_id in range(first_subhalo,first_subhalo+total_subhalos):
            try:
                file = open('Auxiliary Data/'+simulation_name+'/'+str(snap_num)+'/subhaloID='+str(subhalo_id)+'.txt', 'r')
                file.close()
            except:
                sucess=False
                
                while (sucess==False):
                    try:
                        get_subhalo_descendant_tree(simulation_name, snap_num, subhalo_id)
                        sucess=True
                    except:
                        sucess=False

# snap_num = 40
# subhalo_id = 4
                        
# try:
#     file = open('Auxiliary Data/'+simulation_name+'/'+str(snap_num)+'/subhaloID='+str(subhalo_id)+'.txt', 'r')
#     file.close()
# except:
#     sucess=False
                
#     while (sucess==False):
#         try:
#             get_subhalo_descendant_tree(simulation_name, snap_num, subhalo_id)
#             sucess=True
#         except:
#             sucess=False

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))