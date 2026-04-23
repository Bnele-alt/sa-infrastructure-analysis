# ============================================
# 03_municipalities.py
# Municipality Explorer
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import sys

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))

from utils.data_loader import (
    load_master_enriched,
    load_audit,
    CLUSTER_COLORS,
    CLUSTER_DESCRIPTIONS,
    GOVERNANCE_LABELS,
)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title='Municipalities — SA Infrastructure',
    page_icon='🏘️',
    layout='wide',
)

st.title('🏘️ Municipality Explorer')
st.markdown(
    'Select any municipality to see its complete '
    'financial profile, governance history and '
    'how it compares to national averages.'
)
st.markdown('---')

# ============================================
# LOAD DATA
# ============================================
master = load_master_enriched()
audit  = load_audit()

# ============================================
# SEARCH — Province then Municipality
# Two step selection so the dropdown is
# not overwhelmed with 248 names at once
# ============================================
col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    provinces = sorted(master['province'].dropna().unique())
    selected_province = st.selectbox(
        'Step 1 — Select province',
        options=provinces,
    )

with col_sel2:
    province_munis = master[
        master['province'] == selected_province
    ]['muni_name'].dropna().sort_values().tolist()

    selected_muni = st.selectbox(
        'Step 2 — Select municipality',
        options=province_munis,
    )

# ============================================
# GET MUNICIPALITY DATA
# ============================================
muni_row = master[
    master['muni_name'] == selected_muni
].iloc[0]

muni_code = muni_row.get('muni_code', '')
cluster   = muni_row.get('cluster', -1)
cluster_name = muni_row.get('cluster_name', 'No data')

# Get national averages for comparison
nat_avg_income = master['avg_taxable_income'].mean()
nat_avg_gov    = master['governance_score'].mean()
nat_avg_capex  = master['total_capex_rm'].mean()
nat_avg_spend  = master['spending_ratio'].mean()
nat_avg_uifw   = master['uifw_total_rm'].mean()

st.markdown('---')

# ============================================
# MUNICIPALITY HEADER
# ============================================
cluster_color = CLUSTER_COLORS.get(
    int(cluster) if pd.notna(cluster) else -1,
    '#999999'
)

st.markdown(f'''
<div style="
    background: linear-gradient(
        135deg, #1a1d27 0%, #2d3142 100%);
    border-left: 5px solid {cluster_color};
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 20px;
">
    <h2 style="margin:0;color:white;">
        {selected_muni}
    </h2>
    <p style="margin:4px 0 0 0;color:#aaa;">
        {selected_province} ·
        {muni_row.get("muni_long_name", "")} ·
        Category {muni_row.get("muni_category", "")}
    </p>
    <p style="margin:8px 0 0 0;">
        <span style="
            background:{cluster_color}33;
            color:{cluster_color};
            border:1px solid {cluster_color};
            border-radius:4px;
            padding:3px 10px;
            font-size:13px;
        ">
            {cluster_name}
        </span>
    </p>
</div>
''', unsafe_allow_html=True)

# ============================================
# KEY METRICS VS NATIONAL AVERAGE
# ============================================
st.markdown('### Financial Profile')
st.caption('Compared to national municipal average.')

m1, m2, m3, m4, m5 = st.columns(5)

avg_income = muni_row.get('avg_taxable_income')
gov_score  = muni_row.get('governance_score')
capex      = muni_row.get('total_capex_rm')
spend      = muni_row.get('spending_ratio')
uifw       = muni_row.get('uifw_total_rm')

with m1:
    if pd.notna(avg_income):
        delta = avg_income - nat_avg_income
        st.metric(
            'Avg Taxable Income',
            f"R{avg_income:,.0f}",
            f"R{delta:+,.0f} vs national",
        )
    else:
        st.metric('Avg Taxable Income', 'No data')

with m2:
    if pd.notna(gov_score):
        delta = gov_score - nat_avg_gov
        label = GOVERNANCE_LABELS.get(
            int(gov_score), 'Unknown')
        st.metric(
            'Governance Score',
            f"{gov_score:.0f} / 5",
            f"{delta:+.2f} vs national avg",
        )
        st.caption(label)
    else:
        st.metric('Governance Score', 'No data')

with m3:
    if pd.notna(capex):
        delta = capex - nat_avg_capex
        st.metric(
            'Capex Spend',
            f"R{capex:,.1f}M",
            f"R{delta:+,.1f}M vs national",
        )
    else:
        st.metric('Capex Spend', 'No data')

with m4:
    if pd.notna(spend):
        delta = spend - nat_avg_spend
        st.metric(
            'Spending Ratio',
            f"{spend:.3f}",
            f"{delta:+.3f} vs national avg",
            help='1.0 = spent exactly budget'
        )
    else:
        st.metric('Spending Ratio', 'No data')

with m5:
    if pd.notna(uifw):
        uifw_pct = muni_row.get('uifw_pct_budget', 0)
        uifw_pct = 0 if pd.isna(uifw_pct) else uifw_pct
        st.metric(
            'UIFW Total',
            f"R{uifw:,.1f}M",
            f"{uifw_pct:.1f}% of budget",
        )
        if uifw_pct > 50:
            st.error('⚠️ Exceeds 50% of budget')
        elif uifw_pct > 30:
            st.warning('⚠️ Above 30% of budget')
    else:
        st.metric('UIFW Total', 'No data')

