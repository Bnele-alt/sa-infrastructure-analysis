# ============================================
# charts.py
# Reusable chart functions for Streamlit pages
# ============================================
#
# PLANNED CONTENTS:
#
# This module is intended to hold reusable
# matplotlib/seaborn chart functions that can
# be called from any page in the dashboard
# without duplicating code.
#
# Planned functions:
#
# render_des_bar(des_df)
#   Horizontal bar chart of DES scores by province.
#   Used on overview and province pages.
#
# render_governance_bar(gov_df)
#   Horizontal bar chart of governance scores.
#   Used on overview and cluster pages.
#
# render_comparison_bar(muni_name, muni_vals,
#                       prov_vals, nat_vals)
#   Grouped bar chart comparing a municipality
#   against provincial and national averages.
#   Used on municipality explorer page.
#
# render_cluster_scatter(cluster_df)
#   Scatter plot of income vs governance
#   coloured by cluster membership.
#   Used on cluster explorer page.
#
# render_uifw_bar(cluster_df)
#   Bar chart of UIFW percentage by municipality.
#   Used on cluster and query builder pages.
#
# CURRENT STATUS:
#
# Chart code is currently written inline inside
# each page file. This module will be populated
# during a refactoring pass to centralise chart
# logic and make pages cleaner and more maintainable.
#
# To use this module in a page:
#   from utils.charts import render_des_bar
#   fig = render_des_bar(des_df)
#   st.pyplot(fig)
# ============================================