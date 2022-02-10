import math
import os
import numpy as np
from .tools_writing import write_dists
from .config import R_HOME
from .config import R_USER

#import os
#os.environ['R_HOME'] = R_HOME
#os.environ['R_USER'] = R_USER

os.environ['R_HOME'] = R_HOME
os.environ['R_USER'] = R_USER

from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri, Formula, FloatVector

"""
#Instalar pacotes do R

from rpy2.robjects.packages import importr
utils = importr('utils')
utils.install_packages('multimode')
utils.install_packages('cdfquantreg')
"""

show_graphics = False
save_graphics = True
save_dists = False

def calc_dist_point_and_line(x, y, a, b, c):
    return abs((a*x+b*y+c))/(math.sqrt(math.pow(a, 2)+math.pow(b, 2)))

def calc_dist_sample(sample, a, b, c, color_str, mag_str):
    dist = {}
    
    for i in range(0, len(sample)):
        x = sample[mag_str][i]
        y = sample[color_str][i]
        
        dist[sample['id'][i]] = calc_dist_point_and_line(x, y, a, b, c)
        
    return dist
    
def calc_prob_rg(filters, zf):
    pandas2ri.activate()
    
    multimode = importr('multimode')
    base = importr('base')
    MASS = importr('MASS')
    stats = importr('stats')
    graphics = importr('graphics')
    grdevices = importr('grDevices')
    plyr = importr('plyr')
    cdfquantreg = importr('cdfquantreg')

    R_filters_df = pandas2ri.py2rpy(filters)

    color = R_filters_df.rx2('filter_g_r')
    mag = R_filters_df.rx2('filter_r')
    color_str = 'filter_g_r'
    mag_str = 'filter_r'
    color_graph_str = '(g-r)'
    mag_graph_str = 'M[r]'
    
    
    # color = R_filters_df.rx2('filter_r_i')
    # mag = R_filters_df.rx2('filter_i')
    # color_str = 'filter_r_i'
    # mag_str = 'filter_i'
    # color_graph_str = '(r-i)'
    # mag_graph_str = 'M[i]'


    # color = R_filters_df.rx2('filter_i_z')
    # mag = R_filters_df.rx2('filter_z')
    # color_str = 'filter_i_z'
    # mag_str = 'filter_z'
    # color_graph_str = '(i-z)'
    # mag_graph_str = 'M[z]'

    # if (zf<=0.33):
    #     color = R_filters_df.rx2('filter_g_r')
    #     mag = R_filters_df.rx2('filter_r')
    #     color_str = 'filter_g_r'
    #     mag_str = 'filter_r'
    #     color_graph_str = '(g-r)'
    #     mag_graph_str = 'M[r]'
    # elif (zf<=0.7):
    #     color = R_filters_df.rx2('filter_r_i')
    #     mag = R_filters_df.rx2('filter_i')
    #     color_str = 'filter_r_i'
    #     mag_str = 'filter_i'
    #     color_graph_str = '(r-i)'
    #     mag_graph_str = 'M[i]'
    # else:
    #     color = R_filters_df.rx2('filter_i_z')
    #     mag = R_filters_df.rx2('filter_z')
    #     color_str = 'filter_i_z'
    #     mag_str = 'filter_z'
    #     color_graph_str = '(i-z)'
    #     mag_graph_str = 'M[z]'

    modes = multimode.locmodes(color, mod0=2, display=show_graphics)
    
    if (save_graphics):
        grdevices.pdf(file='Results/modes.pdf')
        multimode.locmodes(color, mod0=2, display=True)
        grdevices.dev_off()
    
    #mode1 = modes.rx2('locations')[0]
    mode2 = modes.rx2('locations')[2]
    antimode = modes.rx2('locations')[1]
    
    red = base.subset(R_filters_df, color>antimode)
    blue = base.subset(R_filters_df, color<=antimode)

    #Regressão linear
    subred1 = base.subset(red, red[mag_str]>=-21.0)
    subred2 = base.subset(red, red[mag_str]<-21.0)
    subred3 = base.subset(subred2, subred2[color_str]>=mode2)
    
    subred_aux = base.rbind(subred1, subred3)
    subred = plyr.arrange(subred_aux, subred_aux['id'])
    
    fmla = Formula('y ~ x')
    env = fmla.environment
    env['y'] = subred[color_str]
    env['x'] = subred[mag_str]
    
    lr_cormag = MASS.rlm(fmla, data=subred)
    
    #stats.predict(lr_cormag, subred, True)
    
    pred_w_plim = base.data_frame(stats.predict(lr_cormag, subred, interval='prediction', level=0.68))
    
    if (show_graphics):
        graphics.plot(mag, color, xlim=base.c(-25,-13), col='white', xlab=base.parse(text=base.paste0(mag_graph_str)), ylab=base.parse(text=base.paste0(color_graph_str)), cex_lab=1.25)
        graphics.points(red[mag_str], red[color_str], pch=20, col='red', cex=1.1)
        graphics.points(blue[mag_str], blue[color_str],pch=20,col="blue", cex=1.1)
        graphics.abline(v=-21, lty=2, col='gray')
        graphics.points(subred[mag_str], pred_w_plim['X1'], col='red', t='l')
        graphics.points(subred[mag_str], pred_w_plim['X2'], col='red', t='l', lty=2)
        graphics.points(subred[mag_str], pred_w_plim['X3'], col='red', t='l', lty=2)
    
    #Redefinindo as amostras
    red_sample = base.subset(subred, subred[color_str]>=pred_w_plim['X2'])
    green_sample1 = base.subset(subred, subred[color_str]<pred_w_plim['X2'])
    green_sample2 = base.subset(red, red[color_str]<mode2)
    green_sample3 = base.subset(green_sample2, green_sample2[mag_str]<-21)
    green_sample = base.rbind(green_sample1, green_sample3)
    
    if (show_graphics):
        graphics.plot(mag, color, xlim=base.c(-25,-13), col='white', xlab=base.parse(text=base.paste0(mag_graph_str)), ylab=base.parse(text=base.paste0(color_graph_str)), cex_lab=1.25)
        graphics.points(red[mag_str], red[color_str], pch=20, col='purple', cex=1.1)
        graphics.points(red_sample[mag_str], red_sample[color_str], pch=20, col='red', cex=1.1)
        graphics.points(green_sample[mag_str], green_sample[color_str], pch=20, col='green', cex=1.1)
        graphics.points(blue[mag_str], blue[color_str], pch=20, col="blue", cex=1.1)
        graphics.points(subred[mag_str], pred_w_plim['X1'], col='red', t='l')
        graphics.points(subred[mag_str], pred_w_plim['X2'], col='red', t='l', lty=2)
        graphics.points(subred[mag_str], pred_w_plim['X3'], col='red', t='l', lty=2)
    
    #Salvando os gráficos
    if (save_graphics):
        grdevices.pdf(file='Results/modes.pdf')
        multimode.locmodes(color, mod0=2, display=True)
        grdevices.dev_off()
        
        grdevices.pdf(file='Results/regression.pdf')
        graphics.plot(mag, color, xlim=base.c(-25,-13), col='white', xlab=base.parse(text=base.paste0(mag_graph_str)), ylab=base.parse(text=base.paste0(color_graph_str)), cex_lab=1.25)
        graphics.points(red[mag_str], red[color_str], pch=20, col='purple', cex=1.1)
        graphics.points(red_sample[mag_str], red_sample[color_str], pch=20, col='red', cex=1.1)
        graphics.points(green_sample[mag_str], green_sample[color_str], pch=20, col='green', cex=1.1)
        graphics.points(blue[mag_str], blue[color_str], pch=20, col="blue", cex=1.1)
        graphics.points(subred[mag_str], pred_w_plim['X1'], col='red', t='l')
        graphics.points(subred[mag_str], pred_w_plim['X2'], col='red', t='l', lty=2)
        graphics.points(subred[mag_str], pred_w_plim['X3'], col='red', t='l', lty=2)
        grdevices.dev_off()
    
    #Calcular as distâncias entre os pontos e a reta de regressão
    #y = slope*x + intercept => slope*x - y + intercept = 0
    #Distancia entre ponto e reta
    #a*xp+b*yp+c/sqrt(a^2+b^2)
    #a = slope
    #b = -1
    #c = intercept
    
    a = lr_cormag.rx2('coefficients')[1]
    b = -1
    c = lr_cormag.rx2('coefficients')[0]
    
    dist_r = calc_dist_sample(red_sample, a, b, c, color_str, mag_str)
    dist_g = calc_dist_sample(green_sample, a, b, c, color_str, mag_str)
    dist_b = calc_dist_sample(blue, a, b, c, color_str, mag_str)
    
    dists = dict(list(dist_r.items())+list(dist_g.items())+list(dist_b.items()))
    
    #dict(sorted(dists.items()))
    
    #Method 1
    lr_summary = base.summary(lr_cormag)
    sigma_intercept = lr_summary.rx2('coefficients')[0][1]
    sigma_slope = lr_summary.rx2('coefficients')[1][1]
    
    sigma_int_2 = math.pow(0.05, 2)
    sigma_proj_2 = math.pow(sigma_intercept, 2) + math.pow(sigma_slope, 2)
    sigma_col_2 = sigma_int_2 + sigma_proj_2
    
    dists_scaled = {}

    for key in dists:
        dists_scaled[key] = math.exp(-(pow(dists[key], 2)/(2*sigma_col_2)))
        
    #Method 2
    # R_dists = FloatVector(list(dists.values()))
    # dists_scaled_vector = cdfquantreg.scaleTR(R_dists)
    
    # dists_scaled = {}
    # i = 0
    
    # for key in dists:
    #     dists_scaled[key] = 1-dists_scaled_vector[i]
    #     i += 1
    
    if (save_dists):
        write_dists(dist_r, red_sample, dist_g, green_sample, dist_b, blue, dists_scaled, a, c)
    
    return dists_scaled

