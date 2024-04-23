#!/usr/bin/env python
# coding: utf-8

# # Dashboard and visualization of KPIs

# ### Key Performance indicators

# - Using the Key Performance Indicators created earlier to design and display in the dashboard
#     - Average annual income by loan default risk
#     - Average age by loan default risk
#     - Average years of work experience by loan default risk
#     - Average years of current employment by loan default risk
#     - Average years of current residence by loan default risk
#     - Percentage of loan default risk by house ownership
#     - Percentage of loan default risk by vehicle ownership
#     - Distribution of customer’s occupation by loan default risk

# In[440]:


import streamlit as st
import pandas as pd
import numpy as np


# In[441]:


df = pd.read_csv('clean_data.csv')


# In[442]:


# Page configuration
img ='logo.png'
st.set_page_config(
    page_title="Loan Approval Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")


# In[443]:


# Set page title at the top center
st.markdown("<h1 style='text-align: center;'>Loan Approval Analysis Dashboard</h1>", unsafe_allow_html=True)


# ##### color list creation to avoid filtering error; orange(#EE7600)-1 and blue(#448EE4)-0

# In[444]:


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

# In[445]:


#Sidebar

with st.sidebar:
    st.title("Add Filter")
    
#     default_list = list(df['new_Loan_Default_Risk'].unique())[::-1]
#     selected_loan = st.selectbox('Loan default Risk', default_list)
    
    mar_grp = df['Marital_Status'].unique()
    selected_mar_grp= st.selectbox('Marital Status', mar_grp)
    
    age_grp = df['Applicant_Age_groups'].unique()
    selected_age_grp= st.selectbox('Age Group', age_grp)
    
    hs_grp = df['House_Ownership'].unique()
    selected_hs_grp= st.selectbox('House Ownership', hs_grp)
    
    ve_grp = df['Vehicle_Ownership(car)'].unique()
    selected_ve_grp= st.selectbox('Vehicle Ownership', ve_grp)


# ###### Average variables by loan default risk

# In[446]:


# Filter the DataFrame based on the selected options
filtered_df = df[(df['Marital_Status'] == selected_mar_grp) &
                 (df['Applicant_Age_groups'] == selected_age_grp) &
                 (df['House_Ownership'] == selected_hs_grp) &
                 (df['Vehicle_Ownership(car)'] == selected_ve_grp)]


# In[447]:


# Exempts Errors: ValueError to return 0, TypeError to return '-' and every other errors to return '-'
try:        
    app_cou = filtered_df['Applicant_ID'].count()
    value_appl_count = int(app_cou/1000)
    if app_cou < 10000:
        value_appl_count = app_cou
    elif app_cou >= 10000:
        value_appl_count = str(value_appl_count) + 'K'
except ValueError as c:
    value_appl_count = 0
except TypeError as tec:
    value_income_avg = '-'
except Exception as ec:
    value_income_avg = '-'

try:
    app_inc_avg = filtered_df['Annual_Income'].mean()
    value_income_avg = int(app_inc_avg/1000)
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
    value_Age_avg = int(filtered_df['Applicant_Age'].mean())
except ValueError as a:
    value_Age_avg = 0
except TypeError as tea:
    value_income_avg = '-'
except Exception as ea:
    value_income_avg = '-'

try:
    value_Work_avg = int(filtered_df['Work_Experience'].mean())
except ValueError as w:
    value_Work_avg = 0
except TypeError as tew:
    value_income_avg = '-'
except Exception as ew:
    value_income_avg = '-'
    
try:
    value_Employment_avg = int(filtered_df['Years_in_Current_Employment'].mean())
except ValueError as em:
    value_Employment_avg = 0
except TypeError as teem:
    value_income_avg = '-'
except Exception as eem:
    value_income_avg = '-'
    
try:
    value_Residence_avg = int(filtered_df['Years_in_Current_Residence'].mean())
except ValueError as re:
    value_Residence_avg = 0
except TypeError as tere:
    value_income_avg = '-'
except Exception as ere:
    value_income_avg = '-'


# In[448]:


# # Dashboard Main Panel

col = st.columns((2,3,2,2,2,2), gap='medium')

# Display metrics in the first row
with col[0]:
    st.metric(label='No. Applicants', value=str(int(filtered_df['Applicant_ID'].count()/1000)) + 'K')
with col[1]:
    st.metric(label='Avg. Income', value=str(int(filtered_df['Annual_Income'].mean()/1000)) + 'K')
with col[2]:
    st.metric(label='Avg. Age', value=int(filtered_df['Applicant_Age'].mean()))
with col[3]:
    st.metric(label='Avg. Work', value=int(filtered_df['Work_Experience'].mean()))
with col[4]:
    st.metric(label='Avg. CurrEmployment', value=int(filtered_df['Years_in_Current_Employment'].mean()))
with col[5]:
    st.metric(label='Avg. CurrResidence', value=int(filtered_df['Years_in_Current_Residence'].mean()))


# ###### Percentage of loan default risk by house ownership, Vehicle ownership, and Marital status

# In[449]:


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

# In[450]:


# Display the third bar chart in the second row
st.markdown("##### Occupational categories")
Occupation = pd.crosstab(filtered_df['Occupation_Group'], filtered_df['new_Loan_Default_Risk'])
occu_stack = Occupation.div(Occupation.sum(1).astype(float), axis=0).mul(100)
st.bar_chart(occu_stack, use_container_width=True, color=color_loan(occu_stack))

