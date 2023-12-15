import logging

def calculate_kpi_score(df, essential, core, secondary):
    """
    Calculate a Key Performance Indicator (KPI) score based on the provided DataFrame and attribute lists.

    The KPI score is calculated by assigning different weights to essential, core, and secondary attributes
    in the DataFrame. The weights are 5 for essential attributes, 3 for core attributes, and 1 for secondary attributes.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - essential (list): A list of essential attributes used for KPI calculation.
    - core (list): A list of core attributes used for KPI calculation.
    - secondary (list): A list of secondary attributes used for KPI calculation.

    Returns:
    - float: The calculated KPI score.

    Raises:
    - Exception: If the total number of fields for KPI calculation is zero.
    """
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
    """
    Calculate a custom Key Performance Indicator (KPI) score based on the provided DataFrame and attribute lists.

    The KPI score is calculated by assigning different weights to essential, core, secondary, and tertiary attributes
    in the DataFrame. The weights are 5 for essential attributes, 3 for core attributes, 2 for secondary attributes,
    and 1 for tertiary attributes.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - essential (list): A list of essential attributes used for KPI calculation.
    - core (list): A list of core attributes used for KPI calculation.
    - secondary (list): A list of secondary attributes used for KPI calculation.
    - tertiary (list): A list of tertiary attributes used for KPI calculation.

    Returns:
    - float: The calculated custom KPI score.

    Raises:
    - Exception: If the total number of fields for KPI calculation is zero.
    """
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