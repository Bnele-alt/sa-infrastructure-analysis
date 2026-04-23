# ============================================
# 05_query_builder.py
# SQL Query Builder
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
    PROVINCES,
)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title='Query Builder — SA Infrastructure',
    page_icon='🔍',
    layout='wide',
)

st.title('🔍 SQL Query Builder')
st.markdown(
    'Build custom queries to filter and rank '
    'municipalities by any financial or '
    'governance metric. No SQL knowledge required.'
)
st.markdown('---')

# ============================================
# LOAD DATA
# ============================================
master = load_master_enriched()

# ============================================
# QUERY BUILDER UI
# ============================================
st.markdown('## Build Your Query')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('**Filter by province**')
    province_options = ['All provinces'] + PROVINCES
    selected_province = st.selectbox(
        'Province',
        options=province_options,
        label_visibility='collapsed'
    )

with col2:
    st.markdown('**Filter by cluster**')
    cluster_options = [
        'All clusters',
        'Operational — Moderate governance',
        'At Risk — High irregular expenditure',
        'Failing — No financial accountability',
        'Critical — Extreme budget breach',
    ]
    selected_cluster = st.selectbox(
        'Cluster',
        options=cluster_options,
        label_visibility='collapsed'
    )

with col3:
    st.markdown('**Filter by municipality type**')
    type_options = [
        'All types',
        'A — Metropolitan',
        'B — Local',
    ]
    selected_type = st.selectbox(
        'Type',
        options=type_options,
        label_visibility='collapsed'
    )

st.markdown('---')

# Metric filter
st.markdown('## Add a Metric Condition')

metric_col1, metric_col2, metric_col3 = st.columns(3)

metric_options = {
    'Average taxable income':    'avg_taxable_income',
    'Governance score (0-5)':    'governance_score',
    'Capex spend (R millions)':  'total_capex_rm',
    'Spending ratio':            'spending_ratio',
    'UIFW total (R millions)':   'uifw_total_rm',
    'UIFW % of budget':          'uifw_pct_budget',
    'Number of taxpayers':       'num_taxpayers',
}

with metric_col1:
    st.markdown('**Metric**')
    selected_metric_label = st.selectbox(
        'Metric',
        options=list(metric_options.keys()),
        label_visibility='collapsed'
    )
    selected_metric = metric_options[
        selected_metric_label]

with metric_col2:
    st.markdown('**Condition**')
    condition = st.selectbox(
        'Condition',
        options=[
            'Greater than',
            'Less than',
            'Greater than or equal to',
            'Less than or equal to',
        ],
        label_visibility='collapsed'
    )

with metric_col3:
    st.markdown('**Value**')
    metric_series = master[selected_metric].dropna()
    default_val = float(metric_series.median())
    threshold = st.number_input(
        'Value',
        value=default_val,
        label_visibility='collapsed'
    )

st.markdown('---')

# Sort options
st.markdown('## Sort Results')

sort_col1, sort_col2 = st.columns(2)

with sort_col1:
    st.markdown('**Sort by**')
    sort_by_label = st.selectbox(
        'Sort by',
        options=list(metric_options.keys()),
        label_visibility='collapsed'
    )
    sort_by = metric_options[sort_by_label]

with sort_col2:
    st.markdown('**Order**')
    sort_order = st.selectbox(
        'Order',
        options=['Highest first', 'Lowest first'],
        label_visibility='collapsed'
    )

st.markdown('---')

# ============================================
# BUILD AND DISPLAY QUERY DESCRIPTION
# ============================================
condition_map = {
    'Greater than':             '>',
    'Less than':                '<',
    'Greater than or equal to': '>=',
    'Less than or equal to':    '<=',
}

condition_symbol = condition_map[condition]

query_parts = []
if selected_province != 'All provinces':
    query_parts.append(f"province = {selected_province}")
if selected_cluster != 'All clusters':
    query_parts.append(f"cluster = {selected_cluster}")
if selected_type != 'All types':
    type_code = selected_type.split('—')[0].strip()
    query_parts.append(
        f"municipality type = {type_code}")
query_parts.append(
    f"{selected_metric_label} "
    f"{condition_symbol} {threshold:,.2f}"
)

query_description = ' AND '.join(query_parts)

st.markdown('### Query')
st.code(
    f"SELECT municipalities WHERE {query_description}\n"
    f"ORDER BY {sort_by_label} "
    f"{'DESC' if sort_order == 'Highest first' else 'ASC'}",
    language='sql'
)

