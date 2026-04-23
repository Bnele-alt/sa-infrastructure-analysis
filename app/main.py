# ============================================
# main.py
# SA Infrastructure & Wealth Analysis
# Streamlit Dashboard Entry Point
# ============================================

import streamlit as st

# ============================================
# PAGE CONFIGURATION
# Must be the first Streamlit command
# ============================================
st.set_page_config(
    page_title='SA Infrastructure & Wealth Analysis',
    page_icon='🇿🇦',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ============================================
# CUSTOM CSS
# Applies across all pages
# ============================================
st.markdown('''
    <style>
        /* Main background */
        .stApp {
            background-color: #0f1117;
            color: #ffffff;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1a1d27;
            border-right: 1px solid #2d3142;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background-color: #1a1d27;
            border: 1px solid #2d3142;
            border-radius: 8px;
            padding: 16px;
        }

        /* Headers */
        h1, h2, h3 {
            color: #ffffff;
        }

        /* Divider */
        hr {
            border-color: #2d3142;
        }

        /* Dataframe */
        [data-testid="stDataFrame"] {
            background-color: #1a1d27;
        }

        /* Selectbox and other inputs */
        [data-testid="stSelectbox"] {
            background-color: #1a1d27;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
''', unsafe_allow_html=True)

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.image(
    'https://upload.wikimedia.org/wikipedia/commons'
    '/thumb/a/af/Flag_of_South_Africa.svg/'
    '320px-Flag_of_South_Africa.svg.png',
    width=120
)

st.sidebar.markdown('---')
st.sidebar.markdown('''
### SA Infrastructure Analysis
**Data Science Portfolio Project**

Analysing service delivery, governance
and wealth across 248 SA municipalities
using public government data.
''')

st.sidebar.markdown('---')
st.sidebar.markdown('''
**Data Sources**
- Stats SA — General Household Survey 2022
- SARS — Tax Statistics 2022
- National Treasury — Municipal Money 2021

**Methodology**
- GHS service delivery analysis
- K-means municipal clustering
- Correlation and regression analysis

**Built by:** Zansii
''')

st.sidebar.markdown('---')
st.sidebar.caption(
    'Data reflects 2021 financial year and '
    '2022 household survey. '
    'Clusters based on relative financial '
    'positioning — not absolute quality ratings.'
)

# ============================================
# LANDING PAGE CONTENT
# ============================================
st.title('🇿🇦 SA Infrastructure & Wealth Analysis')
st.markdown(
    '### Service delivery, governance and wealth '
    'across 248 South African municipalities'
)

st.markdown('---')

# ============================================
# KEY FINDINGS SUMMARY
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label='Municipalities Analysed',
        value='248',
        delta='A and B categories only',
    )

with col2:
    st.metric(
        label='Clean Audits 2021',
        value='40',
        delta='15.6% of municipalities',
    )

with col3:
    st.metric(
        label='No Audit Submitted',
        value='24',
        delta='9.3% — outstanding',
    )

with col4:
    st.metric(
        label='National DES Gap',
        value='69.6 pts',
        delta='WC 91.4 vs EC 21.7',
    )

st.markdown('---')

# ============================================
# PROJECT OVERVIEW
# ============================================
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('''
    ## What this project measures

    This dashboard presents a data-driven analysis
    of service delivery inequality across South Africa,
    combining three public government datasets into
    one integrated view of municipal performance.

    **Phase 1 — Service Delivery (GHS 2022)**
    Analysis of water access, sanitation, refuse
    removal, electricity and housing across all
    9 provinces using the Stats SA General Household
    Survey. A Development Efficiency Score (DES)
    was calculated for each province.

    **Phase 2 — Wealth and Governance (2021)**
    Municipal income data from SARS Tax Statistics
    combined with National Treasury Municipal Money
    data on capital expenditure, audit outcomes and
    irregular expenditure. K-means clustering
    identified 4 distinct municipality profiles.

    **Phase 3 — Visualisation**
    Interactive choropleth map, province explorer,
    municipality profiles and SQL query builder.
    ''')

with col_right:
    st.markdown('## Central Finding')
    st.info('''
    **Income does not determine
    governance quality.**

    Gamagara Local Municipality —
    the wealthiest municipality in SA
    by average taxable income —
    sits in the At Risk cluster
    alongside municipalities earning
    half as much.

    Institutional capacity, not wealth,
    determines whether municipalities
    deliver services effectively.
    ''')

st.markdown('---')

# ============================================
# DES SCORES SUMMARY TABLE
# ============================================
st.markdown('## Development Efficiency Scores by Province')
st.caption(
    'Composite score across 10 GHS 2022 service '
    'delivery indicators. Higher is better. '
    'Maximum possible score: 100.'
)

import pandas as pd

des_data = {
    'Province': [
        'Western Cape', 'Gauteng', 'Free State',
        'Northern Cape', 'North West', 'Mpumalanga',
        'KwaZulu-Natal', 'Limpopo', 'Eastern Cape'
    ],
    'DES Score': [
        91.4, 84.4, 71.1,
        58.5, 56.0, 55.6,
        54.4, 44.5, 21.7
    ],
    'Governance Score (avg)': [
        4.20, 3.89, 1.74,
        2.23, 2.00, 3.12,
        3.70, 3.55, 3.42
    ],
    'Avg Taxable Income': [
        'R256,491', 'R337,053', 'R232,588',
        'R263,088', 'R261,268', 'R274,653',
        'R256,832', 'R293,447', 'R239,962'
    ],
}

des_df = pd.DataFrame(des_data)
des_df = des_df.sort_values('DES Score', ascending=False)

st.dataframe(
    des_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown('---')

# ============================================
# NAVIGATION GUIDE
# ============================================
st.markdown('## Explore the Dashboard')

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown('''
    **📊 Overview**
    Provincial service delivery heatmap
    and DES score comparison.
    ''')
    st.markdown('''
    **🗺️ Province Explorer**
    Select a province to see all service
    delivery charts and metrics.
    ''')

with nav_col2:
    st.markdown('''
    **🏘️ Municipality Explorer**
    Look up any municipality for its full
    financial and governance profile.
    ''')
    st.markdown('''
    **🔵 Cluster Explorer**
    Interactive map and profiles of the
    4 municipality cluster types.
    ''')

with nav_col3:
    st.markdown('''
    **🔍 Query Builder**
    Build custom SQL queries to filter
    and rank municipalities by any metric.
    ''')
    st.markdown('''
    **📋 Methodology**
    Data sources, limitations and
    analytical approach.
    ''')

st.markdown('---')
st.caption(
    'Built by Zansii · '
    'Data: Stats SA GHS 2022, SARS Tax Statistics 2022, '
    'National Treasury Municipal Money 2021 · '
    'Analysis reflects 2021 financial year data'
)