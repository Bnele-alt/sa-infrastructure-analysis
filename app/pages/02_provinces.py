# ============================================
# 02_provinces.py
# Province Explorer
# ============================================

import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))

from utils.data_loader import (
    load_master_enriched,
    get_outputs_path,
    PROVINCES,
    CLUSTER_COLORS,
)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title='Provinces — SA Infrastructure',
    page_icon='🗺️',
    layout='wide',
)

st.title('🗺️ Province Explorer')
st.markdown(
    'Select a province to explore its service '
    'delivery performance, governance quality '
    'and municipal financial data.'
)
st.markdown('---')

# ============================================
# PROVINCE SELECTOR
# ============================================
selected_province = st.selectbox(
    'Select a province',
    options=PROVINCES,
    index=0,
)

# ============================================
# LOAD DATA
# ============================================
master = load_master_enriched()

province_data = master[
    master['province'] == selected_province
].copy()

st.markdown(f'## {selected_province}')
st.markdown(
    f'{len(province_data)} municipalities in this province.'
)

# ============================================
# PROVINCE METRICS
# ============================================
col1, col2, col3, col4 = st.columns(4)

avg_income = province_data['avg_taxable_income'].mean()
avg_gov    = province_data['governance_score'].mean()
avg_capex  = province_data['total_capex_rm'].mean()
avg_uifw   = province_data['uifw_total_rm'].mean()

with col1:
    st.metric(
        label='Avg Taxable Income',
        value=f"R{avg_income:,.0f}" if pd.notna(
            avg_income) else 'N/A',
    )

with col2:
    st.metric(
        label='Avg Governance Score',
        value=f"{avg_gov:.2f} / 5" if pd.notna(
            avg_gov) else 'N/A',
    )

with col3:
    st.metric(
        label='Avg Capex Spend (Rm)',
        value=f"R{avg_capex:,.1f}M" if pd.notna(
            avg_capex) else 'N/A',
    )

with col4:
    avg_spend = province_data['spending_ratio'].mean()
    st.metric(
        label='Avg Spending Ratio',
        value=f"{avg_spend:.2f}" if pd.notna(
            avg_spend) else 'N/A',
        help='1.0 = spent exactly budget'
    )

st.markdown('---')

# ============================================
# DES SCORE FOR THIS PROVINCE
# ============================================
des_scores = {
    'Western Cape':   91.4,
    'Gauteng':        84.4,
    'Free State':     71.1,
    'Northern Cape':  58.5,
    'North West':     56.0,
    'Mpumalanga':     55.6,
    'KwaZulu-Natal':  54.4,
    'Limpopo':        44.5,
    'Eastern Cape':   21.7,
}

des_score = des_scores.get(selected_province, 0)
national_avg = 59.7

col_des1, col_des2 = st.columns([1, 2])

with col_des1:
    st.markdown('### Development Efficiency Score')
    delta_val = des_score - national_avg
    delta_str = (f"+{delta_val:.1f} above national avg"
                 if delta_val >= 0
                 else f"{delta_val:.1f} below national avg")
    st.metric(
        label=f'{selected_province} DES',
        value=f'{des_score}',
        delta=delta_str,
    )
    st.caption(
        'Composite score across 10 GHS 2022 '
        'service delivery indicators. '
        'National average: 59.7'
    )

