import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import os
from .tools_ndpredict import convert_mass_to_log_msun
from .config import simulation_name

def write_probs(probs, file_name, title):    
    file = open('Results/'+file_name+'.txt', 'w')
    
    file.write(title+'\n\n')

    for key in probs:
        file.write(str(key)+': '+str(probs[key])+'\n')

    file.close()
    
def write_summary(summary):    
    file = open('Results/summary.txt', 'w')
    
    file.write('Comparativo entre os métodos de combinação\n\n')
    file.write('z0: '+str(summary['z0'])+'\n')
    file.write('zf: '+str(summary['zf'])+'\n')
    file.write('Id do descendente verdadeiro em zf: '+str(summary['true_desc_subhalo_id'])+'\n\n')
    
    file.write('Resultados para o descendente verdadeiro\n\n')
    file.write('NDpredict: '+str(summary['ndp'])+'\n\n')
    
    file.write('KK\n\n')
    file.write('NDpredict 75% e Redgalaxy 25%: '+str(summary['kk'][0])+' Ganho/perda em relação ao NDpredict: '+str(summary['kk_gp'][0])+'%\n')
    file.write('NDpredict 50% e Redgalaxy 50%: '+str(summary['kk'][1])+' Ganho/perda em relação ao NDpredict: '+str(summary['kk_gp'][1])+'%\n')
    file.write('NDpredict 25% e Redgalaxy 75%: '+str(summary['kk'][2])+' Ganho/perda em relação ao NDpredict: '+str(summary['kk_gp'][2])+'%\n\n')
    
    file.write('LoOP\n\n')
    file.write('NDpredict 75% e Redgalaxy 25%: '+str(summary['loop'][0])+' Ganho/perda em relação ao NDpredict: '+str(summary['loop_gp'][0])+'%\n')
    file.write('NDpredict 50% e Redgalaxy 50%: '+str(summary['loop'][1])+' Ganho/perda em relação ao NDpredict: '+str(summary['loop_gp'][1])+'%\n')
    file.write('NDpredict 25% e Redgalaxy 75%: '+str(summary['loop'][2])+' Ganho/perda em relação ao NDpredict: '+str(summary['loop_gp'][2])+'%\n\n')
    
    file.write('LiOP\n\n')
    file.write('NDpredict 75% e Redgalaxy 25%: '+str(summary['liop'][0])+' Ganho/perda em relação ao NDpredict: '+str(summary['liop_gp'][0])+'%\n')
    file.write('NDpredict 50% e Redgalaxy 50%: '+str(summary['liop'][1])+' Ganho/perda em relação ao NDpredict: '+str(summary['liop_gp'][1])+'%\n')
    file.write('NDpredict 25% e Redgalaxy 75%: '+str(summary['liop'][2])+' Ganho/perda em relação ao NDpredict: '+str(summary['liop_gp'][2])+'%\n\n')

    file.close()
    
def write_summary_tab(summary):    
    file = open('Results/summary_tab.txt', 'w')
    
    file.write('Comparativo entre os métodos de combinação\n\n')
    file.write('z0: '+str(summary['z0'])+'\n')
    file.write('zf: '+str(summary['zf'])+'\n')
    file.write('Id do descendente verdadeiro em zf: '+str(summary['true_desc_subhalo_id'])+'\n\n')
    
    file.write('Resultados para o descendente verdadeiro\n\n')
    file.write('NDpredict\t'+str(round(summary['ndp'],4))+'\n\n')
    
    file.write('NDpredict 75% e Redgalaxy 25%\n')
    file.write('\tResultados\tG/P\n')
    file.write('KK\t'+str(round(summary['kk'][0],4))+'\t'+str(round(summary['kk_gp'][0],4))+'%\n')
    file.write('LoOP\t'+str(round(summary['loop'][0],4))+'\t'+str(round(summary['loop_gp'][0],4))+'%\n')
    file.write('LiOP\t'+str(round(summary['liop'][0],4))+'\t'+str(round(summary['liop_gp'][0],4))+'%\n\n')
    
    file.write('NDpredict 50% e Redgalaxy 50%\n')
    file.write('\tResultados\tG/P\n')
    file.write('KK\t'+str(round(summary['kk'][1],4))+'\t'+str(round(summary['kk_gp'][1],4))+'%\n')
    file.write('LoOP\t'+str(round(summary['loop'][1],4))+'\t'+str(round(summary['loop_gp'][1],4))+'%\n')
    file.write('LiOP\t'+str(round(summary['liop'][1],4))+'\t'+str(round(summary['liop_gp'][1],4))+'%\n\n')
    
    file.write('NDpredict 25% e Redgalaxy 75%\n')
    file.write('\tResultados\tG/P\n')
    file.write('KK\t'+str(round(summary['kk'][2],4))+'\t'+str(round(summary['kk_gp'][2],4))+'%\n')
    file.write('LoOP\t'+str(round(summary['loop'][2],4))+'\t'+str(round(summary['loop_gp'][2],4))+'%\n')
    file.write('LiOP\t'+str(round(summary['liop'][2],4))+'\t'+str(round(summary['liop_gp'][2],4))+'%\n\n')

    file.close()
    
