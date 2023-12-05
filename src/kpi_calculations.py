
def calculate_kpi_score(df, essential, core, secondary):
    score = 0
    div = len(essential) * 5 + len(core) * 3 + len(secondary)
    if div == 0:
        raise Exception("Number of fields for KPI calculation cannot be zero")
    
    for i in essential:
        score = score + (df[i] * 5)
        
    for i in core:
        score = score + (df[i] * 3)
        
    for i in secondary:
        score = score + (df[i])
    
    return round(score/div, 1)



def calculate_custom_kpi_score(df, essential, core, secondary, tertiary):
    score = 0
    div = len(essential) * 5 + len(core) * 3 + len(secondary) * 2 + len(tertiary)
    if div == 0:
        raise Exception("Number of fields for KPI calculation cannot be zero")
    
    for i in essential:
        score = score + (df[i] * 5)
        
    for i in core:
        score = score + (df[i] * 3)
        
    for i in secondary:
        score = score + (df[i] * 2)
        
    for i in tertiary:
        score = score + (df[i])
    
    return round(score/div, 1)