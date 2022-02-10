import NDpredict as ndp
import numpy as np
from .tools_aux import adjust_probs_scale

def convert_mass_to_log_msun(value):
    h = 0.6774
    res = []
    
    if (isinstance(value, list)):
         for i in range(len(value)):
             res.append(np.log10(value[i]*(1e10/h)))
         return res

    return np.log10(value*(1e10/h))

def get_mass_stars_dict(sample):
    dict_sample = {}
    
    for i in range(0, len(sample)):
        dict_sample[sample['id'][i]] = sample['mass_stars'][i]
            
    return dict_sample

def calc_prob_ndp(sample, z0, zf, M0):
    sample_dict = get_mass_stars_dict(sample)
    sample_convert = convert_mass_to_log_msun(list(sample_dict.values()))
    sample_masses = sample_convert #Array de massas estelares de todas as galáxias da amostra
    vol = 50**3  #Volume da amostra in Mpc^3
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
    #np.ageatmax(probs)
    #np.ageatmin(probs)

    probsdict = {}
    sample_id = list(sample_dict.keys())
    for i in range(len(sample_dict)):
        probsdict[sample_id[i]] = probs[i]
        
    adjust_probs_scale(probsdict)

    return probsdict

def print_npd_probs(probs, snap_num_zf, z0, zf, M0, prog_subhalo_id, true_desc_subhalo_id):
    print ('Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')\n')
    print ('z0='+str(z0))
    print ('zf='+str(zf))
    print ('Snap='+str(snap_num_zf))
    print ('M0='+str(M0))
    print ('Total='+str(sum(list(probs.values())))+'\n')
    print (probs)
    print ('\n\n')