def write_dists(dist_r, red_sample, dist_g, green_sample, dist_b, blue_sample, dists_scaled, slope, intercept):    
    file = open('Results/dists.txt', 'w')
    
    file.write('Cálculo das distâncias\n\n')
    
    file.write('Slope: '+str(slope)+'\n')
    file.write('Intercept: '+str(intercept)+'\n\n')
    
    file.write('Distâncias da amostra red\n')
    file.write('id\tdist\tdists_scaled\tfilter_r\tfilter_g_r\n')
    
    i = 0

    for key in dist_r:
        file.write(str(key)+'\t'+str(dist_r[key])+'\t'+str(dists_scaled[key])+'\t'+str(red_sample['filter_r'][i])+'\t'+str(red_sample['filter_g_r'][i])+'\n')
        i += 1
        
    file.write('\nDistâncias da amostra green\n')
    file.write('id\tdist\tdists_scaled\tfilter_r\tfilter_g_r\n')

    i = 0

    for key in dist_g:
        file.write(str(key)+'\t'+str(dist_g[key])+'\t'+str(dists_scaled[key])+'\t'+str(green_sample['filter_r'][i])+'\t'+str(green_sample['filter_g_r'][i])+'\n')
        i += 1
        
    file.write('\nDistâncias da amostra blue\n')
    file.write('id\tdist\tdists_scaled\tfilter_r\tfilter_g_r\n')
    
    i = 0

    for key in dist_b:
        file.write(str(key)+'\t'+str(dist_b[key])+'\t'+str(dists_scaled[key])+'\t'+str(blue_sample['filter_r'][i])+'\t'+str(blue_sample['filter_g_r'][i])+'\n')
        i += 1

    file.close()
    
def write_coefs(coefs):
    file = open('Results/coefs/coefs.txt', 'w')
    
    file.write('Parâmetros do ajuste linear\n\n')
    file.write('snap\tz\tslope\tintercept\terror_lr\ttotal_red\ttotal_sample\terror_modes\n')
    
    for key in coefs:
        file.write(str(key['snap'])+'\t'+str(key['z'])+'\t'+str(key['slope'])+'\t'+str(key['intercept'])+'\t'+str(key['error_lr'])+'\t'+str(key['total_red'])+'\t'+str(key['total_sample'])+'\t'+str(key['error_modes'])+'\n')
    
    file.close()
    
def write_probs_ndp_x_rg(snaps, redshifts, probs_ndp, probs_rg, gp, mass_log_msun, clear_files):  
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\data\\gp'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for i in range(0, len(snaps)):
        if (clear_files):
            file = open('Results/ndp_x_rg/'+simulation_name+'/data/gp/snap_'+str(snaps[i])+'.txt', 'w+')
        else:
            file = open('Results/ndp_x_rg/'+simulation_name+'/data/gp/snap_'+str(snaps[i])+'.txt', 'a+')
        
        file.seek(0)
        first_char = file.read(1)
        
        if not first_char:
            file.write('redshift='+str(redshifts[i])+'\n')
            file.write('halo_id\tprobs_ndp\tprobs_rg\tgp')
            # file.write('halo_id\tmass_log_msun\tprobs_ndp\tprobs_rg\tgp')
        
        for halo_id in probs_ndp:
            file.write('\n'+str(halo_id)+'\t'+str(round(probs_ndp[halo_id][i],4))+'\t'+str(round(probs_rg[halo_id][i],4))+'\t'+str(round(gp[halo_id][i],4)))
            # file.write(str(halo_id)+'\t'+str(mass_log_msun[halo_id])+'\t'+str(probs_ndp[halo_id][i])+'\t'+str(probs_rg[halo_id][i])+'\t'+str(gp[halo_id][i])+'\n')

        file.close()
        