def calc_coef_rg(filters, snap, z):
    coef = {}
    
    pandas2ri.activate()
    
    multimode = importr('multimode')
    base = importr('base')
    MASS = importr('MASS')
    stats = importr('stats')
    graphics = importr('graphics')
    grdevices = importr('grDevices')
    plyr = importr('plyr')
    #cdfquantreg = importr('cdfquantreg')

    R_filters_df = pandas2ri.py2rpy(filters)
    
    color = R_filters_df.rx2('filter_g_r')
    mag = R_filters_df.rx2('filter_r')

    if (len(color)>1):
        modes = multimode.locmodes(color, mod0=2, display=show_graphics)
        
        #mode1 = modes.rx2('locations')[0]
        mode2 = modes.rx2('locations')[2]
        antimode = modes.rx2('locations')[1]
        total_sample = len(color)
        error_modes = modes.rx2("cbw").rx2("bw")[0]
        
        red = base.subset(R_filters_df, color>antimode)
        blue = base.subset(R_filters_df, color<=antimode)
        
        #Regressão linear
        subred1 = base.subset(red, red['filter_r']>=-21.0)
        subred2 = base.subset(red, red['filter_r']<-21.0)
        subred3 = base.subset(subred2, subred2['filter_g_r']>=mode2)
        
        subred_aux = base.rbind(subred1, subred3)
        subred = plyr.arrange(subred_aux, subred_aux['id'])
    
        is_all_zero = not np.any(subred['filter_r'])
        
        if (len(subred['filter_r'])>1 and not is_all_zero):
            fmla = Formula('y ~ x')
            env = fmla.environment
            env['y'] = subred['filter_g_r']
            env['x'] = subred['filter_r']
            
            lr_cormag = MASS.rlm(fmla, data=subred)
            total_red = len(subred)
            error_lr = lr_cormag.rx2('s')[0]
            
            #stats.predict(lr_cormag, subred, True)
            
            pred_w_plim = base.data_frame(stats.predict(lr_cormag, subred, interval='prediction', level=0.68))
            
            #Redefinindo as amostras
            red_sample = base.subset(subred, subred['filter_g_r']>=pred_w_plim['X2'])
            green_sample1 = base.subset(subred, subred['filter_g_r']<pred_w_plim['X2'])
            green_sample2 = base.subset(red, red['filter_g_r']<mode2)
            green_sample3 = base.subset(green_sample2, green_sample2['filter_r']<-21)
            green_sample = base.rbind(green_sample1, green_sample3)
            
            #Salvando os gráficos
            grdevices.png(file='Results/coefs/rg-snap'+str(snap)+'.png')
            graphics.plot(mag, color, main='Snapshot '+str(snap)+' (z='+str(z)+')', xlim=base.c(-25,-13), col='white', xlab=base.parse(text=base.paste0('M[r]')), ylab=base.parse(text=base.paste0('(g-r)')), cex_lab=1.25)
            graphics.points(red['filter_r'], red['filter_g_r'], pch=20, col='purple', cex=1.1)
            graphics.points(red_sample['filter_r'], red_sample['filter_g_r'], pch=20, col='red', cex=1.1)
            graphics.points(green_sample['filter_r'], green_sample['filter_g_r'], pch=20, col='green', cex=1.1)
            graphics.points(blue['filter_r'], blue['filter_g_r'], pch=20, col="blue", cex=1.1)
            graphics.points(subred['filter_r'], pred_w_plim['X1'], col='red', t='l')
            graphics.points(subred['filter_r'], pred_w_plim['X2'], col='red', t='l', lty=2)
            graphics.points(subred['filter_r'], pred_w_plim['X3'], col='red', t='l', lty=2)
            grdevices.dev_off()
            
            a = lr_cormag.rx2('coefficients')[1]
            #b = -1
            c = lr_cormag.rx2('coefficients')[0]
    
            coef['snap'] = snap
            coef['z'] = z
            coef['slope'] = a
            coef['intercept'] = c
            coef['total_sample'] = total_sample
            coef['total_red'] = total_red
            coef['error_modes'] = error_modes
            coef['error_lr'] = error_lr
            
    return coef