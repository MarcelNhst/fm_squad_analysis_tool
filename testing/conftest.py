import pytest
import pandas as pd

@pytest.fixture(scope='session')
def df_raw():
    return pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10], 'Cmp': [14, 1], 'Str': [12, 15], 'Mar': [8, 6], 'Tck': [-1, -20]})