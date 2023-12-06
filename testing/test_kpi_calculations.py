import pandas as pd
import sys
from pandas.testing import assert_frame_equal
import pytest
sys.path.append('H:/Python_Projects/fm_squad_analysis_tool/src/')

import kpi_calculations



def test_basic_kpi_calculations_essential(df_raw):
    df1 = pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10], 'Spd': [15.0, 5.0]})
    df2 = df_raw

    df2['Spd'] = kpi_calculations.calculate_kpi_score(df2, ['Acc', 'Pac'], [], [])
    df2 = df2[['Acc', 'Pac', 'Spd']]


    assert_frame_equal(df1, df2)

def test_basic_kpi_calculations_core(df_raw):
    df1 = pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10], 'Spd': [15.0, 5.0]})
    df2 = df_raw

    df2['Spd'] = kpi_calculations.calculate_kpi_score(df2, [], ['Acc', 'Pac'], [])
    df2 = df2[['Acc', 'Pac', 'Spd']]


    assert_frame_equal(df1, df2)


def test_basic_kpi_calculations_secondary(df_raw):
    df1 = pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10], 'Spd': [15.0, 5.0]})
    df2 = df_raw

    df2['Spd'] = kpi_calculations.calculate_kpi_score(df2, [], [], ['Acc', 'Pac'])
    df2 = df2[['Acc', 'Pac', 'Spd']]


    assert_frame_equal(df1, df2)
    
def test_kpi_calculations(df_raw):
    df1 = pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10], 'Kpi': [13.3, 3.7]})
    df2 = df_raw

    df2['Kpi'] = kpi_calculations.calculate_kpi_score(df2, ['Cmp', 'Acc'], ['Pac'], ['Str', 'Mar'])
    df2 = df2[['Acc', 'Pac', 'Kpi']]


    assert_frame_equal(df1, df2)  
    
def test_negative_kpi_calculations(df_raw):
    df1 = pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10], 'Kpi': [7, -7.1]})
    df2 = df_raw

    df2['Kpi'] = kpi_calculations.calculate_kpi_score(df2, ['Tck'], ['Pac'], ['Mar'])
    df2 = df2[['Acc', 'Pac', 'Kpi']]


    assert_frame_equal(df1, df2)     

def test_empty_kpi_calculations(df_raw):
    df2 = df_raw

    with pytest.raises(Exception):
        df2['Kpi'] = kpi_calculations.calculate_kpi_score(df2, [], [], [])