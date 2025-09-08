import streamlit as st
import pandas as pd
import altair as alt 

st.set_page_config(layout="wide")
#

df = pd.read_csv('Telco_customer_churn.csv')

st.sidebar.header('Customer Filters')


contract_filter = st.sidebar.multiselect(
    'Select a Contract Type:',
    options=df['Contract'].unique(),
    default=df['Contract'].unique()
)



internet_service_filter = st.sidebar.multiselect(
    'Select an Internet Service Type:',
    options=df['Internet Service'].unique(),
    default=df['Internet Service'].unique()
)

tenure_filter = st.slider(
    'Select Tenure Months:',
    min_value=int(df['Tenure Months'].min()),
    max_value=int(df['Tenure Months'].max()),
    value=(int(df['Tenure Months'].min()), int(df['Tenure Months'].max()))
)


filtered_df = df[
  (df['Contract'].isin(contract_filter)) &
  (df['Internet Service'].isin(internet_service_filter)) &
  (df['Tenure Months'] >= tenure_filter[0]) & (df['Tenure Months'] <= tenure_filter[1])
]

total_customers = filtered_df.shape[0] 

# Calculating the Churn Rate per each Contract Type
churn_rate_by_contract = filtered_df.groupby('Contract')['Churn Value'].mean().reset_index()

churn_rate_by_contract_chart = alt.Chart(churn_rate_by_contract).mark_bar().encode(
    y=alt.X('Contract:N', title=''),
    x=alt.Y('Churn Value:Q', title='Churn Rate', axis=alt.Axis(format='%')),
    color='Contract'
).properties(
    title='Churn Rate by Contract Type'
)


churn_rate_by_internet_service = filtered_df.groupby('Internet Service')['Churn Value'].mean().reset_index()
churn_rate_by_internet_service_chart = alt.Chart(churn_rate_by_internet_service).mark_bar().encode(
    y=alt.X('Internet Service:N', title=''),
    x=alt.Y('Churn Value:Q', title='Churn Rate', axis=alt.Axis(format='%')),
    color='Internet Service'
).properties(
    title='Churn Rate by Internet Service Type'
)

churn_reasons = filtered_df[filtered_df['Churn Reason'] != 'Don\'t know'].groupby('Churn Reason')['Count'].sum().sort_values(ascending=False).reset_index().head()


tab1, tab2 = st.tabs(["Churn Overview", "Deep Dive"])


with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Total Customers",
            value=filtered_df.shape[0],

        )
    with col2:
         churn_rate = filtered_df['Churn Value'].mean()
         st.metric(
         label="Overall Churn Rate",
         value=f"{churn_rate:.1%}" # Format as a percentage
    )

    st.altair_chart(churn_rate_by_contract_chart, use_container_width=True)

    st.altair_chart(churn_rate_by_internet_service_chart, use_container_width=True)

  
with tab2:

  
  churn_reasons_count = alt.Chart(churn_reasons).mark_bar().encode( 
      y=alt.X('Churn Reason', title='', sort='-x'),
      x=alt.Y('Count', title=''),
      color='Churn Reason'
      ).properties(
          title = 'Top 5 Churn Reasons'
      )

  
  st.altair_chart(churn_reasons_count, use_container_width=True)