def write_probs_errors(snaps, redshifts, errors_test_ndp, errors_test_rg, clear_files):  
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\data\\errors'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for i in range(0, len(snaps)):
        if (clear_files):
            file = open('Results/ndp_x_rg/'+simulation_name+'/data/errors/snap_'+str(snaps[i])+'.txt', 'w+')
        else:
            file = open('Results/ndp_x_rg/'+simulation_name+'/data/errors/snap_'+str(snaps[i])+'.txt', 'a+')
        
        file.seek(0)
        first_char = file.read(1)
        
        if not first_char:
            file.write('redshift='+str(redshifts[i])+'\n')
            file.write('halo_id\terrors_ndp\terrors_rg')
        
        for halo_id in errors_test_ndp:
            file.write('\n'+str(halo_id)+'\t'+str(round(errors_test_ndp[halo_id][i],4))+'\t'+str(round(errors_test_rg[halo_id][i],4)))

        file.close()
    
def write_halo_sfr_data(sfr_data, halo_id, snap_num):
    cwd = os.getcwd()
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\data\\sfr\\'+str(snap_num)
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    file = open('Results/ndp_x_rg/'+simulation_name+'/data/sfr/'+str(snap_num)+'/halo_'+str(halo_id)+'.txt', 'w')
    file.write('id\toriginal\tndp\trg\tgp_ndp\tgp_rg\tis_central\n')
    
    for i in range(0, len(sfr_data)):
        file.write(str(sfr_data['id'][i])+'\t'+str(round(sfr_data['original'][i],4))+'\t'+str(round(sfr_data['ndp'][i],4))+'\t'+str(round(sfr_data['rg'][i],4))+'\t'+str(round(sfr_data['gp_ndp'][i],4))+'\t'+str(round(sfr_data['gp_rg'][i],4))+'\t'+str(sfr_data['is_central'][i])+'\n')

    file.close()
    
def write_halo_sfr_mean_data(name, snaps, redshifts, sfr_true, sfr_ndp, sfr_rg, gp_sfr_mean_ndp, gp_sfr_mean_rg, clear_files):  
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\data\\sfr_mean'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for i in range(0, len(snaps)):
        if (clear_files):
            file = open('Results/ndp_x_rg/'+simulation_name+'/data/sfr_mean/snap_'+str(snaps[i])+'_'+name+'.txt', 'w+')
        else:
            file = open('Results/ndp_x_rg/'+simulation_name+'/data/sfr_mean/snap_'+str(snaps[i])+'_'+name+'.txt', 'a+')
        
        file.seek(0)
        first_char = file.read(1)
        
        if not first_char:
            file.write('redshift='+str(redshifts[snaps[i]])+'\n')
            file.write('halo_id\tsfr_true\tsfr_ndp\tsfr_rg\tgp_sfr_mean_ndp\tgp_sfr_mean_rg')
            # file.write('halo_id\tmass_log_msun\tprobs_ndp\tprobs_rg\tgp')
        
        for halo_id in sfr_true:
            file.write('\n'+str(halo_id)+'\t'+str(round(sfr_true[halo_id][i],4))+'\t'+str(round(sfr_ndp[halo_id][i],4))+'\t'+str(round(sfr_rg[halo_id][i],4))+'\t'+str(round(gp_sfr_mean_ndp[halo_id][i],4))+'\t'+str(round(gp_sfr_mean_rg[halo_id][i],4)))
            # file.write(str(halo_id)+'\t'+str(mass_log_msun[halo_id])+'\t'+str(probs_ndp[halo_id][i])+'\t'+str(probs_rg[halo_id][i])+'\t'+str(gp[halo_id][i])+'\n')

        file.close()
        
def write_halo_sfr_mean_tab(snaps, redshifts, sfr_rg, sfr_rg_central, sfr_rg_periphery):  
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\data\\sfr_mean_tab'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for i in range(0, len(snaps)):
        file = open('Results/ndp_x_rg/'+simulation_name+'/data/sfr_mean_tab/snap_'+str(snaps[i])+'.txt', 'w+')
        
        file.write('redshift='+str(redshifts[snaps[i]])+'\n')
        file.write('halo_id\tsfr_rg\tsfr_rg_central\tsfr_rg_periphery')
        
        for halo_id in sfr_rg:
            file.write('\n'+str(halo_id)+'\t'+str(round(sfr_rg[halo_id][i],4))+'\t'+str(round(sfr_rg_central[halo_id][i],4))+'\t'+str(round(sfr_rg_periphery[halo_id][i],4)))

        file.close()
    
