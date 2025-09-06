import streamlit as st
import pandas as pd
import altair as alt

st.title("Hello, Streamlit!")   


df = pd.DataFrame({
    'Category': ['A', 'B', 'C'],
    'Value': [10, 20, 30], 
    'Product': ['Apple', 'Banana', 'Carrot']
}) 


option = st.selectbox('Select a category:', df['Category'])

filtered_df = df[df['Category'] == option] 

st.write(filtered_df)

chart = alt.Chart(filtered_df).mark_bar().encode(
    x='Product',
    y='Value'
).properties(
    title='Product Value by Category'
)

st.altair_chart(chart, use_container_width=True)