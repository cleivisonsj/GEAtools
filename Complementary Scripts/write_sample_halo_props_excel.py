import GEAtools as geat
import illustris_python as il
import xlsxwriter
import os

cwd = os.getcwd()
dir_name = cwd+'\\Results'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

workbook = xlsxwriter.Workbook('Results/props_halos.xlsx')

def write_halos_sample_props(snaps, simulations_data):
    for snap_num in snaps:
        i = 0
        j = 0
        
        worksheet = workbook.add_worksheet('Snap='+str(snap_num))
        worksheet.set_column('A:E', 20)

        for simulation_name in list(simulations_data.keys()):
            base_path = './'+simulation_name+'/output/'
            
            for halo_id in simulations_data[simulation_name]:
                worksheet.write(0+j, 0, 'Simulação: '+simulation_name)
                worksheet.write(1+j, 0, 'HaloID')
                worksheet.write(1+j, 1, 'Massa log(Msun)')
                worksheet.write(1+j, 2, 'Quant subhalos')
                worksheet.write(1+j, 3, 'Quant subhalos corte')
                worksheet.write(1+j, 4, 'Group_R_Crit200')
                
                halo = il.groupcat.loadSingle(base_path,snap_num,haloID=halo_id)
                count_subhalo_cut = 0

                for subhalo_id in range(halo['GroupFirstSub'],halo['GroupFirstSub']+halo['GroupNsubs']):
                    subhalo = il.groupcat.loadSingle(base_path,snap_num,subhaloID=subhalo_id)
                    subhalo_mass_stars = subhalo['SubhaloMassType'][4]
                    subhalo_mass = subhalo['SubhaloMass']
                         
                    if (subhalo_mass_stars>0 and ((subhalo_mass*(1e10/0.6774))>=1e9)):
                        count_subhalo_cut += 1
                             
                mass_halo_log_msun = geat.convert_mass_to_log_msun(halo['GroupMass'])
                             
                worksheet.write(2+i, 0, halo_id)
                worksheet.write(2+i, 1, round(mass_halo_log_msun, 4))
                worksheet.write(2+i, 2, halo['GroupNsubs'])
                worksheet.write(2+i, 3, count_subhalo_cut)
                worksheet.write(2+i, 4, round(halo['Group_R_Crit200'], 4))
                    
                i += 1
                
            j = 3 + i + 1
            i = j
        
snaps = [50, 55, 65, 80, 99]
# snaps = [50]
simulations_data = {'TNG100-3': range(0,50), 'TNG100-2': range(0,10), 'TNG100-1': range(0,2)}

write_halos_sample_props(snaps, simulations_data)
    
workbook.close()