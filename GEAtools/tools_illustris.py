import illustris_python as il
import pandas as pd
import json
import math
import os
import requests
from .config import simulation_name

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

#Retorna um array da massas estelares e dados fotométricos de todos os subhalos do halo id=0 de um snapshot informado
def get_sample(snap_num, halo_id):    
    base_path = './'+simulation_name+'/output/'
    sample = {}
    list_id = []
    list_mass_stars = []
    list_filter_g = []
    list_filter_r = []
    list_filter_i = []
    list_filter_z = []
    list_filter_g_r = []
    list_filter_r_i = []
    list_filter_i_z = []
    list_sfr = []
    list_is_central = []

    halo = il.groupcat.loadSingle(base_path,snap_num,haloID=halo_id)
    halo_rad = halo['Group_R_Crit200']

    # halo['Group_R_Crit200']
    # halo['Group_R_Crit500']
    # halo['Group_M_Crit200']
    # halo['Group_M_Crit500']
    
    is_non_empty = bool(halo)
    
    if (is_non_empty):
        for i in range(halo['GroupFirstSub'],halo['GroupFirstSub']+halo['GroupNsubs']):
            subhalo = il.groupcat.loadSingle(base_path,snap_num,subhaloID=i)
            subhalo_mass_stars = subhalo['SubhaloMassType'][4]
            subhalo_mass = subhalo['SubhaloMass']
            
            if (subhalo_mass_stars>0 and ((subhalo_mass*(1e10/0.6774))>=1e9)):
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
                
                if (d<halo_rad):
                    is_central = True
                else:
                    is_central = False
                
                list_id.append(i)
                list_mass_stars.append(subhalo_mass_stars)
                list_filter_g.append(filter_g)
                list_filter_r.append(filter_r)
                list_filter_i.append(filter_i)
                list_filter_z.append(filter_z)
                list_filter_g_r.append(filter_g_r)
                list_filter_r_i.append(filter_r_i)
                list_filter_i_z.append(filter_i_z)
                list_sfr.append(subhalo['SubhaloSFR'])
                list_is_central.append(is_central)
    
    sample['id'] = list_id
    sample['mass_stars'] = list_mass_stars
    sample['filter_g'] = list_filter_g
    sample['filter_r'] = list_filter_r
    sample['filter_i'] = list_filter_i
    sample['filter_z'] = list_filter_z
    sample['filter_g_r'] = list_filter_g_r
    sample['filter_r_i'] = list_filter_r_i
    sample['filter_i_z'] = list_filter_i_z
    sample['sfr'] = list_sfr
    sample['is_central'] = list_is_central
       
    """
    subhalos_mass_stars = il.groupcat.loadSubhalos(base_path,snap_num,fields=['SubhaloMassType'])[:,4]
    """

    sample_df = pd.DataFrame(sample)

    return sample_df

def get_subhalo_mass_star(snap_num, subhalo_id):
    base_path = './'+simulation_name+'/output/'

    subhalo = il.groupcat.loadSingle(base_path,snap_num,subhaloID=subhalo_id)
    subhalo_mass_stars = subhalo['SubhaloMassType'][4]
    
    return subhalo_mass_stars

def get_subhalo_descendant_tree(snap_num, subhalo_id):
    file = open('Auxiliary Data/'+simulation_name+'/'+str(snap_num)+'/subhaloID='+str(subhalo_id)+'.txt', 'r')
    content = file.readlines()

    subhalo_descendant_tree_dict = {}
    
    for data in content:
        snap_num_descendant, subhalo_id_descendant, halo_parent_id = data.split(':', 2)
        subhalo_descendant_tree_dict[int(snap_num_descendant)] = int(subhalo_id_descendant)

    return subhalo_descendant_tree_dict

def get_halo_parent_tree(snap_num, subhalo_id):
    file = open('Auxiliary Data/'+simulation_name+'/'+str(snap_num)+'/subhaloID='+str(subhalo_id)+'.txt', 'r')
    content = file.readlines()

    halo_parent_tree_dict = {}
    
    for data in content:
        snap_num_descendant, subhalo_id_descendant, halo_parent_id = data.split(':', 2)
        data = []
        data.append(int(subhalo_id_descendant))
        data.append(int(halo_parent_id))
        halo_parent_tree_dict[int(snap_num_descendant)] = data

    return halo_parent_tree_dict

def get_halo_descendant_at_zf(snap_num_z0, snap_num_zf, primary_subhalo_id):
    halo_parent_tree = get_halo_parent_tree(snap_num_z0, primary_subhalo_id)
    
    if snap_num_zf in halo_parent_tree:
        halo_parent = halo_parent_tree[snap_num_zf][1]
    else:
        halo_parent = None
    
    return halo_parent

def get_halo_descendant_at_zf_api(snap_num_z0, snap_num_zf, primary_subhalo_id):
    subhalo_descendant_tree = get_subhalo_descendant_tree(snap_num_z0, primary_subhalo_id)
    primary_subhalo_id_descendant = subhalo_descendant_tree[snap_num_zf]
    
    primary_subhalo_id_info = get('http://www.tng-project.org/api/'+simulation_name+'/snapshots/'+str(snap_num_zf)+'/subhalos/'+str(primary_subhalo_id_descendant))
    halo_info = get(primary_subhalo_id_info['related']['parent_halo'])
    
    return halo_info['halo_id']

def get_subhalo_descendant_tree_api(snap_num, subhalo_id):
    try:
        with open('Cache/'+simulation_name+'/'+str(snap_num)+'/subhaloID='+str(subhalo_id)+'_descendant_tree_start_at='+str(snap_num)+'.txt') as json_file:
            tree_json = json.load(json_file)
    except:
        try:
            tree_json = get('http://www.tng-project.org/api/'+simulation_name+'/snapshots/'+str(snap_num)+'/subhalos/'+str(subhalo_id)+'/sublink/simple.json')
            path = 'Cache/'+simulation_name+'/'+str(snap_num)
            
            if not os.path.exists(path):
                os.makedirs(path)
            
            with open('Cache/'+simulation_name+'/'+str(snap_num)+'/subhaloID='+str(subhalo_id)+'_descendant_tree_start_at='+str(snap_num)+'.txt', 'w') as outfile:
                json.dump(tree_json, outfile)
        except:
            return None
    
    subhalo_descendant_tree_dict = {}
        
    for key in tree_json['Main']: 
        subhalo_descendant_tree_dict[key[0]] = key[1]
        
    return subhalo_descendant_tree_dict

def get_halos(snap_num):
    base_path = './'+simulation_name+'/output/'
    halos = il.groupcat.loadHalos(base_path,snap_num)
    return halos