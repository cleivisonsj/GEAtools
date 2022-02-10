import NDpredict as ndp
import illustris_python as il
import numpy as np
import matplotlib.pyplot as plt

def convert_mass_to_log_msun (value):
    h = 0.6774
    res = []
    
    if (isinstance(value, list)):
         for i in range(len(value)):
             res.append(np.log10(value[i]*(1e10/h)))
         return res

    return np.log10(value*(1e10/h))

"""
Verificando qual o maior halo do snapshot e se ele é aglomerado ou grupo

import illustris_python as il
import numpy as np
base_path = './TNG50-4/output/'
halos = il.groupcat.loadHalos(base_path,50)
halos_mass = halos['GroupMass']
#halos_mass_stars = halos['GroupMassType'][:,4]
max_halo_mass = np.nanmax(halos_mass)
max_halo_index = np.nanargmax(halos_mass)
(max_halo_mass*(1e10/0.6774))>1e14 #aglomerado
(max_halo_mass*(1e10/0.6774))>1e13 #grupo
"""

def write_probs(name, title, probs):    
    file = open('Gráficos/'+name+'.txt', 'w')
    
    file.write(title+'\n\n')

    for key in probs:
        file.write(str(key)+': '+str(probs[key])+'\n')

    file.close()
    
def get_subhalo_descendant_tree(snap_num, subhalo_id):
    file = open('Resultados/subhaloID='+str(subhalo_id)+'_descendant_tree_start_at='+str(snap_num)+'.txt', 'r')
    content = file.readlines()
    start_snap_num = int(content[0])
    
    subhalo_descendant_tree_dict = {}
    
    for i in range(1, len(content)):
        value = int(content[i])
        subhalo_descendant_tree_dict[start_snap_num+i] = value

    return subhalo_descendant_tree_dict

def get_redshifts():
    file = open('redshifts.txt', 'r')
    content = file.readlines()
    
    redshifts_dict = {}
    
    for i in range(len(content)):
        value = float(content[i])
        redshifts_dict[i] = value

    return redshifts_dict

def get_subhalo_mass_star(snap_num, subhalo_id):
    base_path = './TNG50-4/output/'

    subhalo = il.groupcat.loadSingle(base_path,snap_num,subhaloID=subhalo_id)
    subhalo_mass_stars = subhalo['SubhaloMassType'][4]
    
    return subhalo_mass_stars

def get_total_halos(snap_num):
    base_path = './TNG50-4/output/'
    halos = il.groupcat.loadHalos(base_path,snap_num)
    
    return halos['count']

#Retorna um array da massas estelares de todos os subhalos do halo id=0 de um snapshot informado
def get_sample(snap_num, halo_id):
    sampledict = {}
    base_path = './TNG50-4/output/'

    halo = il.groupcat.loadSingle(base_path,snap_num,haloID=halo_id)
    
    for i in range(halo['GroupFirstSub'],halo['GroupFirstSub']+halo['GroupNsubs']):
         subhalo = il.groupcat.loadSingle(base_path,snap_num,subhaloID=i)
         subhalo_mass_stars = subhalo['SubhaloMassType'][4]
         
         if (subhalo_mass_stars>0):
             sampledict[i] = subhalo_mass_stars
   
    """
    subhalos_mass_stars = il.groupcat.loadSubhalos(base_path,snap_num,fields=['SubhaloMassType'])[:,4]
    
    for i in range(0,len(subhalos_mass_stars)):
         subhalo_mass_stars = subhalos_mass_stars[i]
         
         if (subhalo_mass_stars>0):
             sampledict[i] = subhalo_mass_stars
    """

    return sampledict

def adjust_probs_scale (probs):
    total = sum(list(probs.values()))
    
    for key in probs:
        probs[key] = probs[key]/total

def calc_prob(snap_num, z0, zf, M0, subhalo_id, halo_id, sample, cor="red"):
    sample_convert = convert_mass_to_log_msun(list(sample.values()))
    sample_masses = sample_convert #Array de massas estelares de todas as galáxias da amostra
    vol = 15**3  #Volume da amostra in Mpc^3
    #z0 = 1 #Redshift da previsão
    #zf = 0 #Redshift da amostra
    M0 = convert_mass_to_log_msun(M0) #Massa do subhalo em z0 que se quer prever
    probs = ndp.assign_probabilities(M0, z0, zf, sample_masses, vol, massfunc='illustris')

    #Mean descendant mass
    #Mavg = np.average(list(sample.values()), weights=probs)
    #print (Mavg)

    #Formas de analizar os resultados
    #max(probs)
    #min(probs)
    #np.argmax(probs)
    #np.argmin(probs)

    probsdict = {}
    sample_id = list(sample.keys())
    for i in range(len(sample)):
        probsdict[sample_id[i]] = probs[i]
        
    adjust_probs_scale(probsdict)
    probs_ordered = dict(sorted(probsdict.items(), key=lambda item: item[1])) #Ordena as probabilidades em ordem crescente

    """
    print ('Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(subhalo_id)+' em z='+str(z0)+'\n')
    print ('z0='+str(z0))
    print ('zf='+str(zf))
    print ('Snap='+str(snap_num))
    print ('M0='+str(M0))
    print ('Total='+str(sum(list(probs_ordered.values())))+'\n')
    """
    print (probs_ordered)
    print ('\n\n')
    

    #Gera um gráfico de barras
    num_subhalos = 10 #apenas as informações dos subhalos com maiores probabilidades serão exibidas para melhor visualização dos dados (neste caso os 10 maiores)
    
    subhalos_id = list(probs_ordered.keys())
    subhalos_id_ajusted = subhalos_id[-num_subhalos:]
    subhalos_id_ajusted = [str(element) for element in subhalos_id_ajusted]
    
    probs_list = list(probs_ordered.values())
    probs_list_ajusted = probs_list[-num_subhalos:]
    
    #Ajuste nos valores das probabilidades para possibilitar a visualização no gráfico, já que os valores gerados são muito pequenos
    """
    min_exp = abs(np.floor(np.log10(np.abs(probs_list[0]))).astype(int)) #Retorna o menor expoente da lista de probabilidades
    const = 10.**min_exp
    probs_list_ajusted = [element * const for element in probs_list_ajusted]
    """
    
    plt.bar(subhalos_id_ajusted, probs_list_ajusted, color=cor)
    plt.xticks(subhalos_id_ajusted)
    plt.ylabel('Probabilidades')
    plt.xlabel('Id do subhalo')
    plt.title('Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(subhalo_id)+' em z='+str(z0)+'\n')
    plt.show()
    
    return probs_ordered

"""
Subhalo escolhido em z=1, snapshot=50
subhalo_id = 4, mass_star = 3.060467004776001
"""

start_snapshot = 50
start_subhalo = 4
max_probs_dict = {}
redshifts = get_redshifts()
subhalo_descendant_tree = get_subhalo_descendant_tree(start_snapshot, start_subhalo)

subhalo_id = 4
snap_num = 51
z0 = redshifts[start_snapshot]
zf = redshifts[snap_num]
M0 = get_subhalo_mass_star(start_snapshot, subhalo_id)

total_halos = get_total_halos(snap_num)

for i in range(total_halos):
    sample = get_sample(snap_num, i)
    
    if (len(sample)>50):
        probs = calc_prob(snap_num, z0, zf, M0, subhalo_id, i, sample)
        max_probs_dict[list(probs.keys())[-1]] = list(probs.values())[-1]
    
max_probs_dict_ordered = dict(sorted(max_probs_dict.items(), key=lambda item: item[1]))
max_probs_dict_ordered