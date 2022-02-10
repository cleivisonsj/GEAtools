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
    

def down_merge_tree(simulation_name):
    cwd = os.getcwd()
    
    path = cwd+'\\'+simulation_name+'\\postprocessing\\trees\\SubLink'

    if not os.path.exists(path):
        os.makedirs(path)
    
    os.chdir(path)
    
    list = get('http://www.tng-project.org/api/'+simulation_name+'/files/sublink/')
    
    for i in range(len(list['files'])):
        get(list['files'][i])

#Baixando arquivos
def down_files(simulation_name, snap_num):
    cwd = os.getcwd()
    
    if (snap_num<10):
        zeros = '00'
    else:
        zeros = '0'

    path = cwd+'\\'+simulation_name+'\\output\\groups_'+zeros+str(snap_num)

    if not os.path.exists(path):
        os.makedirs(path)
    
    os.chdir(path)
    
    sucess=False
                
    while (sucess==False):
        try:
            list = get('http://www.tng-project.org/api/'+simulation_name+'/files/groupcat-'+str(snap_num)+'/')
            sucess=True
        except:
            sucess=False

    #print (list['files'])
    
    #Baixar um arquivo específico
    #file = get(list['files'][0])
    
    #Baixar todos os arquivos
    for i in range(len(list['files'])):
        sucess=False
                
        while (sucess==False):
            try:
                get(list['files'][i])
                sucess=True
            except:
                sucess=False

    """
    #Baixar snapshot
    path = cwd+'\\'+simulation_name+'\\output\\snapdir_'+zeros+str(snap_num)
   
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)
    
    list = get('http://www.tng-project.org/api/'+simulation_name+'/files/snapshot-'+str(snap_num)+'/')
    
    for i in range(len(list['files'])):
        get(list['files'][i])
    """
        
    path = cwd+'\\'+simulation_name+'\\postprocessing\\offsets'
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    os.chdir(path)
    
    sucess=False
                
    while (sucess==False):
        try:
            list = get('http://www.tng-project.org/api/'+simulation_name+'/files/offsets/')
            get(list['files'][snap_num])
            sucess=True
        except:
            sucess=False

    os.chdir(cwd)
    
snaps = [50,55,65,80,99]

for i in snaps:
    down_files('TNG100-1', i)

#down_files('TNG50-4', 50)

#down_merge_tree('TNG50-4')
    