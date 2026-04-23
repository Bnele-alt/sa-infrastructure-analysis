# ============================================
# 04_clusters.py
# Cluster Explorer
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
    get_assets_path,
    CLUSTER_COLORS,
    CLUSTER_NAMES,
    CLUSTER_DESCRIPTIONS,
)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title='Clusters — SA Infrastructure',
    page_icon='🔵',
    layout='wide',
)

st.title('🔵 Cluster Explorer')
st.markdown(
    'South African municipalities grouped into '
    '4 financial performance profiles using '
    'K-means clustering on 2021 financial data.'
)
st.markdown('---')

# ============================================
# LOAD DATA
# ============================================
master = load_master_enriched()

# ============================================
# METHODOLOGY NOTE
# ============================================
with st.expander('📋 Methodology — How clusters were built'):
    st.markdown('''
    **Algorithm:** K-means clustering (k=4)

    **Features used:**
    - Average taxable income per taxpayer (SARS 2021)
    - Governance score derived from AG audit opinion
    - Capital expenditure spending ratio (actual/budget)
    - UIFW as percentage of capital budget

    **Preprocessing:**
    - StandardScaler applied to all features
    - UIFW capped at 200% to prevent outlier dominance
    - 205 of 248 municipalities had complete data

    **Validation:**
    - Silhouette score: 0.407 at k=4
    - Elbow method confirmed k=4 as optimal

    **Important limitation:**
    Clusters reflect relative financial positioning
    based on 2021 submitted data only. They do not
    represent absolute governance quality ratings.
    Local context and news reporting may indicate
    conditions not captured in financial submissions.
    Municipalities marked (partial data) were assigned
    using income and governance score only.
    ''')

st.markdown('---')

# ============================================
# CLUSTER OVERVIEW CARDS
# ============================================
st.markdown('## The 4 Municipality Profiles')

col0, col1, col2, col3 = st.columns(4)

cluster_counts = master[
    'cluster_name'
].value_counts()

