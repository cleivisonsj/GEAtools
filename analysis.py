import GEAtools as geat

"""
Verificando qual o maior halo do snapshot e se ele é aglomerado ou grupo

import illustris_python as il
import numpy as np
base_path = './TNG50-4/output/'
halos = il.groupcat.loadHalos(base_path,50)
halos_mass = halos['GroupMass']
#halos_mass_stars = halos['GroupMassType'][:,4]
max_halo_mass = np.nanmax(halos_mass)
max_halo_index = np.argmax(halos_mass)
(max_halo_mass*(1e10/0.6774))>1e14 #aglomerado
(max_halo_mass*(1e10/0.6774))>1e13 #grupo
"""

snap_num_z0 = 50
snap_num_zf = 53
start_subhalo_z0 = 21

redshifts = geat.get_redshifts()
subhalo_descendant_tree = geat.get_subhalo_descendant_tree(snap_num_z0, start_subhalo_z0)

prog_subhalo_id = start_subhalo_z0
true_desc_subhalo_id = subhalo_descendant_tree[snap_num_zf]
z0 = redshifts[snap_num_z0]
zf = redshifts[snap_num_zf]
M0 = geat.get_subhalo_mass_star(snap_num_z0, prog_subhalo_id)
sample = geat.get_sample(snap_num_zf, 0)
probs_ndp = geat.calc_prob_ndp(sample, z0, zf, M0)
geat.print_bar_chart(probs_ndp,  'Resultado NDpredict', 'blue', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_ndp, 'Resultado NDpredict', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

probs_rg = geat.calc_prob_rg(sample, zf)
geat.adjust_probs_scale(probs_rg)

#Usando a combinação kk
method = 'kk'
kk = []

b1=0.75
b2=0.25
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
kk.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

b1=0.5
b2=0.5
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
kk.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

b1=0.25
b2=0.75
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
kk.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

#Usando a combinação loop
method = 'loop'
loop = []

b1=0.75
b2=0.25
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
loop.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

b1=0.5
b2=0.5
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
loop.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

b1=0.25
b2=0.75
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
loop.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

#Usando a combinação liop
method = 'liop'
liop = []

b1=0.75
b2=0.25
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
liop.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

b1=0.5
b2=0.5
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
liop.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

b1=0.25
b2=0.75
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
liop.append(probs_comb[true_desc_subhalo_id])
geat.print_bar_chart(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'red', z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample)
geat.write_probs(probs_comb, method+'/Resultado NDpredict '+str(int(b1*100))+'% e Redgalaxy '+str(int(b2*100))+'%', 'Probabilidades de cada subhalo da amostra em z='+str(zf)+' serem descendentes do subhalo id='+str(prog_subhalo_id)+' em z='+str(z0)+'\n(Id do subhalo verdadeiro='+str(true_desc_subhalo_id)+')')

kk_gp = []
liop_gp = []
loop_gp = []

for i in range (0, 3):
    kk_gp.append(((kk[i]/probs_ndp[true_desc_subhalo_id])-1)*100)
    liop_gp.append(((liop[i]/probs_ndp[true_desc_subhalo_id])-1)*100)
    loop_gp.append(((loop[i]/probs_ndp[true_desc_subhalo_id])-1)*100)

summary = {}
summary['kk'] = kk
summary['loop'] = loop
summary['liop'] = liop
summary['kk_gp'] = kk_gp
summary['loop_gp'] = loop_gp
summary['liop_gp'] = liop_gp
summary['ndp'] = probs_ndp[true_desc_subhalo_id]
summary['z0'] = z0
summary['zf'] = zf
summary['true_desc_subhalo_id'] = true_desc_subhalo_id
    
geat.write_summary(summary)
geat.write_summary_tab(summary)

x = [r'$\beta _1=0.75$ e $\beta _2=0.25$', r'$\beta _1=0.5$ e $\beta _2=0.5$', r'$\beta _1=0.25$ e $\beta _2=0.75$']

geat.print_chart_comp_comb(x, kk_gp, loop_gp, liop_gp)

# Gera um gráfico que mostra o resultado da combinação com a variação dos betas
# import numpy as np

# method = 'kk'
# method_values = []
# x = []

# b1=0.25
# b2=0.75
# step = 0.01

# i = 0

# while b1<=0.75:
#     probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
#     method_values.append(probs_comb[true_desc_subhalo_id])
#     x.append(b1)
#     #x.append('{'+str(b1)+','+str(b2)+'}')
#     b1 += step
#     b2 -= step
    
#     # print (b1,b2,i)
    
#     b1 = round(b1,2)
#     b2 = round(b2,2)
    
#     i += 1
    
# method_gp = []

# for i in range (len(method_values)):
#     method_gp.append(((method_values[i]/probs_ndp[true_desc_subhalo_id])-1)*100)

# geat.print_chart_comp_comb_method(x, method_gp, 'KK')

# max_value_method_gp = np.nanmax(method_gp)
# max_index_method_gp = np.argmax(method_gp)
# x[max_index_method_gp]

#sum(list(probs_comb.values()))

#subhalo_true_desc_subhalo_id_tree[70]
#convert_mass_to_log_msun(get_subhalo_mass_star(70, 5))