def get_redshifts():
    file = open('Auxiliary Data/redshifts.txt', 'r')
    content = file.readlines()
    
    redshifts_dict = {}
    
    for i in range(len(content)):
        value = float(content[i])
        redshifts_dict[i] = value

    return redshifts_dict

def adjust_probs_scale(probs):
    total = sum(list(probs.values()))
    
    for key in probs:
        probs[key] = probs[key]/total