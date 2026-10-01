import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import pytest

from build_features import calculate_daily_return
def test_daily_return_on_constant_series():
    rates=pd.Series([1.0,1.0,1.0,1.0])
    result=calculate_daily_return(rates)
    assert result.iloc[1]==0.0
    assert result.iloc[2]==0.0
    assert result.iloc[3]==0.0

def test_daily_return_on_known_values():
    rates=pd.Series([100.0,110.0,99.0])
    result=calculate_daily_return(rates)

    assert result.iloc[1]==pytest.approx(0.1)
    assert result.iloc[2]==pytest.approx(-0.1)
def test_daily_return_length_matches_point():
    rates=pd.Series([1.0,2.0,3.0,4.0,5.0])
    result=calculate_daily_return(rates)

    assert len(result)==len(rates)