# ============================================
# RUN QUERY
# ============================================
if st.button('▶ Run Query', type='primary'):

    results = master.copy()

    # Apply province filter
    if selected_province != 'All provinces':
        results = results[
            results['province'] == selected_province
        ]

    # Apply cluster filter
    if selected_cluster != 'All clusters':
        results = results[
            results['cluster_name'].str.contains(
                selected_cluster.split('—')[0].strip(),
                na=False
            )
        ]

    # Apply type filter
    if selected_type != 'All types':
        type_code = selected_type[0]
        results = results[
            results['muni_category'] == type_code
        ]

    # Apply metric condition
    results = results.dropna(subset=[selected_metric])

    if condition_symbol == '>':
        results = results[
            results[selected_metric] > threshold]
    elif condition_symbol == '<':
        results = results[
            results[selected_metric] < threshold]
    elif condition_symbol == '>=':
        results = results[
            results[selected_metric] >= threshold]
    elif condition_symbol == '<=':
        results = results[
            results[selected_metric] <= threshold]

    # Apply sort
    ascending = sort_order == 'Lowest first'
    results = results.sort_values(
        sort_by, ascending=ascending)

    # ============================================
    # DISPLAY RESULTS
    # ============================================
    st.markdown(f'### Results — {len(results)} municipalities')

    if len(results) == 0:
        st.warning(
            'No municipalities match your query. '
            'Try adjusting the filters or threshold.'
        )
    else:
        display_cols = {
            'muni_name':          'Municipality',
            'province':           'Province',
            'muni_category':      'Type',
            'cluster_name':       'Cluster',
            'governance_score':   'Governance',
            'avg_taxable_income': 'Avg Income',
            'total_capex_rm':     'Capex (Rm)',
            'spending_ratio':     'Spend Ratio',
            'uifw_pct_budget':    'UIFW %',
        }

        available = [
            c for c in display_cols
            if c in results.columns
        ]

        table = results[available].rename(
            columns=display_cols)

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
        )

        # Summary stats
        st.markdown('### Summary Statistics')
        summary_cols = [
            c for c in [
                'avg_taxable_income',
                'governance_score',
                'spending_ratio',
                'uifw_pct_budget'
            ] if c in results.columns
        ]

        if summary_cols:
            summary = results[summary_cols].describe(
            ).round(2)
            summary.columns = [
                display_cols.get(c, c)
                for c in summary.columns
            ]
            st.dataframe(
                summary,
                use_container_width=True,
            )

        # Download button
        csv = table.to_csv(index=False)
        st.download_button(
            label='⬇ Download results as CSV',
            data=csv,
            file_name='municipality_query_results.csv',
            mime='text/csv',
        )

st.markdown('---')

# ============================================
# PRESET QUERIES
# ============================================
st.markdown('## Preset Queries')
st.caption(
    'Click any preset to populate the query '
    'builder with a meaningful starting point.'
)

presets = {
    'Worst governance nationally': {
        'description':
            'Municipalities with governance score '
            'of 0 or 1 — outstanding or disclaimer.',
        'filter': lambda df: df[
            df['governance_score'] <= 1
        ].sort_values('governance_score'),
    },
    'Severe underspending': {
        'description':
            'Municipalities spending less than '
            '30% of their capital budget.',
        'filter': lambda df: df[
            df['spending_ratio'] < 0.3
        ].sort_values('spending_ratio'),
    },
    'Extreme irregular expenditure': {
        'description':
            'Municipalities where UIFW exceeds '
            '100% of capital budget.',
        'filter': lambda df: df[
            df['uifw_pct_budget'] > 100
        ].sort_values(
            'uifw_pct_budget', ascending=False),
    },
    'Western Cape municipalities': {
        'description':
            'All Western Cape municipalities '
            'sorted by governance score.',
        'filter': lambda df: df[
            df['province'] == 'Western Cape'
        ].sort_values(
            'governance_score', ascending=False),
    },
    'High income poor governance': {
        'description':
            'Municipalities above national income '
            'average but below average governance.',
        'filter': lambda df: df[
            (df['avg_taxable_income'] >
             df['avg_taxable_income'].mean()) &
            (df['governance_score'] < 
             df['governance_score'].mean())
        ].sort_values(
            'avg_taxable_income', ascending=False),
    },
    'Free State financial crisis': {
        'description':
            'All Free State municipalities '
            'showing the governance paradox.',
        'filter': lambda df: df[
            df['province'] == 'Free State'
        ].sort_values('governance_score'),
    },
}

for preset_name, preset in presets.items():
    with st.expander(f'📊 {preset_name}'):
        st.caption(preset['description'])
        if st.button(
            f'Run: {preset_name}',
            key=f'preset_{preset_name}'
        ):
            preset_results = preset['filter'](
                master.copy())

            st.markdown(
                f'**{len(preset_results)} municipalities**'
            )

            display_cols = {
                'muni_name':          'Municipality',
                'province':           'Province',
                'cluster_name':       'Cluster',
                'governance_score':   'Governance',
                'avg_taxable_income': 'Avg Income',
                'spending_ratio':     'Spend Ratio',
                'uifw_pct_budget':    'UIFW %',
            }

            available = [
                c for c in display_cols
                if c in preset_results.columns
            ]

            st.dataframe(
                preset_results[available].rename(
                    columns=display_cols),
                use_container_width=True,
                hide_index=True,
            )

            csv = preset_results[available].rename(
                columns=display_cols
            ).to_csv(index=False)

            st.download_button(
                label='⬇ Download as CSV',
                data=csv,
                file_name=f'{preset_name.lower().replace(" ", "_")}.csv',
                mime='text/csv',
                key=f'download_{preset_name}'
            )

st.markdown('---')
st.caption(
    'Source: National Treasury Municipal Money 2021 · '
    'SARS Tax Statistics 2022'
)