def write_probs_associations(snaps, prog_subhalo_id_values, association_true_values, association_ndp_values, association_rg_values, sample_values):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\data\\associations'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    for halo_id in association_true_values:
        file_true = open('Results/ndp_x_rg/'+simulation_name+'/data/associations/halo_'+str(halo_id)+'_true.txt', 'w')
        file_ndp = open('Results/ndp_x_rg/'+simulation_name+'/data/associations/halo_'+str(halo_id)+'_ndp.txt', 'w')    
        file_rg = open('Results/ndp_x_rg/'+simulation_name+'/data/associations/halo_'+str(halo_id)+'_rg.txt', 'w')
        
        for prog_subhalo_id in prog_subhalo_id_values[halo_id][0]:
            for i in range(0, len(snaps)):
                if (i==0):
                    sample_data_dict = sample_values[halo_id][0]
                    file_true.write('subhalo '+str(prog_subhalo_id)+' ('+str(50)+', '+str(round(sample_data_dict[prog_subhalo_id][0],4))+', '+str(round(sample_data_dict[prog_subhalo_id][1],4))+', '+str(sample_data_dict[prog_subhalo_id][2])+')')
                    file_ndp.write('subhalo '+str(prog_subhalo_id)+' ('+str(50)+', '+str(round(sample_data_dict[prog_subhalo_id][0],4))+', '+str(round(sample_data_dict[prog_subhalo_id][1],4))+', '+str(sample_data_dict[prog_subhalo_id][2])+')')
                    file_rg.write('subhalo '+str(prog_subhalo_id)+' ('+str(50)+', '+str(round(sample_data_dict[prog_subhalo_id][0],4))+', '+str(round(sample_data_dict[prog_subhalo_id][1],4))+', '+str(sample_data_dict[prog_subhalo_id][2])+')')
                
                if (prog_subhalo_id in association_true_values[halo_id][i]):
                    descendant_subhalo_id_true = association_true_values[halo_id][i][prog_subhalo_id]
                    descendant_subhalo_id_ndp = association_ndp_values[halo_id][i][prog_subhalo_id]
                    descendant_subhalo_id_rg = association_rg_values[halo_id][i][prog_subhalo_id]
                    sample_data_dict = sample_values[halo_id][i+1]
                    file_true.write(' => subhalo '+str(descendant_subhalo_id_true)+' ('+str(snaps[i])+', '+str(round(sample_data_dict[descendant_subhalo_id_true][0],4))+', '+str(round(sample_data_dict[descendant_subhalo_id_true][1],4))+', '+str(sample_data_dict[descendant_subhalo_id_true][2])+')')
                    file_ndp.write(' => subhalo '+str(descendant_subhalo_id_ndp)+' ('+str(snaps[i])+', '+str(round(sample_data_dict[descendant_subhalo_id_ndp][0],4))+', '+str(round(sample_data_dict[descendant_subhalo_id_ndp][1],4))+', '+str(sample_data_dict[descendant_subhalo_id_ndp][2])+')')
                    file_rg.write(' => subhalo '+str(descendant_subhalo_id_rg)+' ('+str(snaps[i])+', '+str(round(sample_data_dict[descendant_subhalo_id_rg][0],4))+', '+str(round(sample_data_dict[descendant_subhalo_id_rg][1],4))+', '+str(sample_data_dict[descendant_subhalo_id_rg][2])+')')
                
            file_true.write('\n')
            file_ndp.write('\n')
            file_rg.write('\n')

        file_true.close()
        file_ndp.close()
        file_rg.close()
        
