import streamlit as st 
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

#reading the data from excel file 
df = pd.read_excel("file_example_XLS_100.xls")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open("gradient-colored-computer-logo-template_23-2149182751.avif")

col1, col2 = st.columns([0.5,0.5])
with col1:
    st.image(image,width=200)   
    
html_title = """
    <style>
    .title-test 
    {
    font-weighted:bold;
    padding: 5px;
    border-radius: 6px;
    
}
</style>
<center><h1 style='text-align:center;'>SAAS DASHBOARD</h1></center>"""

st.markdown(html_title,unsafe_allow_html=True)
    
col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Latest Updated by:  \n {box_date}")
    
with col4:
        fig = px.bar(df, x = "First Name", y ="Last Name", labels={"Last Name" : "Last Name"},
                 title = "Representation of People through Age", hover_data=["Last Name"],
                 template="gridon", height=500)
        st.plotly_chart(fig,use_container_width=True)
    
_, view1 , dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Age Overview")
    data = df[["First Name","Last Name","Age"]].groupby(by="Age")["Last Name"].count()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                     file_name = "RetailerSales.csv",mime="text/csv")   
    
df["Age"]=df["Date"].dt.strftime("%b-%y")
result = df.groupby(by = "Age")["TotalPeople"].sum().reset_index()

with col5:
    fig1 = px.line(result, x = "Age", y = "TotalPeople",title= "Total people over time",
                   template="gridon")
    st.plotly_chart(fig1,use_container_width=True)
    