# pip install mysql-connector-python
# pip install streamlit plotly mysql-connector-python
# pip install streamlit
# pip install streamlit_extras

import mysql.connector
import pandas as pd
import psycopg2
import streamlit as st
import PIL
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import requests
import geopandas as gpd

# connect to the database
import mysql.connector

# establishing the connection
conn = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', database="phonepe")

# create a cursor object
cursor = conn.cursor()

# with st.headbar:
SELECT = option_menu(
    menu_title=None,
    options=["About", "Home", "Top Charts", "Explore Data", "Contact"],
    icons=["exclamation-circle", "house", "bar-chart", "toggles", "at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})

# ----------------Home----------------------#
cursor = conn.cursor()

# execute a SELECT statement
cursor.execute("SELECT * FROM phonepe.data_aggregated_transaction_table")

# fetch all rows
rows = cursor.fetchall()
from streamlit_extras.add_vertical_space import add_vertical_space

if SELECT == "Home":
    col1, col2, = st.columns(2)
    col1.image(Image.open("C:\\Users\\Admin\\Desktop\\Phonepe_image2.png"), width=300)
    with col1:
        st.subheader(
            "PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:\\Users\\Admin\\Desktop\\upi.mp4")

# ----------------TOP CHARTS----------------------#

# MENU 2 - TOP CHARTS
if SELECT == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1, 1.8], gap="medium")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.info(
            """
            #### From this menu we can get insights like :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on the how many people use phonepe.
            """, icon="🔍"
        )

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(
                f"select state, sum(Total_Transactions_count) as Total_Transactions_count, sum(Transaction_amount) as Total from Data_Aggregated_Transaction_Table where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions_count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Transactions_count'],
                         labels={'Total_Transactions_count': 'Total_Transactions_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(
                f"select district , sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total from Data_Map_Transaction_Table where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction_count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transaction_count'],
                         labels={'Transaction_count': 'Transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Top Charts - USERS
    if Type == "Users":
        col1, col2, col3 = st.columns([2, 2, 2], gap="medium")

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                cursor.execute(
                    f"select Brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from Data_Aggregated_User_Table where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brands",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(
                f"select district, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from Data_Map_User_Table where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :violet[State]")
            cursor.execute(
                f"select state, sum(Registeredusers) as Total_Users, sum(AppOpens) as Total_Appopens from Data_Map_User_Table where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Appopens'],
                         labels={'Total_Appopens': 'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# ----------------EXPLORE DATA----------------------#


# MENU 3 - EXPLORE DATA
if SELECT == "Explore Data":
    Year = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.slider("Quarter", min_value=1, max_value=4)
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns(2)

    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(f"select state, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from Data_Map_Transaction_Table where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r"C:\\Users\\Admin\\Desktop\\Statenames.csv")
            df2.State = df1
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                       featureidkey='properties.ST_NM',
                       locations='State',
                       color='Total_amount',
                       color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(fig,use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            cursor.execute(f"select state, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from Data_Map_Transaction_Table where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(), columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r"C:\\Users\\Admin\\Desktop\\Statenames.csv")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df2.State = df1

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(
            f"select Transaction_type, sum(Total_Transactions_count) as Total_Transactions_count, sum(Transaction_amount) as Total_amount from Data_Aggregated_Transaction_Table where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions_count', 'Total_amount'])

        st.plotly_chart(fig, use_container_width=False)
        fig = px.bar(df,
                     title='Transaction Type vs Total_Transactions_count',
                     x="Transaction_type",
                     y="Total_Transactions_count",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        cursor.execute(
            f"select State, District,year,quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from Data_Map_Transaction_Table where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")

        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                       'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    # EXPLORE DATA - USERS
    if Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        cursor.execute(
            f"select state, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from Data_Map_User_Table where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        df2 = pd.read_csv(r"C:\\Users\\Admin\\Desktop\\Statenames.csv")
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df2.State = df1

        # BAR CHART TOTAL USERS - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        cursor.execute(
            f"select State,year,quarter,District,sum(Registeredusers) as Total_Users, sum(AppOpens) as Total_Appopens from Data_Map_User_Table where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")

        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'year', 'quarter', 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    # ----------------About-----------------------#

if SELECT == "About":
    col1, col2 = st.columns(2)
    with col1:
        st.video("C:\\Users\\Admin\\Desktop\\pulse-video.mp4")
    with col2:
        st.image(Image.open("C:\\Users\\Admin\\Desktop\\Phonepe_image2.png"), width=500)
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                     " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                     " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                     "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("C:\\Users\\Admin\\Desktop\\about_phonepe.jpg"), width=400)
        with open("C:\\Users\\Admin\\Desktop\\about_phonepe1.png", "rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT", data, file_name="annual report.pdf")
    with col2:
        st.image(Image.open("C:\\Users\\Admin\\Desktop\\about_phonepe1.png"), width=800)

# ----------------------Contact---------------#


if SELECT == "Contact":
    Name = (f'{"Name :"}  {"SASIKALA THENNARASU"}')
    mail = (f'{"Mail :"}  {"tsasionmail@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {

        "GITHUB": "https://github.com/SasikalaThennarasu/GUVI-CAPSTONE-PROJECTS",
        "LINKEDIN": "https://www.linkedin.com/in/sasikala-thennarasu-51a45259/"}

    st.title('Phonepe Pulse data visualisation')
    st.write("The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
    st.write("---")

    st.subheader(Name)
    st.subheader(mail)

    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")
