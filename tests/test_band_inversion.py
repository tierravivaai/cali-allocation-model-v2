import duckdb
import pandas as pd
from logic.data_loader import load_data, get_base_data
from logic.calculator import calculate_allocations

def test_band_inversion_completeness():
    con = duckdb.connect(database=':memory:')
    load_data(con)
    df = get_base_data(con)
    
    # Run with band inversion
    res = calculate_allocations(df, 1_000_000_000, 50, un_scale_mode="band_inversion")
    
    eligible = res[res['eligible']]
    
    # Check that every eligible country has a band assigned
    assert eligible['un_band'].notna().all(), "Some eligible countries have no band assigned"
    
    # Check that every eligible country has a band weight assigned
    assert eligible['un_band_weight'].notna().all(), "Some eligible countries have no band weight assigned"
    
    # Check that shares sum to 1.0 (approximately)
    assert abs(eligible['iusaf_share'].sum() - 1.0) < 1e-10
    
def test_band_inversion_values():
    con = duckdb.connect(database=':memory:')
    load_data(con)
    df = get_base_data(con)
    
    # Band 1: <= 0.001 (Weight 1.50)
    # Band 5: > 1.0 (Weight 0.75)
    res = calculate_allocations(df, 1_000_000_000, 50, un_scale_mode="band_inversion")
    
    gb = res[res['party'].str.contains('Guinea-Bissau', case=False)].iloc[0]
    assert gb['un_share'] <= 0.001
    assert gb['un_band_weight'] == 1.50
    
    china = res[res['party'].str.contains('China', case=False)].iloc[0]
    assert china['un_share'] > 1.0
    assert china['un_band_weight'] == 0.75

if __name__ == "__main__":
    test_band_inversion_completeness()
    test_band_inversion_values()
    print("Band inversion tests passed!")
