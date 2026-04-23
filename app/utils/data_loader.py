# ============================================
# data_loader.py
# Central data loading module for Streamlit
# All datasets loaded once and cached
# ============================================

import pandas as pd
import os

# ============================================
# PATH CONFIGURATION
# Works whether running from app/ or project root
# ============================================
def get_data_path(filename):
    """
    Returns the correct path to a cleaned data file
    regardless of where Streamlit is launched from.
    """
    # Try relative to this file first
    base = os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    ))
    path = os.path.join(base, 'data', 'cleaned', filename)
    if os.path.exists(path):
        return path
    # Fallback
    return os.path.join('data', 'cleaned', filename)


def get_outputs_path(filename):
    """Returns path to outputs folder."""
    # data_loader.py lives at app/utils/data_loader.py
    # so we need to go up 3 levels to reach project root
    utils_dir   = os.path.dirname(os.path.abspath(__file__))
    app_dir     = os.path.dirname(utils_dir)
    project_dir = os.path.dirname(app_dir)
    return os.path.join(project_dir, 'outputs', filename)


def get_assets_path(filename):
    """Returns path to app/assets folder."""
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        os.path.dirname(base), 'assets', filename)


# ============================================
# CACHED DATA LOADERS
# @st.cache_data means Streamlit loads each
# dataset once and reuses it across all pages
# without hitting disk again
# ============================================

import streamlit as st

@st.cache_data
def load_master():
    """
    Master municipal dataset.
    248 A and B municipalities.
    18 columns including income, governance,
    capex spending and UIFW.
    """
    return pd.read_csv(
        get_data_path('master_municipal_2021.csv')
    )


@st.cache_data
def load_clusters():
    """
    K-means cluster assignments.
    205 municipalities with complete data.
    4 clusters: Operational, At Risk,
    Failing, Critical.
    """
    return pd.read_csv(
        get_data_path('municipal_clusters_2021.csv')
    )


@st.cache_data
def load_audit():
    """
    Audit opinions 2021.
    257 municipalities.
    Governance scores 0-5.
    """
    return pd.read_csv(
        get_data_path('municipal_audit_2021_cleaned.csv')
    )


@st.cache_data
def load_capex():
    """
    Capital expenditure 2021.
    247 municipalities.
    Actual spend vs adjusted budget.
    """
    return pd.read_csv(
        get_data_path('municipal_capex_2021_cleaned.csv')
    )


@st.cache_data
def load_uifw():
    """
    UIFW irregular expenditure 2021.
    257 municipalities.
    Fruitless, irregular and unauthorised.
    """
    return pd.read_csv(
        get_data_path('municipal_uifw_2021_cleaned.csv')
    )


@st.cache_data
def load_pit():
    """
    SARS personal income tax 2021.
    213 municipalities with formal taxpayers.
    """
    return pd.read_csv(
        get_data_path('SARS_municipal_PIT_2021_cleaned.csv')
    )


@st.cache_data
def load_reference():
    """
    Municipality reference table.
    292 municipalities with names,
    provinces and categories.
    """
    return pd.read_csv(
        get_data_path('municipality_reference_cleaned.csv')
    )


@st.cache_data
def load_master_enriched():
    """
    Master dataset merged with cluster assignments.
    Used by most pages as the primary dataframe.
    """
    master   = load_master()
    clusters = load_clusters()

    enriched = master.merge(
        clusters[[
            'muni_code', 'cluster', 'cluster_name',
            'avg_taxable_income', 'governance_score',
            'spending_ratio', 'uifw_pct_budget'
        ]],
        on='muni_code',
        how='left',
        suffixes=('', '_cluster')
    )
    return enriched


# ============================================
# PROVINCE LIST
# Used by dropdowns throughout the dashboard
# ============================================
PROVINCES = [
    'Eastern Cape',
    'Free State',
    'Gauteng',
    'KwaZulu-Natal',
    'Limpopo',
    'Mpumalanga',
    'North West',
    'Northern Cape',
    'Western Cape',
]

# ============================================
# CLUSTER METADATA
# Used by cluster explorer and tooltips
# ============================================
CLUSTER_NAMES = {
    0: 'At Risk — High irregular expenditure',
    1: 'Operational — Moderate governance',
    2: 'Failing — No financial accountability',
    3: 'Critical — Extreme budget breach',
}

CLUSTER_COLORS = {
    0: '#fc8d59',
    1: '#1a9850',
    2: '#d73027',
    3: '#4575b4',
}

CLUSTER_DESCRIPTIONS = {
    0: (
        'Municipalities with mixed governance quality '
        'but extreme levels of irregular, unauthorised '
        'or wasteful expenditure. Often includes '
        'resource-rich areas like mining municipalities '
        'where wealth does not translate to financial '
        'discipline. Average UIFW exceeds 159% of '
        'capital budget.'
    ),
    1: (
        'The largest cluster — 125 municipalities. '
        'Broadly functional with moderate to good '
        'governance scores. Low irregular expenditure. '
        'Includes most Western Cape and Gauteng '
        'municipalities as well as well-run local '
        'municipalities across all provinces. '
        'Note: operational does not mean perfect — '
        'some members still have concerning UIFW levels.'
    ),
    2: (
        'Municipalities where financial accountability '
        'has effectively broken down. Average governance '
        'score of 0.36 — meaning most cannot produce '
        'audited financial statements. Concentrated in '
        'Free State and Northern Cape. These '
        'municipalities exist politically but are '
        'largely invisible to the formal accountability '
        'system.'
    ),
    3: (
        'Two municipalities so extreme in capital '
        'budget overspending they form their own cluster. '
        'uMshwathi (KZN) spent 17x its adjusted budget. '
        'Sundays River Valley (EC) spent 29x its budget. '
        'Isolated by the algorithm as statistical '
        'outliers requiring individual investigation.'
    ),
}

# ============================================
# GOVERNANCE SCORE LABELS
# ============================================
GOVERNANCE_LABELS = {
    5: 'Unqualified — Clean audit',
    4: 'Unqualified — Emphasis of matter',
    3: 'Qualified opinion',
    2: 'Adverse opinion',
    1: 'Disclaimer of opinion',
    0: 'Outstanding — Not submitted',
}