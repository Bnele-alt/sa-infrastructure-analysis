# ============================================
# 01_overview.py
# Provincial Service Delivery Overview
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import sys

# Add parent directory to path so we can
# import from utils
sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))

from utils.data_loader import (
    load_master_enriched,
    get_outputs_path,
    PROVINCES,
    GOVERNANCE_LABELS,
)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title='Overview — SA Infrastructure',
    page_icon='📊',
    layout='wide',
)

st.title('📊 Provincial Overview')
st.markdown(
    'Service delivery performance across all '
    '9 provinces based on the Stats SA '
    'General Household Survey 2022.'
)
st.markdown('---')

# ============================================
# DES SCORES
# ============================================
st.markdown('## Development Efficiency Scores')
st.caption(
    'Composite score across 10 service delivery '
    'indicators. Weighted by importance — water '
    'and sanitation weighted highest. Max score: 100.'
)

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
    'Water Access %': [
        96.8, 95.2, 88.4,
        85.1, 82.3, 79.6,
        78.4, 72.1, 65.3
    ],
    'Refuse Reliability %': [
        94.2, 89.1, 72.3,
        61.2, 58.4, 55.1,
        52.3, 41.2, 28.4
    ],
    'Avg Governance Score': [
        4.20, 3.89, 1.74,
        2.23, 2.00, 3.12,
        3.70, 3.55, 3.42
    ],
}

des_df = pd.DataFrame(des_data)
des_df = des_df.sort_values('DES Score', ascending=False)

# ============================================
# DES BAR CHART
# ============================================
fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#1a1d27')

colors = [
    '#1a9850' if s >= 80 else
    '#fee08b' if s >= 60 else
    '#fc8d59' if s >= 40 else
    '#d73027'
    for s in des_df['DES Score']
]

bars = ax.barh(
    des_df['Province'],
    des_df['DES Score'],
    color=colors,
    edgecolor='none',
    height=0.6,
)

# Add value labels
for bar, val in zip(bars, des_df['DES Score']):
    ax.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f'{val}',
        va='center', ha='left',
        color='white', fontsize=11,
        fontweight='bold'
    )

ax.axvline(x=59.7, color='white', linestyle='--',
           alpha=0.4, linewidth=1)
ax.text(59.7, -0.7, 'National avg 59.7',
        color='white', alpha=0.5, fontsize=9,
        ha='center')

ax.set_xlim(0, 105)
ax.set_xlabel('DES Score', color='white', fontsize=11)
ax.set_title(
    'Development Efficiency Score by Province — 2022',
    color='white', fontsize=13, fontweight='bold', pad=15
)
ax.tick_params(colors='white')
ax.spines[:].set_visible(False)

for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown('---')

# ============================================
# MASTER HEATMAP
# Load from outputs if it exists
# ============================================
st.markdown('## Service Delivery Heatmap')
st.caption(
    'All 10 GHS indicators across all 9 provinces. '
    'Green = better performance, Red = worse.'
)

heatmap_path = get_outputs_path(
    'master_heatmap_2022.png')

if os.path.exists(heatmap_path):
    st.image(heatmap_path, use_container_width=True)
else:
    st.info(
        'Heatmap image not found in outputs folder. '
        'Run 02_analysis.ipynb to generate it.'
    )

st.markdown('---')

# ============================================
# GOVERNANCE OVERVIEW
# ============================================
st.markdown('## Governance Quality 2021')
st.caption(
    'Audit outcomes from the Auditor General. '
    'Score 5 = clean audit. Score 0 = not submitted.'
)

col1, col2 = st.columns(2)

with col1:
    st.markdown('**Audit outcome distribution**')

    audit_data = {
        'Outcome': [
            'Clean (score 5)',
            'Unqualified + emphasis (score 4)',
            'Qualified (score 3)',
            'Adverse (score 2)',
            'Disclaimer (score 1)',
            'Outstanding (score 0)'
        ],
        'Count': [40, 100, 71, 4, 18, 24],
        'Percentage': [
            '15.6%', '38.9%', '27.6%',
            '1.6%', '7.0%', '9.3%'
        ]
    }

    audit_df = pd.DataFrame(audit_data)
    st.dataframe(
        audit_df,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.markdown('**Average governance score by province**')

    gov_data = {
        'Province': [
            'Western Cape', 'Gauteng',
            'KwaZulu-Natal', 'Limpopo',
            'Eastern Cape', 'Mpumalanga',
            'Northern Cape', 'North West',
            'Free State'
        ],
        'Avg Score': [
            4.20, 3.89, 3.70, 3.55,
            3.42, 3.12, 2.23, 2.00, 1.74
        ]
    }

    gov_df = pd.DataFrame(gov_data)
    gov_df = gov_df.sort_values(
        'Avg Score', ascending=False)

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    fig2.patch.set_facecolor('#0f1117')
    ax2.set_facecolor('#1a1d27')

    gov_colors = [
        '#1a9850' if s >= 4 else
        '#fee08b' if s >= 3 else
        '#fc8d59' if s >= 2 else
        '#d73027'
        for s in gov_df['Avg Score']
    ]

    ax2.barh(
        gov_df['Province'],
        gov_df['Avg Score'],
        color=gov_colors,
        edgecolor='none',
        height=0.6
    )
    ax2.set_xlim(0, 5.5)
    ax2.set_xlabel(
        'Average governance score (0-5)',
        color='white'
    )
    ax2.tick_params(colors='white')
    ax2.spines[:].set_visible(False)
    ax2.set_title(
        'Governance by province',
        color='white', fontweight='bold'
    )
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

st.markdown('---')

# ============================================
# KEY FINDINGS
# ============================================
st.markdown('## Key Findings')

findings_col1, findings_col2, findings_col3 = (
    st.columns(3))

with findings_col1:
    st.error('''
    **Eastern Cape — 21.7 DES**

    Lowest service delivery score nationally.
    Gap of 69.6 points below Western Cape.
    Only 28.4% of households have reliable
    refuse removal.
    ''')

with findings_col2:
    st.warning('''
    **Free State paradox**

    DES score of 71.1 — third highest nationally.
    But governance score of 1.74 — lowest nationally.
    Capex spending ratio 0.47 — spending less than
    half their infrastructure budget.
    ''')

with findings_col3:
    st.success('''
    **Western Cape consistency**

    Highest DES at 91.4 and highest governance
    at 4.20. Only province where financial
    performance and service delivery align
    consistently across all metrics.
    ''')

st.markdown('---')
st.caption(
    'Source: Stats SA General Household Survey 2022 · '
    'National Treasury Municipal Money 2021 · '
    'SARS Tax Statistics 2022'
)