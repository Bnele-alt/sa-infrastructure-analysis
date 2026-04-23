# ============================================
# sql_templates.py
# SQL query templates for the query builder
# ============================================
#
# PLANNED CONTENTS:
#
# This module is intended to hold SQL template
# strings and a query execution function using
# pandasql — a library that allows running
# standard SQL queries against pandas DataFrames.
#
# Planned templates:
#
# QUERY_TOP_INCOME
#   SELECT muni_name, province, avg_taxable_income
#   FROM master
#   ORDER BY avg_taxable_income DESC
#   LIMIT 10
#
# QUERY_WORST_GOVERNANCE
#   SELECT muni_name, province, governance_score,
#          opinion_label
#   FROM master
#   WHERE governance_score <= 1
#   ORDER BY governance_score ASC
#
# QUERY_HIGH_UIFW
#   SELECT muni_name, province, uifw_pct_budget,
#          cluster_name
#   FROM master
#   WHERE uifw_pct_budget > 100
#   ORDER BY uifw_pct_budget DESC
#
# QUERY_PROVINCE_SUMMARY
#   SELECT province,
#          AVG(governance_score) as avg_governance,
#          AVG(avg_taxable_income) as avg_income,
#          AVG(spending_ratio) as avg_spending,
#          COUNT(*) as municipality_count
#   FROM master
#   GROUP BY province
#   ORDER BY avg_governance DESC
#
# QUERY_CLUSTER_PROFILE
#   SELECT cluster_name,
#          AVG(avg_taxable_income) as avg_income,
#          AVG(governance_score) as avg_governance,
#          AVG(uifw_pct_budget) as avg_uifw,
#          COUNT(*) as count
#   FROM master
#   GROUP BY cluster_name
#
# Planned execution function:
#
# def run_query(template, master_df):
#   import pandasql as ps
#   master = master_df
#   return ps.sqldf(template, locals())
#
# CURRENT STATUS:
#
# Query builder page currently uses pandas
# boolean filters instead of SQL. This module
# will be populated when pandasql is integrated
# to allow users to write and run raw SQL queries
# directly against the municipal dataset.
#
# To install pandasql:
#   py -3.12 -m pip install pandasql
#
# To use this module in a page:
#   from utils.sql_templates import run_query
#   results = run_query(QUERY_WORST_GOVERNANCE,
#                       master_df)
# ============================================