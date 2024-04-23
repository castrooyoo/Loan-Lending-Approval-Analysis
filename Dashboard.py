#!/usr/bin/env python
# coding: utf-8

# # Dashboard and visualization of KPIs

# ### Key Performance indicators

# - Using the Key Performance Indicators created earlier to design and display in the dashboard
#     - Total Applicants
#     - Rate of loan default Risk (computed total applicants with loan default risk/total applicants)
#     - Average annual income by loan default risk
#     - Average age by loan default risk
#     - Average years of work experience by loan default risk
#     - Average years of current employment by loan default risk
#     - Average years of current residence by loan default risk
#     - Percentage of loan default risk by house ownership
#     - Percentage of loan default risk by vehicle ownership
#     - Distribution of applicants' occupation by loan default risk

# In[247]:


import streamlit as st
import pandas as pd
import numpy as np


# In[248]:


df = pd.read_csv('clean_data.csv')


# In[249]:


# Page configuration
img ='logo.png'
st.set_page_config(
    page_title="Loan Approval Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")


# In[250]:


# Set page title at the top center
st.markdown("<h1 style='text-align: center;'>Loan Approval Analysis Dashboard</h1>", unsafe_allow_html=True)


# ##### color list creation to avoid filtering error; orange(#EE7600)-1 and blue(#448EE4)-0

# In[251]:


def color_loan(val):
    val = list(val.columns)
    try:
        colors = []
        if len(val) > 0:
            for i in val:
                if i == 'default':
                    colors.append('#448EE4')  # Orange
                elif i == 'non default':
                    colors.append('#EE7600')  # Blue
            return colors
        else:
            print()
    except Exception as e:
        print(f'No loan default risk data: {e}')


# ###### Adding Slicer

# ###### Side bar - Slicer/Filter

# In[252]:


#Sidebar

with st.sidebar:
    st.title("Filter")
    selected_mar_grp = st.selectbox('Marital Status', ['select option'] + list(df['Marital_Status'].unique()), placeholder="select option")
    selected_age_grp = st.selectbox('Age Group', ['select option'] + list(df['Applicant_Age_groups'].unique()),placeholder="select option")
    selected_hs_grp = st.selectbox('House Ownership', ['select option'] + list(df['House_Ownership'].unique()),placeholder="select option")
    selected_ve_grp = st.selectbox('Vehicle Ownership', ['select option'] + list(df['Vehicle_Ownership(car)'].unique()),placeholder="select option")


# In[253]:


# with st.sidebar: #reset slicer
#     reset_slicer= st.button('Reset slicer')
#     if reset_slicer:
#         selected_mar_grp = 'select option'
#         selected_age_grp = 'select option'
#         selected_hs_grp = 'select option'
#         selected_ve_grp = 'select option'


# ###### Average variables by loan default risk

# In[254]:


# Filter the DataFrame based on the selected options
filtered_df = df[
    ((df['Marital_Status'] == selected_mar_grp) | (selected_mar_grp == 'select option')) &
    ((df['Applicant_Age_groups'] == selected_age_grp) | (selected_age_grp == 'select option')) &
    ((df['House_Ownership'] == selected_hs_grp) | (selected_hs_grp == 'select option')) &
    ((df['Vehicle_Ownership(car)'] == selected_ve_grp) | (selected_ve_grp == 'select option'))
]


# In[255]:


#creating a reset button for the data filtered
with st.sidebar:
    reset_dashboard = st.button('Reset')
    if reset_dashboard:
        filtered_df = df # revert dataset to the main df ie from filtered_df back to df


# In[256]:


# Exempts Errors: ValueError to return 0, TypeError to return '-' and every other errors to return '-'

try:        
    ldr_default_div = filtered_df[filtered_df['Loan_Default_Risk']==1]['Applicant_ID'].count()/len(filtered_df['Loan_Default_Risk'])
    value_ldr_rate = round((ldr_default_div)*(100))
    value_ldr_rate1 = str(value_ldr_rate) + '%'
except ValueError as l:
    value_ldr_rate1 = 0
except TypeError as tel:
    value_ldr_rate1 = '-'
except TypeError as el:
    value_ldr_rate1 = '-'

try:        
    app_cou = filtered_df['Applicant_ID'].count()
    value_appl_count = round(app_cou/1000)
    if app_cou < 10000:
        value_appl_count = app_cou
    elif app_cou >= 10000:
        value_appl_count = str(value_appl_count) + 'K'