def write_probs_associations_excel(snaps, prog_subhalo_id_values, association_true_values, association_ndp_values, association_rg_values, sample_values):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\data\\associations'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    for halo_id in association_true_values:
        workbook = xlsxwriter.Workbook('Results/ndp_x_rg/'+simulation_name+'/data/associations/halo_'+str(halo_id)+'.xlsx')
        
        worksheet_true = workbook.add_worksheet('True')
        worksheet_ndp = workbook.add_worksheet('NDP')
        worksheet_rg = workbook.add_worksheet('RG')
        
        worksheet_true.write(0, 0, 50)
        worksheet_ndp.write(0, 0, 50)
        worksheet_rg.write(0, 0, 50)
        
        worksheet_true.set_column('A:X', 13)
        worksheet_ndp.set_column('A:X', 13)
        worksheet_rg.set_column('A:X', 13)
        
        for i in range(0, len(snaps)):
            worksheet_true.write(0, i*5+5, snaps[i])
            worksheet_ndp.write(0, i*5+5, snaps[i])
            worksheet_rg.write(0, i*5+5, snaps[i])

        line = 0
    
        for prog_subhalo_id in prog_subhalo_id_values[halo_id][0]:
            for i in range(0, len(snaps)):
                if (i==0):
                    sample_data_dict = sample_values[halo_id][0]

                    worksheet_true.write(line+1, 0, 'Subhalo '+str(prog_subhalo_id))
                    worksheet_true.write(line+1, 1, round(sample_data_dict[prog_subhalo_id][0],4))
                    worksheet_true.write(line+1, 2, round(sample_data_dict[prog_subhalo_id][1],4))
                    worksheet_true.write(line+1, 3, sample_data_dict[prog_subhalo_id][2])
                    
                    worksheet_ndp.write(line+1, 0, 'Subhalo '+str(prog_subhalo_id))
                    worksheet_ndp.write(line+1, 1, round(sample_data_dict[prog_subhalo_id][0],4))
                    worksheet_ndp.write(line+1, 2, round(sample_data_dict[prog_subhalo_id][1],4))
                    worksheet_ndp.write(line+1, 3, sample_data_dict[prog_subhalo_id][2])
                    
                    worksheet_rg.write(line+1, 0, 'Subhalo '+str(prog_subhalo_id))
                    worksheet_rg.write(line+1, 1, round(sample_data_dict[prog_subhalo_id][0],4))
                    worksheet_rg.write(line+1, 2, round(sample_data_dict[prog_subhalo_id][1],4))
                    worksheet_rg.write(line+1, 3, sample_data_dict[prog_subhalo_id][2])
            
                if (prog_subhalo_id in association_true_values[halo_id][i]):
                    descendant_subhalo_id_true = association_true_values[halo_id][i][prog_subhalo_id]
                    descendant_subhalo_id_ndp = association_ndp_values[halo_id][i][prog_subhalo_id]
                    descendant_subhalo_id_rg = association_rg_values[halo_id][i][prog_subhalo_id]
                    sample_data_dict = sample_values[halo_id][i+1]
                    
                    worksheet_true.write_string(line+1, i*5+4, '=>')
                    worksheet_true.write(line+1, i*5+1+4, 'Subhalo '+str(descendant_subhalo_id_true))
                    worksheet_true.write(line+1, i*5+2+4, round(sample_data_dict[descendant_subhalo_id_true][0],4))
                    worksheet_true.write(line+1, i*5+3+4, round(sample_data_dict[descendant_subhalo_id_true][1],4))
                    worksheet_true.write(line+1, i*5+4+4, sample_data_dict[descendant_subhalo_id_true][2])
                    
                    worksheet_ndp.write_string(line+1, i*5+4, '=>')
                    worksheet_ndp.write(line+1, i*5+1+4, 'Subhalo '+str(descendant_subhalo_id_ndp))
                    worksheet_ndp.write(line+1, i*5+2+4, round(sample_data_dict[descendant_subhalo_id_ndp][0],4))
                    worksheet_ndp.write(line+1, i*5+3+4, round(sample_data_dict[descendant_subhalo_id_ndp][1],4))
                    worksheet_ndp.write(line+1, i*5+4+4, sample_data_dict[descendant_subhalo_id_ndp][2])
                    
                    worksheet_rg.write_string(line+1, i*5+4, '=>')
                    worksheet_rg.write(line+1, i*5+1+4, 'Subhalo '+str(descendant_subhalo_id_rg))
                    worksheet_rg.write(line+1, i*5+2+4, round(sample_data_dict[descendant_subhalo_id_rg][0],4))
                    worksheet_rg.write(line+1, i*5+3+4, round(sample_data_dict[descendant_subhalo_id_rg][1],4))
                    worksheet_rg.write(line+1, i*5+4+4, sample_data_dict[descendant_subhalo_id_rg][2])
                    
            line = line + 1

        workbook.close()
    
def print_bar_chart(probsdict, file_name, cor, z0, zf, prog_subhalo_id, true_desc_subhalo_id, M0, sample):
    #Gera um gráfico de barras
    probs_ordered = dict(sorted(probsdict.items(), key=lambda item: item[1])) #Ordena as probabilidades em ordem crescente

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
    
    if (z0<zf):
        text = 'progenitor'
    else:
        text = 'descendente'

    plt.title('Probabilidades de cada subhalo da amostra em $z='+str(zf)+'$ serem descendentes do subhalo $id='+str(prog_subhalo_id)+'$ em $z='+str(z0)+'$\n(Id do subhalo '+text+' verdadeiro='+str(true_desc_subhalo_id)+')')
    
    M0_log_msun = convert_mass_to_log_msun(M0)
    min_log_msun = convert_mass_to_log_msun(np.nanmin(sample['mass_stars']))
    max_log_msun = convert_mass_to_log_msun(np.nanmax(sample['mass_stars']))
    
    plt.figtext(.15, .7, '$M_0 = '+str(round(M0_log_msun, 4))+'$ $log(M_\odot)$\n'+
                         '$I = '+str(round(min_log_msun, 4))+' - '+str(round(max_log_msun, 4))+'$ $log(M_\odot)$\n'+
                         '$N = '+str(len(sample))+'$')
    plt.savefig('Results/'+file_name+'.png', bbox_inches='tight')
    plt.show()
    