st.markdown('---')

# ============================================
# CLUSTER CONTEXT
# ============================================
st.markdown('### Cluster Membership')

col_cl1, col_cl2 = st.columns([1, 2])

with col_cl1:
    st.markdown(f'''
    <div style="
        background:{cluster_color}22;
        border:1px solid {cluster_color};
        border-radius:8px;
        padding:16px;
        text-align:center;
    ">
        <div style="
            font-size:32px;
            font-weight:bold;
            color:{cluster_color};
        ">
            {cluster_name.split("—")[0].strip()
             if "—" in str(cluster_name) else cluster_name}
        </div>
        <div style="color:#aaa;font-size:13px;">
            {cluster_name}
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col_cl2:
    desc = CLUSTER_DESCRIPTIONS.get(
        int(cluster) if pd.notna(cluster)
        and cluster != -1 else -1,
        'No cluster data available for this municipality.'
    )
    st.markdown(f'**About this cluster:**')
    st.info(desc)

st.markdown('---')

# ============================================
# COMPARISON CHART
# This municipality vs provincial avg vs national avg
# ============================================
st.markdown('### How does it compare?')
st.caption(
    'This municipality vs provincial average '
    'vs national average across key metrics.'
)

# Get provincial averages
prov_data = master[
    master['province'] == selected_province
]
prov_avg_income = prov_data['avg_taxable_income'].mean()
prov_avg_gov    = prov_data['governance_score'].mean()
prov_avg_spend  = prov_data['spending_ratio'].mean()

# Normalize metrics to 0-100 scale for radar
metrics = ['Income', 'Governance', 'Spend ratio']

# Use min-max from full dataset for normalization
def normalize(val, col):
    col_min = master[col].min()
    col_max = master[col].max()
    if col_max == col_min:
        return 50
    return ((val - col_min) / (col_max - col_min)) * 100

muni_vals = [
    normalize(avg_income or 0, 'avg_taxable_income'),
    normalize(gov_score or 0, 'governance_score'),
    normalize(min(spend or 0, 3), 'spending_ratio'),
]
prov_vals = [
    normalize(prov_avg_income, 'avg_taxable_income'),
    normalize(prov_avg_gov, 'governance_score'),
    normalize(min(prov_avg_spend, 3), 'spending_ratio'),
]
nat_vals = [
    normalize(nat_avg_income, 'avg_taxable_income'),
    normalize(nat_avg_gov, 'governance_score'),
    normalize(min(nat_avg_spend, 3), 'spending_ratio'),
]

fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#1a1d27')

x = range(len(metrics))
width = 0.25

bars1 = ax.bar(
    [i - width for i in x],
    muni_vals,
    width,
    label=selected_muni,
    color=cluster_color,
    alpha=0.9,
)
bars2 = ax.bar(
    x,
    prov_vals,
    width,
    label=f'{selected_province} avg',
    color='#4575b4',
    alpha=0.7,
)
bars3 = ax.bar(
    [i + width for i in x],
    nat_vals,
    width,
    label='National avg',
    color='#999999',
    alpha=0.6,
)

ax.set_xticks(list(x))
ax.set_xticklabels(metrics, color='white', fontsize=12)
ax.set_ylabel(
    'Normalised score (0-100)',
    color='white'
)
ax.set_title(
    f'{selected_muni} vs provincial and national averages',
    color='white', fontweight='bold'
)
ax.legend(
    facecolor='#1a1d27',
    labelcolor='white',
    fontsize=10
)
ax.tick_params(colors='white')
ax.spines[:].set_visible(False)
ax.set_ylim(0, 115)

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown('---')

# ============================================
# AUDIT HISTORY
# Show all years from audit opinions file
# ============================================
st.markdown('### Audit History')
st.caption(
    'Audit outcomes from the Auditor General '
    'across all available years.'
)

# Handle both column naming conventions
# API download uses dots, cleaned file may use underscores
muni_audit = audit[
    audit['muni_code'] == muni_code
].copy()

if len(muni_audit) > 0:
    muni_audit_display = muni_audit[[
        'muni_code', 'opinion_code',
        'opinion_label', 'governance_score'
    ]].rename(columns={
        'muni_code':        'Code',
        'opinion_code':     'Audit Code',
        'opinion_label':    'Audit Outcome',
        'governance_score': 'Score'
    })
    st.dataframe(
        muni_audit_display,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info(
        'No audit history found for this municipality.'
    )

st.markdown('---')

# ============================================
# RAW DATA
# ============================================
with st.expander('View raw data for this municipality'):
    display_row = muni_row.to_frame().T
    st.dataframe(
        display_row,
        use_container_width=True,
        hide_index=True,
    )

st.markdown('---')
st.caption(
    'Source: National Treasury Municipal Money 2021 · '
    'SARS Tax Statistics 2022 · '
    'Auditor General audit opinions'
)