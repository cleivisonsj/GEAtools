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

"""
Colocar esses códigos no terminal para listar as simulações disponíveis

r = get(baseUrl)
r.keys()
len(r['simulations'])
r['simulations'][0]
names = [sim['name'] for sim in r['simulations']]
names
"""

"""
Colocar esses códigos no terminal para requisitar os dados de uma simulação

i = names.index('TNG100-3')
i
sim = get( r['simulations'][i]['url'] )
sim.keys()
sim['num_dm']
"""

"""
Exemplo requisitando a última snapshots da simulação selecionada

sim['snapshots']
snaps = get( sim['snapshots'] )
snaps[-1]
snap = get( snaps[-1]['url'] )
snap
"""

"""
Exemplo requisitando subhalos

subs = get( snap['subhalos'] )
subs.keys()
subs['count']
subs['next']
len(subs['results'])
"""

"""
Aumentando o limite dos resultados
subs = get( snap['subhalos'], {'limit':220} )
len(subs['results'])
subs['next']
subs['results'][0]
"""

"""
Personalizando a busca, ordenado o resultado por ordem decrescente de massa estelar

subs = get( snap['subhalos'], {'limit':20, 'order_by':'-mass_stars'} )
len(subs['results'])
[ subs['results'][i]['id'] for i in range(5) ]
"""

"""
Examinando um subhalo
sub = get( subs['results'][1]['url'] )
sub
"""

"""
Examinando o subhalo parent
url = sub['related']['parent_halo'] + "info.json"
url
parent_fof = get(url)
parent_fof.keys()
parent_fof['Group']
"""

"""
Exemplo

import h5py
mpb1 = get( sub['trees']['sublink_mpb'] ) # file saved, mpb1 contains the filename
f = h5py.File(mpb1,'r')
print f.keys()
print len(f['SnapNum'])
print f['SnapNum'][:]
f.close()

mpb2 = get( sub['trees']['lhalotree_mpb'] ) # file saved, mpb2 contains the filename
with h5py.File(mpb2,'r') as f:
    print len(f['SnapNum'])
    
import matplotlib.pyplot as mpl
with h5py.File(mpb2,'r') as f:
    pos = f['SubhaloPos'][:]
    snapnum = f['SnapNum'][:]
    subid = f['SubhaloNumber'][:]

for i in range(3):
    plt.plot(snapnum,pos[:,i] - pos[0,i], label=['x','y','z'][i])
plt.legend()
plt.xlabel('Snapshot Number')
plt.ylabel('Pos$_{x,y,z}$(z) - Pos(z=0)');

url = sim['snapshots'] + "z=1/"
url
snap = get(url)
snap['number'], snap['redshift']

i = np.where(snapnum == 85)
subid[i]

sub_prog_url = "http://www.tng-project.org/api/Illustris-3/snapshots/85/subhalos/185/"
sub_prog = get(sub_prog_url)
sub_prog['pos_x'], sub_prog['pos_y']

cutout_request = {'gas':'Coordinates,Masses'}
cutout = get(sub_prog_url+"cutout.hdf5", cutout_request)

with h5py.File(cutout,'r') as f:
    x = f['PartType0']['Coordinates'][:,0] - sub_prog['pos_x']
    y = f['PartType0']['Coordinates'][:,1] - sub_prog['pos_y']
    dens = np.log10(f['PartType0']['Masses'][:])
 
    plt.hist2d(x,y,weights=dens,bins=[150,100])
    plt.xlabel('$\Delta x$ [ckpc/h]')
    plt.ylabel('$\Delta y$ [ckpc/h]');
"""

"""
Baixando arquivos

list = get('http://www.tng-project.org/api/TNG100-3/files/groupcat-99/')
print (list['files'][0])

#Baixar um arquivo específico
file = get(list['files'][0])

#Baixar todos os arquivos
for i in range(len(list['files'])):
    get(list['files'][i])

import h5py
f = h5py.File(file,'r')
f.keys()
"""

"""
Manipulando arquivos

import h5py
import illustris_python as il
basePath = './TNG50-4/output/'
fields = ['SubhaloMass','SubhaloSFRinRad']
subhalos = il.groupcat.loadSubhalos(basePath,98,fields=fields)
subhalos.keys()
subhalos['SubhaloMass'].shape

Converter para mass log msun

print (np.log10(14501.287109375 * (1e10 / 0.6773993978395485)))
print (np.log10(14501.287109375 * (1e10 / 0.6774)))

Testes
import numpy as np
halos = il.groupcat.loadHalos(basePath,98)
halos_mass = halos['GroupMass']
halos_mass_stars = halos['GroupMassType'][:,4]
max_halo_mass = np.nanmax(halos_mass)
max_halo_index = np.nanargmax(halos_mass)
((max_halo_mass*1e10)/0.6774)>1e14 #aglomerado
((max_halo_mass*1e10)/0.6774)>1e13 #grupo
"""