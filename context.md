# Session Context: TSAC + SOSAC and Negotiation Dashboard

## Changes Implemented

### Data Ingestion
- Integrated World Bank land area data into the master Party table in `logic/data_loader.py`.
- Handled missing land area data for specific parties (Monaco, Cook Islands, Niue, State of Palestine).

### Core Logic
- Implemented a blended allocation formula in `logic/calculator.py`:
  `Final Share = (1 - beta - gamma) * iusaf_share + beta * tsac_share + gamma * sosac_share`
- Added support for TSAC (land area proportional) and SOSAC (SIDS structural adjustment) components.
- Preserved SIDS eligibility in high-income exclusion mode.
- Implemented SOSAC fallback: reallocates to IUSAF if no eligible SIDS are present.

### User Interface
- Added TSAC and SOSAC sliders to the Streamlit sidebar in `app.py`.
- Implemented dynamic interpretation boxes explaining the allocation impact of beta and gamma.
- Created a "Negotiation Dashboard" tab with Plotly visualizations:
  - Winners/Losers metrics and bar charts.
  - Group impact analysis.
  - Country-level waterfall charts.
  - TSAC vs SOSAC sensitivity heatmap.
- Added negotiation presets (Equity Base, Stewardship, Vulnerability, Balanced).
- Fixed tab NameErrors by using dynamic indexing.

### Testing
- Added comprehensive tests in `tests/test_tsac_sosac.py` and `tests/test_negotiator_dashboard.py`.
- Verified all 67+ tests pass.

## Notes for Next Session
- **Vulnerability and Negotiator Controls**: The current implementation of vulnerability-based adjustments and other negotiator-specific controls requires further review and refinement to ensure they meet policy requirements.
- **UI/UX Refinement**: Continued feedback on the placement and functionality of the negotiation tools is expected.
