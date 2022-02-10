from .tools_aux import adjust_probs_scale

def liop(probs_ndp, probs_rg, b1, b2):
    probs_comb = {}
    
    for key in probs_ndp:
        p1 = probs_ndp[key]
        p2 = probs_rg[key]
        
        #if (str(p1) != 'nan'):
        probs_comb[key] = b1*p1+b2*p2
        
    return probs_comb

def loop(probs_ndp, probs_rg, b1, b2):
    probs_comb = {}
    
    for key in probs_ndp:
        p1 = probs_ndp[key]
        p2 = probs_rg[key]
        
        #if (str(p1) != 'nan'):
        #probs_comb[key] = ((p1**b1)*(p2**b2))/(((p1**b1)*(p2**b2))+((1-p1)**b1)*((1-p2)**b2))
        probs_comb[key] = (p1**b1)*(p2**b2)
        
    return probs_comb

def kk(probs_ndp, probs_rg, b1, b2):
    probs_comb = {}
    
    for key in probs_ndp:
        p1 = probs_ndp[key]
        p2 = probs_rg[key]
        
        #if (str(p1) != 'nan'):
        if (p1==1):
            probs_comb[key] = 1
        else:
            probs_comb[key] = (((p1/(1-p1))**b1)*((p2/(1-p2))**b2))/(1+((p1/(1-p1))**b1)*((p2/(1-p2))**b2))
   
    return probs_comb

def calc_comb(method, probs_ndp, probs_geat, b1, b2):
    if (method=='kk'):
        probs_comb = kk(probs_ndp, probs_geat, b1, b2)

    elif (method=='loop'):
        probs_comb = loop(probs_ndp, probs_geat, b1, b2)
        
    elif (method=='liop'):
        probs_comb = liop(probs_ndp, probs_geat, b1, b2)

    adjust_probs_scale(probs_comb)
    
    return probs_comb