except ValueError as c:
    value_appl_count = 0
except TypeError as tec:
    value_appl_count = '-'
except Exception as ec:
    value_appl_count = '-'

try:
    app_inc_avg = filtered_df['Annual_Income'].mean()
    value_income_avg = round(app_inc_avg/1000)
    if app_inc_avg < 1000:
        value_income_avg = app_inc_avg
    elif app_inc_avg >= 1000:
        value_income_avg = str(value_income_avg) + 'K'
except ValueError as i:
    value_income_avg = 0
except TypeError as tei:
    value_income_avg = '-'
except Exception as ei:
    value_income_avg = '-'

try:
    value_Age_avg = round(filtered_df['Applicant_Age'].mean())
except ValueError as a:
    value_Age_avg = 0
except TypeError as tea:
    value_Age_avg = '-'
except Exception as ea:
    value_Age_avg = '-'

try:
    value_Work_avg = round(filtered_df['Work_Experience'].mean())
except ValueError as w:
    value_Work_avg = 0
except TypeError as tew:
    value_Work_avg = '-'
except Exception as ew:
    value_Work_avg = '-'
    
try:
    value_Employment_avg = round(filtered_df['Years_in_Current_Employment'].mean())
except ValueError as em:
    value_Employment_avg = 0
except TypeError as teem:
    value_Employment_avg = '-'
except Exception as eem:
    value_Employment_avg = '-'
    
try:
    value_Residence_avg = round(filtered_df['Years_in_Current_Residence'].mean())
except ValueError as re:
    value_Residence_avg = 0
except TypeError as tere:
    value_Residence_avg = '-'
except Exception as ere:
    value_Residence_avg = '-'


# In[257]:


# # Dashboard Main Panel

col = st.columns((2,3,2,2,2,2,2), gap='small')

# Display metrics in the first row
with col[0]:
    st.metric(label='LDR Rate', value=value_ldr_rate1)
with col[1]:
    st.metric(label='No. Applicants', value=value_appl_count)
with col[2]:
    st.metric(label='Avg. Income', value=value_income_avg)
with col[3]:
    st.metric(label='Avg. Age', value=value_Age_avg)
with col[4]:
    st.metric(label='Avg. Work', value=value_Work_avg)
with col[5]:
    st.metric(label='Avg. CurrEmployment', value=value_Employment_avg)
with col[6]:
    st.metric(label='Avg. CurrResidence', value=value_Residence_avg)


# ###### Percentage of loan default risk by house ownership, Vehicle ownership, and Marital status

# In[258]:


# Create columns for layout

col1, col2, col3 = st.columns(3)  # Ratio of 2:1 for the first row
# col3 = st.columns(2)  # Full width for the second row


# Display bar charts in the first row
with col1:
    st.markdown("##### House ownership status")
    house = pd.crosstab(filtered_df['House_Ownership'], filtered_df['new_Loan_Default_Risk'])
    hs_stack = house.div(house.sum(1).astype(float), axis=0).mul(100)
    st.bar_chart(hs_stack, use_container_width=True, color=color_loan(hs_stack))

with col2:
    st.markdown("##### Vehicle ownership status")
    vehicle = pd.crosstab(filtered_df['Vehicle_Ownership(car)'], filtered_df['new_Loan_Default_Risk'])
    veh_stack = vehicle.div(vehicle.sum(1).astype(float), axis=0).mul(100)
    st.bar_chart(veh_stack, use_container_width=True, color=color_loan(veh_stack))

with col3:
    st.markdown("##### Marital status")
    marital = pd.crosstab(filtered_df['Marital_Status'], filtered_df['new_Loan_Default_Risk'])
    mar_stack = marital.div(marital.sum(1).astype(float), axis=0).mul(100)
    st.bar_chart(mar_stack, use_container_width=True, color=color_loan(mar_stack))


# ###### Distribution of customer’s occupation by loan default risk

# In[259]:


# Display the third bar chart in the second row
st.markdown("##### Occupational categories")
Occupation = pd.crosstab(filtered_df['Occupation_Group'], filtered_df['new_Loan_Default_Risk'])
occu_stack = Occupation.div(Occupation.sum(1).astype(float), axis=0).mul(100)
st.bar_chart(occu_stack, use_container_width=True, color=color_loan(occu_stack))

