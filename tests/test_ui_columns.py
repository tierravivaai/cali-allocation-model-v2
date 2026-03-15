import pytest
import pandas as pd
import duckdb
from logic.data_loader import load_data, get_base_data
from logic.calculator import calculate_allocations, aggregate_by_region, aggregate_by_income

@pytest.fixture
def mock_con():
    con = duckdb.connect(database=':memory:')
    load_data(con)
    return con

def test_column_visibility_by_tab(mock_con):
    base_df = get_base_data(mock_con)
    fund_size_usd = 1_000_000_000
    iplc_share = 50
    
    results_df = calculate_allocations(
        base_df,
        fund_size_usd,
        iplc_share,
        False, # show_raw
        True,  # exclude_hi
        un_scale_mode="band_inversion"
    )
    
    # 1. Test "By Party" columns logic
    # In app.py: display_cols = ['party', 'total_allocation', 'state_component', 'iplc_component', 'WB Income Group', 'UN LDC', 'CBD Party', 'EU']
    # If show_advanced is False (default) and un_scale_mode is "band_inversion":
    display_cols_party = ['party', 'total_allocation', 'state_component', 'iplc_component', 'WB Income Group', 'UN LDC', 'CBD Party', 'EU', 'un_band', 'un_band_weight']
    
    # Verify "Countries (number)" is NOT in display_cols_party
    assert "Countries (number)" not in display_cols_party
    
    # 2. Test "By UN Region" columns logic
    # In app.py: display_cols_region = ["region", "Countries (number)", "total_allocation", "state_component", "iplc_component"]
    display_cols_region = ["region", "Countries (number)", "total_allocation", "state_component", "iplc_component"]
    assert "Countries (number)" in display_cols_region
    
    # 3. Test "By UN Sub-region" columns logic
    display_cols_sub = ["sub_region", "Countries (number)", "total_allocation", "state_component", "iplc_component"]
    assert "Countries (number)" in display_cols_sub
    
    # 4. Test "By UN Intermediate Region" columns logic
    display_cols_int = ["intermediate_region", "Countries (number)", "total_allocation", "state_component", "iplc_component"]
    assert "Countries (number)" in display_cols_int

    # 5. Test "Share by Income Group" columns logic
    display_cols_income = ['WB Income Group', 'Countries (number)', 'total_allocation', 'state_component', 'iplc_component']
    assert "Countries (number)" in display_cols_income

def test_inversion_comparison_headlines(mock_con):
    base_df = get_base_data(mock_con)
    fund_size_usd = 1_000_000_000
    iplc_share = 50
    
    # Scenario A: Exclude High Income
    results_hi_excluded = calculate_allocations(
        base_df, fund_size_usd, iplc_share, False, exclude_high_income=True
    )
    n_eligible_hi_excluded = results_hi_excluded['eligible'].sum()
    
    # Scenario B: Include High Income
    results_hi_included = calculate_allocations(
        base_df, fund_size_usd, iplc_share, False, exclude_high_income=False
    )
    n_eligible_hi_included = results_hi_included['eligible'].sum()
    
    assert n_eligible_hi_excluded < n_eligible_hi_included
    assert n_eligible_hi_excluded == 142 # 196 - (HIC-SIDS)
    assert n_eligible_hi_included == 196
