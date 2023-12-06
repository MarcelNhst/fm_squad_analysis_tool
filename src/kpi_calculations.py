import logging

def calculate_kpi_score(df, essential, core, secondary):
    score = 0
    div = len(essential) * 5 + len(core) * 3 + len(secondary)
    if div == 0:
        raise Exception("Number of fields for KPI calculation cannot be zero")
    
    for i in essential:
        logging.info('Processing essential attribute ' + i)
        score = score + (df[i] * 5)
        
    for i in core:
        logging.info('Processing core attribute ' + i)
        score = score + (df[i] * 3)
        
    for i in secondary:
        logging.info('Processing secondary attribute ' + i)
        score = score + (df[i])
    
    logging.info('Done with KPI')
    return round(score/div, 1)



def calculate_custom_kpi_score(df, essential, core, secondary, tertiary):
    score = 0
    div = len(essential) * 5 + len(core) * 3 + len(secondary) * 2 + len(tertiary)
    if div == 0:
        raise Exception("Number of fields for KPI calculation cannot be zero")
    
    for i in essential:
        logging.info('Processing essential attribute ' + i)
        score = score + (df[i] * 5)
        
    for i in core:
        logging.info('Processing core attribute ' + i)
        score = score + (df[i] * 3)
        
    for i in secondary:
        logging.info('Processing secondary attribute ' + i)
        score = score + (df[i] * 2)
        
    for i in tertiary:
        logging.info('Processing tertiary attribute ' + i)
        score = score + (df[i])
    
    logging.info('Done with KPI')
    return round(score/div, 1)