for col, cluster_id, label in [
    (col1, 1, CLUSTER_NAMES[1]),
    (col0, 0, CLUSTER_NAMES[0]),
    (col2, 2, CLUSTER_NAMES[2]),
    (col3, 3, CLUSTER_NAMES[3]),
]:
    color = CLUSTER_COLORS[cluster_id]
    count = master[
        master['cluster'] == cluster_id
    ].shape[0]

    col.markdown(f'''
    <div style="
        background:{color}22;
        border:1px solid {color};
        border-radius:8px;
        padding:16px;
        text-align:center;
        height:120px;
    ">
        <div style="
            font-size:28px;
            font-weight:bold;
            color:{color};
        ">{count}</div>
        <div style="
            color:white;
            font-size:12px;
            margin-top:6px;
        ">{label}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('---')

# ============================================
# CLUSTER SELECTOR
# ============================================
selected_cluster_name = st.selectbox(
    'Select a cluster to explore',
    options=[
        CLUSTER_NAMES[1],
        CLUSTER_NAMES[0],
        CLUSTER_NAMES[2],
        CLUSTER_NAMES[3],
    ]
)

# Get cluster ID from name
selected_cluster_id = [
    k for k, v in CLUSTER_NAMES.items()
    if v == selected_cluster_name
][0]

cluster_color = CLUSTER_COLORS[selected_cluster_id]
cluster_data  = master[
    master['cluster'] == selected_cluster_id
].copy()

st.markdown(f'## {selected_cluster_name}')
st.markdown(
    f'{len(cluster_data)} municipalities '
    f'in this cluster.'
)

# ============================================
# CLUSTER DESCRIPTION
# ============================================
st.info(CLUSTER_DESCRIPTIONS[selected_cluster_id])

# ============================================
# CLUSTER METRICS
# ============================================
st.markdown('### Cluster Averages')
st.caption('Average values for all municipalities in this cluster.')

cm1, cm2, cm3, cm4 = st.columns(4)

with cm1:
    avg_inc = cluster_data['avg_taxable_income'].mean()
    nat_inc = master['avg_taxable_income'].mean()
    st.metric(
        'Avg Taxable Income',
        f"R{avg_inc:,.0f}" if pd.notna(avg_inc) else 'N/A',
        f"R{avg_inc - nat_inc:+,.0f} vs national"
        if pd.notna(avg_inc) else '',
    )

with cm2:
    avg_gov = cluster_data['governance_score'].mean()
    nat_gov = master['governance_score'].mean()
    st.metric(
        'Avg Governance Score',
        f"{avg_gov:.2f} / 5" if pd.notna(avg_gov) else 'N/A',
        f"{avg_gov - nat_gov:+.2f} vs national"
        if pd.notna(avg_gov) else '',
    )

with cm3:
    avg_spend = cluster_data['spending_ratio'].mean()
    nat_spend = master['spending_ratio'].mean()
    st.metric(
        'Avg Spending Ratio',
        f"{avg_spend:.3f}" if pd.notna(avg_spend) else 'N/A',
        f"{avg_spend - nat_spend:+.3f} vs national"
        if pd.notna(avg_spend) else '',
    )

with cm4:
    avg_uifw = cluster_data['uifw_pct_budget'].mean()
    nat_uifw = master['uifw_pct_budget'].mean()
    st.metric(
        'Avg UIFW % Budget',
        f"{avg_uifw:.1f}%" if pd.notna(avg_uifw) else 'N/A',
        f"{avg_uifw - nat_uifw:+.1f}% vs national"
        if pd.notna(avg_uifw) else '',
    )

st.markdown('---')

# ============================================
# PROVINCE DISTRIBUTION
# ============================================
st.markdown('### Province Distribution')
st.caption(
    'Which provinces contribute most municipalities '
    'to this cluster.'
)

prov_dist = cluster_data[
    'province'
].value_counts().reset_index()
prov_dist.columns = ['Province', 'Count']
prov_dist['% of cluster'] = (
    prov_dist['Count'] / len(cluster_data) * 100
).round(1).astype(str) + '%'

st.dataframe(
    prov_dist,
    use_container_width=True,
    hide_index=True,
)

st.markdown('---')

# ============================================
# MUNICIPALITY LIST
# ============================================
st.markdown('### Municipalities in this cluster')

display_cols = {
    'muni_name':          'Municipality',
    'province':           'Province',
    'governance_score':   'Governance',
    'avg_taxable_income': 'Avg Income',
    'spending_ratio':     'Spend Ratio',
    'uifw_pct_budget':    'UIFW %',
}

available = [
    c for c in display_cols
    if c in cluster_data.columns
]

table = cluster_data[available].rename(
    columns=display_cols
).sort_values('Governance', ascending=False)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
)

st.markdown('---')

# ============================================
# CLUSTER CHARTS FROM OUTPUTS
# ============================================
st.markdown('### K-Means Analysis Charts')

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    elbow_path = get_outputs_path(
        'kmeans_elbow_silhouette.png')
    if os.path.exists(elbow_path):
        st.markdown('**Elbow and silhouette scores**')
        st.image(
            elbow_path,
            use_container_width=True
        )

with col_chart2:
    cluster_path = get_outputs_path(
        'kmeans_clusters.png')
    if os.path.exists(cluster_path):
        st.markdown('**Cluster scatter plots**')
        st.image(
            cluster_path,
            use_container_width=True
        )

st.markdown('---')

# ============================================
# INTERACTIVE MAP
# ============================================
st.markdown('### Interactive Municipality Map')
st.caption(
    'Colour coded by cluster. '
    'Hover over any municipality for its profile. '
    'Municipalities with irregular spend above 30% '
    'show a warning flag in the tooltip.'
)

map_path = get_assets_path('sa_map.html')

if os.path.exists(map_path):
    with open(map_path, 'r', encoding='utf-8') as f:
        map_html = f.read()
    st.components.v1.html(
        map_html,
        height=600,
        scrolling=False
    )
else:
    st.info(
        'Map not found. Run 04_map.ipynb to generate '
        'app/assets/sa_map.html first.'
    )

st.markdown('---')
st.caption(
    'Source: National Treasury Municipal Money 2021 · '
    'SARS Tax Statistics 2022 · '
    'K-means clustering — sklearn'
)