def print_error_chart_z_slope(redshifts, slopes, error):
    fig, ax = plt.subplots()
    plt.xlim(2.1, -0.1)
    ax.errorbar(redshifts, slopes, yerr=error, fmt='-o')
    ax.set_xlabel('Redshift')
    ax.set_ylabel('Slope')
    ax.set_title('Gráfico redshift x slope')
    plt.savefig('Results/redshift x slope.png', bbox_inches='tight')
    plt.show()

    
def print_error_chart_z_size(redshifts, size, error):
    fig, ax = plt.subplots()
    plt.xlim(2.1, -0.1)
    ax.errorbar(redshifts, size, yerr=error, fmt='-o')
    ax.set_xlabel('Redshift')
    ax.set_ylabel('N_Vermelhas/N_Total')
    ax.set_title('Gráfico redshift x N_Vermelhas/N_Total')
    plt.savefig('Results/redshift x size.png', bbox_inches='tight')
    plt.show()

def print_chart_comp_1(x, y1, y2, y5, y6):
    plt.xlim(0.9, 0.3)

    plt.plot(x, y1, label='Descendentes calculados', marker='.')
    plt.plot(x, y2, label='Descendentes verdadeiros', marker='.')
    plt.plot(x, y5, label='Descendentes calculados média', marker='.')
    plt.plot(x, y6, label='Descendentes verdadeiros média', marker='.')  
    
    plt.xlabel('Redshift') 
    plt.ylabel('Probabilidades') 
    plt.title('Comparativo entre a maior probablidade calculada e a probabilidade do descendente verdadeiro a cada redshift') 
      
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.35), ncol=2)
    plt.savefig('Results/comparativo1.png', bbox_inches='tight')
    plt.show()
    
def print_chart_comp_2(x, y3, y4, y7, y8):
    plt.xlim(0.7, 0.33)
    
    plt.plot(x, y3, label='Descendentes calculados', marker='.') 
    plt.plot(x, y4, label='Descendentes verdadeiros', marker='.') 
    plt.plot(x, y7, label='Descendentes calculados média', marker='.')
    plt.plot(x, y8, label='Descendentes verdadeiros média', marker='.')  
    
    plt.xlabel('Redshift') 
    plt.ylabel('Probabilidades') 
    plt.title('Comparativo entre a maior probablidade calculada e a probabilidade do descendente verdadeiro a cada redshift') 
      
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.35), ncol=2)
    plt.savefig('Results/comparativo2.png', bbox_inches='tight')
    plt.show()
    
def print_chart_comp_1_all(x, ys, mass_log_msun, case):
    plt.xlim(0.9, 0.3)
    # plt.xlim(0.55, -0.05)

    for halo_id in ys:
        plt.plot(x, ys[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$)', marker='.')

    plt.xlabel('Redshift') 
    plt.ylabel('Probabilidades') 
    
    if (case==0):
        plt.title('Comparativo entre as médias das maiores probablidades calculadas para cada halo em diferentes redshifts')
    else:
        plt.title('Comparativo entre as médias das probabilidades do descendente verdadeiro para cada halo em diferentes redshifts') 
      
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.65), ncol=2)
    
    if (case==0):
        plt.savefig('Results/comparativo1allmaior.png', bbox_inches='tight')
    else:
        plt.savefig('Results/comparativo1allverdadeiro.png', bbox_inches='tight')
        
    plt.show()
    
def print_chart_comp_2_all(x, ys, mass_log_msun, case):
    plt.xlim(0.7, 0.33)
    
    for halo_id in ys:
        plt.plot(x, ys[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$)', marker='.')
    
    plt.xlabel('Redshift') 
    plt.ylabel('Probabilidades') 
   
    if (case==0):
        plt.title('Comparativo entre as médias das maiores probablidades calculadas para cada halo em diferentes redshifts')
    else:
        plt.title('Comparativo entre as médias das probabilidades do descendente verdadeiro para cada halo em diferentes redshifts') 
      
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.65), ncol=2)
    
    if (case==0):
        plt.savefig('Results/comparativo2allmaior.png', bbox_inches='tight')
    else:
        plt.savefig('Results/comparativo2allverdadeiro.png', bbox_inches='tight')
        
    plt.show()
    
