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

def get_halo_descendant_tree(simulation_name, start_snap_num):
    #Deve-se definir o subhalo mais massivo do halo nesse snapshot como ponto de partida
    #Neste caso queremos a árvore do haloID=0 que tem como subhalo mais massivo o subhaloID=0
    subhalo = get('http://www.tng-project.org/api/'+simulation_name+'/snapshots/'+str(start_snap_num)+'/subhalos/0/')
    sublink_descendant = subhalo['related']['sublink_descendant']
    
    parent_halo = get(subhalo['related']['parent_halo'])
    halo_id = parent_halo['halo_id']
    
    cwd = os.getcwd()
    dir_name = cwd+'\\Results'

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    file = open('Results/halo_descendant_tree.txt', 'w')
    file.write('Simulação '+simulation_name+'\n')
    file.write('Começando do Snapshot='+str(start_snap_num)+'\n')
    file.write('HaloID='+str(halo_id)+'\n')
    file.write('SubhaloID Massivo='+str(subhalo['id'])+'\n\n')
    
    while (sublink_descendant!=None):
        subhalo = get(sublink_descendant)
        parent_halo = get(subhalo['related']['parent_halo'])
        
        file.write('Snapshot='+str(subhalo['snap'])+'\n')
        file.write('SubhaloID Massivo='+str(parent_halo['child_subhalos']['results'][0]['id'])+'\n')
        file.write('SubhaloID Descendante='+str(subhalo['id'])+'\n')
        file.write('Sublink Descendante='+str(sublink_descendant)+'\n\n')

        sublink_descendant = subhalo['related']['sublink_descendant']
        
get_halo_descendant_tree('TNG50-4', 50)