with col_des2:
    # Show national ranking
    sorted_des = sorted(
        des_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    rank = [p for p, s in sorted_des].index(
        selected_province) + 1
    st.markdown(f'### National Ranking: #{rank} of 9')

    des_df = pd.DataFrame(
        sorted_des, columns=['Province', 'DES Score'])
    des_df['Highlighted'] = des_df['Province'].apply(
        lambda x: '◀ Selected' if x == selected_province
        else ''
    )
    st.dataframe(
        des_df,
        use_container_width=True,
        hide_index=True,
    )

st.markdown('---')

# ============================================
# CLUSTER DISTRIBUTION
# ============================================
st.markdown('### Municipal Cluster Distribution')
st.caption(
    'How municipalities in this province are '
    'distributed across the 4 financial '
    'performance clusters.'
)

cluster_counts = province_data[
    'cluster_name'
].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Count']

if len(cluster_counts) > 0:
    col_c1, col_c2 = st.columns([1, 2])

    with col_c1:
        st.dataframe(
            cluster_counts,
            use_container_width=True,
            hide_index=True,
        )

    with col_c2:
        # Show municipalities by cluster
        for cluster_name in cluster_counts['Cluster']:
            munis = province_data[
                province_data['cluster_name']
                == cluster_name
            ]['muni_name'].tolist()
            if munis:
                st.markdown(
                    f'**{cluster_name}:** '
                    f'{", ".join(munis)}'
                )
else:
    st.info('No cluster data available for this province.')

st.markdown('---')

# ============================================
# SERVICE DELIVERY CHARTS
# Charts from outputs folder
# Each chart covers a specific GHS indicator
# ============================================
st.markdown('### Service Delivery Charts')
st.caption(
    'Charts generated from GHS 2022 analysis. '
    'All provinces shown — selected province '
    'context visible in each chart.'
)

# Map chart files to descriptive labels
chart_files = {
    'Refuse — Weekly Removal':
        'chart01_refuse_weekly_removal.png',
    'Refuse — Composition':
        'chart02_refuse_composition.png',
    'Refuse — Irregular Correlation':
        'chart03_refuse_irregular_correlation.png',
    'Water — Supply Source':
        'chart05_water_supply.png',
    'Water — Distance to Source':
        'chart06_water_distance.png',
    'Water — Source Safety':
        'chart07_water_source_safety.png',
    'Sanitation — Toilet Type':
        'chart08_sanitation.png',
    'Sanitation — Toilet Distance':
        'chart09_toilet_distance.png',
    'Handwashing Access':
        'chart10_handwashing.png',
    'Electricity — Access':
        'chart11_electricity_access.png',
    'Electricity — Source':
        'chart12_electricity_source.png',
    'Housing — Dwelling Type':
        'chart13_dwelling_type.png',
    'Housing — Formal vs Informal':
        'chart13b_formal_vs_informal.png',
    'Housing — Dwelling Age':
        'chart14_dwelling_age.png',
}

# Display charts in pairs
chart_items = list(chart_files.items())
for i in range(0, len(chart_items), 2):
    col_a, col_b = st.columns(2)

    label_a, file_a = chart_items[i]
    path_a = get_outputs_path(file_a)

    with col_a:
        st.markdown(f'**{label_a}**')
        if os.path.exists(path_a):
            st.image(
                path_a,
                use_container_width=True
            )
        else:
            st.caption(f'Chart not found: {file_a}')

    if i + 1 < len(chart_items):
        label_b, file_b = chart_items[i + 1]
        path_b = get_outputs_path(file_b)

        with col_b:
            st.markdown(f'**{label_b}**')
            if os.path.exists(path_b):
                st.image(
                    path_b,
                    use_container_width=True
                )
            else:
                st.caption(f'Chart not found: {file_b}')

st.markdown('---')

# ============================================
# MUNICIPALITY TABLE
# ============================================
st.markdown('### All Municipalities')
st.caption(
    'Complete financial data for all municipalities '
    'in this province. Sort by any column.'
)

display_cols = {
    'muni_name':          'Municipality',
    'muni_category':      'Type',
    'cluster_name':       'Cluster',
    'governance_score':   'Governance',
    'avg_taxable_income': 'Avg Income',
    'total_capex_rm':     'Capex (Rm)',
    'spending_ratio':     'Spend Ratio',
    'uifw_total_rm':      'UIFW (Rm)',
}

available_cols = [
    c for c in display_cols.keys()
    if c in province_data.columns
]

table_df = province_data[available_cols].copy()
table_df = table_df.rename(columns=display_cols)
table_df = table_df.sort_values(
    'Governance', ascending=False)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown('---')
st.caption(
    'Source: Stats SA GHS 2022 · '
    'National Treasury Municipal Money 2021 · '
    'SARS Tax Statistics 2022'
)