def print_chart_comp_ndp_x_rg(x, y_ndp, y_rg, mass_log_msun, case):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\ndp_x_rg'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    for halo_id in y_ndp:
        plt.xlim(0.88, -0.05)
        
        plt.plot(x, y_ndp[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP', marker='.')
        plt.plot(x, y_rg[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG', marker='.')

        plt.xlabel('Redshift') 
        plt.ylabel('Probabilidades') 
        
        if (case==0):
            plt.title('Comparativo entre as médias das maiores probablidades calculadas por cada método para um halo em diferentes redshifts')
        else:
            plt.title('Comparativo entre as médias das probabilidades do descendente verdadeiro calculadas por cada método\npara um halo em diferentes redshifts') 
          
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)
        
        if (case==0):
            plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/ndp_x_rg/comparativo_ndp_x_rg_maior_halo_'+str(halo_id)+'.png', bbox_inches='tight')
        else:
            plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/ndp_x_rg/comparativo_ndp_x_rg_verdadeiro_halo_'+str(halo_id)+'.png', bbox_inches='tight')
            
        plt.show()
        
def print_chart_comp_sfr(x, y_true, y_ndp, y_rg, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_2\\set_1'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    for halo_id in y_ndp:
        plt.xlim(0.88, -0.05)

        plt.plot(x, y_true[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) True', marker='.')
        plt.plot(x, y_ndp[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP', marker='.')
        plt.plot(x, y_rg[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG', marker='.')

        plt.xlabel('Redshift') 
        plt.ylabel('SFR médio ($M_\odot/yr$)') 
    
        plt.title('Comparativo entre o SFR médio das galáxias de um halo calculado com cada método em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_2/set_1/comparativo_sfr_halo_'+str(halo_id)+'.png', bbox_inches='tight')
        plt.show()
        
def print_chart_comp_sfr_central(x, sfr_true_central, sfr_ndp_central, sfr_rg_central, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_2\\set_1'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    for halo_id in sfr_true_central:
        plt.xlim(0.88, -0.05)

        plt.plot(x, sfr_true_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) True Central', marker='.')
        plt.plot(x, sfr_ndp_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP Central', marker='.')
        plt.plot(x, sfr_rg_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG Central', marker='.')
        
        plt.xlabel('Redshift') 
        plt.ylabel('SFR médio ($M_\odot/yr$)') 
    
        plt.title('Comparativo entre o SFR médio das galáxias no centro de um halo calculado com cada método em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_2/set_1/comparativo_sfr_halo_'+str(halo_id)+'_central.png', bbox_inches='tight')
        plt.show()
        
def print_chart_comp_sfr_periphery(x, sfr_true_periphery, sfr_ndp_periphery, sfr_rg_periphery, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_2\\set_1'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    for halo_id in sfr_true_periphery:
        plt.xlim(0.88, -0.05)

        plt.plot(x, sfr_true_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) True Periphery', marker='.')
        plt.plot(x, sfr_ndp_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP Periphery', marker='.')
        plt.plot(x, sfr_rg_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG Periphery', marker='.')
        
        plt.xlabel('Redshift') 
        plt.ylabel('SFR médio ($M_\odot/yr$)')  
    
        plt.title('Comparativo entre o SFR médio das galáxias na periferia de um halo calculado com cada método em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_2/set_1/comparativo_sfr_halo_'+str(halo_id)+'_periphery.png', bbox_inches='tight')
        plt.show()
        
def print_chart_comp_true(x, sfr_true_central, sfr_true_periphery, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_2\\set_2'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    for halo_id in sfr_true_central:
        plt.xlim(0.88, -0.05)

        plt.plot(x, sfr_true_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) Central', marker='.')
        plt.plot(x, sfr_true_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) Periphery', marker='.')

        plt.xlabel('Redshift') 
        plt.ylabel('SFR médio ($M_\odot/yr$)')  
    
        plt.title('Comparativo entre o SFR médio das galáxias de um halo em diferentes redshifts com base no IllustrisTNG')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_2/set_2/comparativo_sfr_halo_'+str(halo_id)+'_true.png', bbox_inches='tight')
        plt.show()
        
def print_chart_comp_ndp(x, sfr_ndp_central, sfr_ndp_periphery, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_2\\set_2'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    for halo_id in sfr_ndp_central:
        plt.xlim(0.88, -0.05)

        plt.plot(x, sfr_ndp_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) Central', marker='.')
        plt.plot(x, sfr_ndp_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) Periphery', marker='.')

        plt.xlabel('Redshift') 
        plt.ylabel('SFR médio ($M_\odot/yr$)')  
    
        plt.title('Comparativo entre o SFR médio das galáxias de um halo calculado com o NDpredict em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_2/set_2/comparativo_sfr_halo_'+str(halo_id)+'_ndp.png', bbox_inches='tight')
        plt.show()
        
def print_chart_comp_rg(x, sfr_rg_central, sfr_rg_periphery, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_2\\set_2'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    for halo_id in sfr_rg_central:
        plt.xlim(0.88, -0.05)

        plt.plot(x, sfr_rg_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) Central', marker='.')
        plt.plot(x, sfr_rg_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) Periphery', marker='.')

        plt.xlabel('Redshift') 
        plt.ylabel('SFR médio ($M_\odot/yr$)')  
    
        plt.title('Comparativo entre o SFR médio das galáxias de um halo calculado com o RG em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_2/set_2/comparativo_sfr_halo_'+str(halo_id)+'_rg.png', bbox_inches='tight')
        plt.show()
        
def print_chart_comp_sfr_central_x_periphery(x, y_ndp_central, y_ndp_periphery, y_rg_central, y_rg_periphery, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_1'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    for halo_id in y_ndp_central:
        plt.xlim(0.88, -0.05)

        plt.plot(x, y_ndp_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP Central', marker='.')
        plt.plot(x, y_rg_central[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG Central', marker='.')
        plt.plot(x, y_ndp_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP Periphery', marker='.')
        plt.plot(x, y_rg_periphery[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG Periphery', marker='.')
        
        plt.xlabel('Redshift') 
        plt.ylabel('Porcentagem') 
    
        plt.title('Comparativo entre a porcentagem média da diferença entre o valor calculado e o real do SFR\npara um halo em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_1/comparativo_sfr_central_x_periphery_halo_'+str(halo_id)+'.png', bbox_inches='tight')
        plt.show()
    
def print_chart_comp_sfr_percent(x, y_ndp, y_rg, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\sfr\\method_1'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    for halo_id in y_ndp:
        plt.xlim(0.88, -0.05)

        plt.plot(x, y_ndp[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP', marker='.')
        plt.plot(x, y_rg[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG', marker='.')

        plt.xlabel('Redshift') 
        plt.ylabel('Porcentagem') 
    
        plt.title('Comparativo entre a porcentagem média da diferença entre o valor calculado e o real do SFR\npara um halo em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/sfr/method_1/comparativo_sfr_halo_'+str(halo_id)+'_percent.png', bbox_inches='tight')
        plt.show()
    
def print_chart_comp_gp(x, gp, mass_log_msun, exe_num):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    plt.xlim(0.88, -0.05)

    for halo_id in gp:
        plt.plot(x, gp[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$)', marker='.')

    plt.xlabel('Redshift') 
    plt.ylabel('Ganho/perda') 

    plt.title('Comparativo entre os ganhos/perdas para cada halo em diferentes redshifts')
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2) #Para dois halos
    # plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.65), ncol=2) #Para dez halos
    plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/comparativo_gp_'+str(exe_num)+'.png', bbox_inches='tight')
    plt.show()
    
def print_chart_comp_errors(x, errors_test_ndp, errors_test_rg, mass_log_msun):
    cwd = os.getcwd()
    
    dir_name = cwd+'\\Results\\ndp_x_rg\\'+simulation_name+'\\graphics\\errors'
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    for halo_id in errors_test_ndp:
        plt.xlim(0.88, -0.05)
        
        plt.plot(x, errors_test_ndp[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) NDP', marker='.')
        plt.plot(x, errors_test_rg[halo_id], label='Halo '+str(halo_id)+' ('+str(mass_log_msun[halo_id])+' $log(M_\odot)$) RG', marker='.')

        plt.xlabel('Redshift') 
        plt.ylabel('Taxa de acerto') 
    
        plt.title('Comparativo entre as taxas de acerto dos métodos para um halo em diferentes redshifts')
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)
        plt.savefig('Results/ndp_x_rg/'+simulation_name+'/graphics/errors/comparativo_taxa_de_acerto_halo_'+str(halo_id)+'.png', bbox_inches='tight')
        plt.show()
    
def print_chart_comp_comb(x, kk_gp, loop_gp, liop_gp):
    plt.plot(x, kk_gp, label='KK', marker='.')
    plt.plot(x, loop_gp, label='LoOP', marker='.')
    plt.plot(x, liop_gp, label='LiOP', marker='.')  
    
    plt.xlabel('Valores dos pesos') 
    plt.ylabel('$\Delta P$') 
    plt.title('Comparativo entre os métodos de combinação') 
      
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=3)
    plt.savefig('Results/comparativo_comb.png', bbox_inches='tight')
    plt.show()
    
def print_chart_comp_comb_method(x, method_gp, name):
    plt.plot(x, method_gp, label=name, marker='.')
    
    plt.xlabel(r'$\beta _1$') 
    plt.ylabel('$\Delta P$') 
    plt.title(r'Variação de $\beta _1$ para o método '+name) 
      
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=3)
    plt.savefig('Results/comparativo_comb_'+name+'.png', bbox_inches='tight')
    plt.show()