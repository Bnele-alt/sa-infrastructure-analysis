# SA Infrastructure & Wealth Analysis

## Project Status
- [x] Project setup and folder structure
- [x] Data collection — 13 GHS2022 datasets from Stats SA
- [x] Data cleaning — all 13 datasets cleaned and standardised
- [x] Refuse analysis — 4 charts, key findings documented
- [x] Water analysis — 3 charts, key findings documented
- [x] Sanitation analysis
- [x] Electricity analysis
- [x] Housing analysis
- [x] Master service delivery heatmap
- [x] Development Efficiency Score calculation
- [x] Wealth correlation layer (Phase 2)
- [x] ML clustering
- [ ] Streamlit dashboard

## Data Sources
- Statistics South Africa — General Household Survey 2022
- SuperWEB2 portal: superweb2.statssa.gov.za

## Datasets
13 service delivery indicators across 9 provinces:
electricity access, electricity source, water source,
water supply, water distance, toilet type, toilet distance,
refuse removal, refuse irregular, handwashing, littering,
dwelling type, dwelling built year

## Key Findings

### Refuse Analysis
**Strongest predictor of littering: Irregular removal (r = 0.951)**

Service reliability matters more than service presence.
Irregular municipal collection is a near-perfect predictor
of household littering perception across provinces.

Province summary:
- Western Cape: Best refuse outcomes — 88.5% municipal weekly
- Free State: Most dysfunctional — high collection on paper,
  highest irregular removal at 58.7%, highest littering at 55.9%
- Limpopo: Complete municipal absence — 68.6% own dump,
  but low littering due to rural normalisation
- Mpumalanga: Most honest data — perception matches reality

### Water Analysis
**Eastern Cape water crisis quantified: 16.2% unsafe sources**

Distance to water is NOT the primary inequality metric.
Source safety and supply reliability are the critical dimensions.

Province summary:
- Gauteng: Best water outcomes — 93.1% supply confirmation,
  negligible unsafe sources
- Eastern Cape: Most severe — 16.2% unsafe sources,
  56.1% supply confirmation, over 1 million households
  on rivers and springs
- KwaZulu-Natal: 8.9% unsafe sources despite water
  being physically close — source quality is the problem
- Limpopo: Infrastructure present but unreliable —
  low supply confirmation despite reasonable distance metrics

### Cross-cutting Pattern
The same three provinces — Eastern Cape, Limpopo, KwaZulu-Natal —
consistently underperform across every service delivery dimension.
This indicates systemic governance failure rather than
sector-specific problems.

Western Cape and Gauteng consistently lead but mask significant
internal inequality between urban cores and peripheral areas.
Provincial averages flatten inequality — municipal level
analysis required for accurate picture.

## Methodology Notes
- Person-weighted counts from GHS2022 used throughout
- SuperWEB2 exports handled three different format types
- UTF-8-sig encoding required for distance variables
- Unsafe water categorisation based on source type not
  quality testing — piped water may still be unreliable
- Irregular removal measures reliability not presence —
  low scores in Limpopo reflect absence of service
  not reliable service

## Tools
- Python 3.12, Pandas, Matplotlib, Seaborn
- Stats SA SuperWEB2
- VS Code with Jupyter extension
- GitHub for version control