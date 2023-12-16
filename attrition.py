import streamlit as st
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import pickle
import sklearn
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#------------------------------------------------------------------------------------------------------
 #Configuring Streamlit GUI 
st.set_page_config(layout='wide')

# Title
st.title(':blue[EMPLOYEE ATTRITION PREDICTION]')
model = pickle.load (open ('rfc.pkl','rb'))


# Tabs 
tab1, tab2 = st.tabs(["ATTRITION PREDICTION", "INSIGHTS"])
#---------------------------------------------------------------------------------------------------------

with tab1:
    st.title("Employee Details Form")

# Create input widgets for each field
    age = st.text_input("Age")
    business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
    
    department = st.radio("Department", ["Human Resources", "Sales", "Research & Development"])
    distance_from_home = st.text_input("Distance From Home")
    st.write("1-Below college,2-college,3-Bachelor,4-Master,5-Doctor")
    education = st.selectbox("Education", [1, 2, 3, 4, 5])
    education_field = st.selectbox("Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree","Human Resources", "Other"])
    st.write("1-Low,2-Medium,3-High,4-Very High")
    environment_satisfaction = st.selectbox("Environment Satisfaction", [1, 2, 3, 4])
    gender = st.radio("Gender", ["Male", "Female"])
    
    st.write("1-Low,2-Medium,3-High,4-Very High")
    job_involvement = st.selectbox("Job Involvement", [1, 2, 3, 4])
    job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])
    job_role = st.selectbox("Job Role", ["Sales Executive","Manufacturing Director","Healthcare Representative","Manager","Research Director","Labortory Technician","Sales Representative", "Research Scientist","Other"])
    job_satisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4])
    marital_status = st.radio("Marital Status", ["Single", "Married", "Divorced"])
    monthly_income = st.text_input("Monthly Income")
    PercentSalaryHike=st.text_input("PercentSalaryHike")
    num_companies_worked = st.text_input("Number of Companies Worked in")
    overtime = st.radio("Over Time", ["Yes", "No"])
    st.write("1-Low,2-Medium,3-High,4-Very High")
    performance_rating = st.selectbox("Performance Rating", [1,2,3, 4])
    
    stock_option_level = st.selectbox("Stock Option Level", [0, 1, 2, 3])
    total_working_years = st.text_input("Total Working Years")
    training_times_last_year = st.text_input("Training Times Last Year")
    work_life_balance = st.selectbox("Work Life Balance", [1, 2, 3, 4])
    years_at_company = st.text_input("Years At Company")
    
    years_since_last_promotion = st.text_input("Years Since Last Promotion")
    years_with_curr_manager = st.text_input("Years With Curr Manager")


# Add a button to submit the form
    if st.button("Submit"):
        # Perform any data processing or analysis here
        data= {
        'Age': int(age),
        'BusinessTravel': business_travel,
        'Department': department,
        'DistanceFromHome': int(distance_from_home),
        'Education': education,
        'EducationField': education_field,
        'EnvironmentSatisfaction': environment_satisfaction,
        'Gender': gender,
        'JobInvolvement': job_involvement,
        'JobLevel': job_level,
        'JobRole': job_role,
        'JobSatisfaction': job_satisfaction,
        'MaritalStatus': marital_status,
        'MonthlyIncome': int(monthly_income),
        'NumCompaniesWorked': int(num_companies_worked),
        'PercentSalaryHike': int(PercentSalaryHike),
        'OverTime': overtime,
        'PerformanceRating': int(performance_rating),
        'StockOptionLevel': stock_option_level,
        'TotalWorkingYears': int(total_working_years),
        'TrainingTimesLastYear': int(training_times_last_year),
        'WorkLifeBalance': work_life_balance,
        'YearsAtCompany': int(years_at_company),
        'YearsSinceLastPromotion': int(years_since_last_promotion),
        'YearsWithCurrManager': int(years_with_curr_manager)
        }
        df = pd.DataFrame ([data])

        df['TotalSatisfaction'] = (df['EnvironmentSatisfaction'] +
                                    df['JobInvolvement'] +
                                    df['JobSatisfaction'] +
                                    df['PerformanceRating'] +
                                    df['WorkLifeBalance']) / 5

        # Drop Columns
        df.drop (
            ['EnvironmentSatisfaction','JobInvolvement','JobSatisfaction',"OverTime","YearsWithCurrManager",'PerformanceRating','WorkLifeBalance'],
            axis=1,inplace=True)
        # Map categorical values to numeric values
        df['BusinessTravel'] = df['BusinessTravel'].replace({"Travel_Rarely": 2, "Travel_Frequently": 3, "Non-Travel": 4})
        df['Gender'] = df['Gender'].replace({"Male": 1, "Female": 0})
        df['MaritalStatus'] = df['MaritalStatus'].replace({"Single": 1, "Married": 2, "Divorced": 3})
        df['Department'] = df['Department'].replace({"Sales": 1, "Human Resources": 2, "Research & Development": 3})
        df['EducationField'] = df['EducationField'].replace({"Life Sciences": 1, "Medical": 2, "Marketing": 3, "Technical Degree": 4, "Human Resources": 5, "Other": 0})
        df['JobRole'] = df['JobRole'].replace({"Sales Executive": 1, "Manufacturing Director": 2, "Healthcare Representative": 3, "Manager": 4, "Research Director": 5, "Laboratory Technician": 6, "Sales Representative": 7, "Research Scientist": 8, "Human Resources": 9})

        st.write(df)
   #if st.button("PREDICT"):
        prediction = model.predict(df)
       
        if prediction == 0:
            st.write('Employee Might Not Leave The Job')

        elif prediction == 1:
          st.write('Employee Might Leave The Job')
        else:
            st.write("error")
#-------------------------------------------------------------------------------------------------------------
with tab2:
   # Connect to the MySQL server
    connect = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "98655",
    database="final"
    )

    # Create a new database and use
    cursor = connect.cursor()
    engine = create_engine('mysql+pymysql://root:98655@localhost/final', echo=False)
    st.markdown("<h2 style='color: blue;'>Insights</h2>", unsafe_allow_html=True)
   
    question_tosql = st.selectbox('**Select your Question**',
    ('1. Age Distribution by Attrition Category',
    '2. Attrition by Gender',
    '3. JobLevel vs Attrition and JobRole vs Attrition',
    '4. Marital Status vs Attrition',
    '5. BusinessTravel and Attrition',
    "6. MonthlyIncome vs Attrition",
    "7. EducationField vs Attrition",
    "8. PercentSalaryHike and Attrition",
    "9. TotalSatisfaction vs Attrition",
    "10.Observations")
    , key = 'collection_question')
    if question_tosql == '1. Age Distribution by Attrition Category':
        cursor.execute("SELECT Attrition, Age, COUNT(*) as NumberOfEmployees FROM data GROUP BY Attrition, Age ORDER BY Attrition, Age;")
        result_1 = cursor.fetchall()
        df1 = pd.DataFrame(result_1, columns=['Attrition', 'Age',"NumberOfEmployees"]).reset_index(drop=True)
        df1.index += 1
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(df1)
        with col2:
            fig = px.bar(
            df1, 
                x='Age', 
                y='NumberOfEmployees', 
                color='Attrition', 
                labels={'NumberOfEmployees': 'Number of Employees'},
                title='Age Distribution by Attrition Category'
            )

            st.plotly_chart(fig)
    
    if question_tosql == '2. Attrition by Gender':
        
            cursor.execute("SELECT Gender, Attrition, COUNT(*) as NumberOfEmployees FROM data GROUP BY Gender, Attrition ORDER BY Gender, Attrition;")
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=['Gender', 'Attrition', 'NumberOfEmployees']).reset_index(drop=True)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df)
            

            # # Create a bar chart using Plotly Express
            with col2:
                fig = px.bar(
                    df, 
                    x='Gender', 
                    y='NumberOfEmployees', 
                    color='Attrition', 
                    labels={'NumberOfEmployees': 'Number of Employees'},
                    title='Attrition by Gender'
                )
                st.plotly_chart(fig)

            

    if question_tosql== '3. JobLevel vs Attrition and JobRole vs Attrition':
        cursor.execute("SELECT JobLevel, Attrition, COUNT(*) as NumberOfEmployees FROM data GROUP BY JobLevel, Attrition ORDER BY JobLevel, Attrition;")
        result_job_level = cursor.fetchall()
        df_job_level = pd.DataFrame(result_job_level, columns=['JobLevel', 'Attrition', 'NumberOfEmployees']).reset_index(drop=True)

        cursor.execute("SELECT JobRole, Attrition, COUNT(*) as NumberOfEmployees FROM data GROUP BY JobRole, Attrition ORDER BY JobRole, Attrition;")
        result_job_role = cursor.fetchall()
        df_job_role = pd.DataFrame(result_job_role, columns=['JobRole', 'Attrition', 'NumberOfEmployees']).reset_index(drop=True)

        # Display the results in two columns
        col1, col2 = st.columns(2)

        # Column 1: JobLevel vs. Attrition with Line Chart
        with col1:
            st.header('JobLevel vs. Attrition')
            st.dataframe(df_job_level)
            fig_job_level = px.line(
                df_job_level, 
                x='JobLevel', 
                y='NumberOfEmployees', 
                color='Attrition', 
                labels={'NumberOfEmployees': 'Number of Employees'},
                title='Attrition by JobLevel'
            )
            st.plotly_chart(fig_job_level)

        # Column 2: JobRole vs. Attrition with Pie Chart
        with col2:
            st.header('JobRole vs. Attrition')
            st.dataframe(df_job_role)
            colors = ['lightcoral', 'lightskyblue']
            fig_job_role = go.Figure(go.Pie(
                labels=df_job_role['JobRole'],
                values=df_job_role['NumberOfEmployees'],
                hole=0.3,
                marker=dict(colors=colors),
                title='Attrition by JobRole'
            ))
            st.plotly_chart(fig_job_role)
            
    if question_tosql=="4. Marital Status vs Attrition":
        cursor.execute("SELECT MaritalStatus, COUNT(*) as NumberOfEmployees FROM data GROUP BY MaritalStatus;")
        result_marital_status = cursor.fetchall()
        df_marital_status = pd.DataFrame(result_marital_status, columns=['MaritalStatus', 'NumberOfEmployees']).reset_index(drop=True)
        col1,col2=st.columns(2)
        with col1:
            st.write(df_marital_status)
        with col2:
        # Display a Donut Chart for MaritalStatus
            fig_marital_status_donut = px.pie(
                df_marital_status,
                names='MaritalStatus',
                values='NumberOfEmployees',
                title='Marital Status Distribution',
                hole=0.3
            )
            st.plotly_chart(fig_marital_status_donut)
    
    if question_tosql=='5. BusinessTravel and Attrition':
        
        cursor.execute("SELECT BusinessTravel, Attrition, COUNT(*) as NumberOfEmployees FROM data GROUP BY BusinessTravel, Attrition ORDER BY BusinessTravel, Attrition;")
        result_business_travel = cursor.fetchall()
        df_business_travel = pd.DataFrame(result_business_travel, columns=['BusinessTravel', 'Attrition', 'NumberOfEmployees']).reset_index(drop=True)

        # Display the Stacked Bar Chart for BusinessTravel vs. Attrition
        fig_business_travel = px.bar(
            df_business_travel,
            x='BusinessTravel',
            y='NumberOfEmployees',
            color='Attrition',
            title='Business Travel vs. Attrition',
            labels={'NumberOfEmployees': 'Number of Employees'},
            barmode='stack'
        )
        st.plotly_chart(fig_business_travel)

    if question_tosql=="6. MonthlyIncome vs Attrition":
        cursor.execute("SELECT Attrition, MonthlyIncome FROM data;")
        result_monthly_income = cursor.fetchall()
        df_monthly_income = pd.DataFrame(result_monthly_income, columns=['Attrition', 'MonthlyIncome']).reset_index(drop=True)

        # Display the Scatter Plot for MonthlyIncome vs. Attrition
        fig_monthly_income_scatter = px.scatter(
            df_monthly_income,
            x='MonthlyIncome',
            color='Attrition',
            title='Monthly Income vs. Attrition (Scatter Plot)',
            labels={'MonthlyIncome': 'Monthly Income'}
        )
        st.plotly_chart(fig_monthly_income_scatter)

    
    if question_tosql=="7. EducationField vs Attrition":
        cursor.execute("SELECT EducationField, Attrition, COUNT(*) as NumberOfEmployees FROM data GROUP BY EducationField, Attrition ORDER BY EducationField, Attrition;")
        result_education_field = cursor.fetchall()
        df_education_field = pd.DataFrame(result_education_field, columns=['EducationField', 'Attrition', 'NumberOfEmployees']).reset_index(drop=True)

        # Display the Sunburst Chart for EducationField vs. Attrition
        fig_education_field_sunburst = px.sunburst(
            df_education_field,
            path=['EducationField', 'Attrition'],
            values='NumberOfEmployees',
            title='Education Field vs. Attrition (Sunburst Chart)'
        )
        st.plotly_chart(fig_education_field_sunburst)


    if question_tosql=="8. PercentSalaryHike and Attrition":
        cursor.execute("SELECT PercentSalaryHike, Attrition, COUNT(*) as NumberOfEmployees FROM data GROUP BY PercentSalaryHike, Attrition ORDER BY PercentSalaryHike, Attrition;")
        result_salary_hike = cursor.fetchall()
        df_salary_hike = pd.DataFrame(result_salary_hike, columns=['PercentSalaryHike', 'Attrition', 'NumberOfEmployees']).reset_index(drop=True)

        # Display the Line Chart for PercentSalaryHike vs. Attrition
        fig_salary_hike_line = px.line(
            df_salary_hike,
            x='PercentSalaryHike',
            y='NumberOfEmployees',
            color='Attrition',
            title='Percent Salary Hike vs. Attrition (Line Chart)',
            labels={'PercentSalaryHike': 'Percent Salary Hike', 'NumberOfEmployees': 'Number of Employees'}
        )
        st.plotly_chart(fig_salary_hike_line)
        
    if question_tosql=="9. TotalSatisfaction vs Attrition":
        cursor.execute("SELECT TotalSatisfaction, Attrition, COUNT(*) as NumberOfEmployees FROM data GROUP BY TotalSatisfaction, Attrition ORDER BY TotalSatisfaction, Attrition;")
        result_satisfaction = cursor.fetchall()
        df_satisfaction = pd.DataFrame(result_satisfaction, columns=['TotalSatisfaction', 'Attrition', 'NumberOfEmployees']).reset_index(drop=True)

        # Display the Stacked Bar Chart for TotalSatisfaction vs. Attrition
        fig_satisfaction_bar = px.bar(
            df_satisfaction,
            x='TotalSatisfaction',
            y='NumberOfEmployees',
            color='Attrition',
            title='Total Satisfaction vs. Attrition',
            labels={'NumberOfEmployees': 'Number of Employees', 'TotalSatisfaction': 'Total Satisfaction'},
            barmode='stack'
        )
        st.plotly_chart(fig_satisfaction_bar)
        
    if question_tosql=="10.Observations":
        observations = [
        "With gender, males have a higher attrition rate of 68%.",
        "In job roles, Research Directors and Research Scientists have a high attrition rate.",
        "In job level, Level 2 has the highest attrition rate.",
        "Singles have a higher attrition count compared to married and divorced individuals.",
        "Those who travel rarely on business trips have a higher attrition rate.",
        "The age group from 25 to 35 has a high attrition rate.",
        "Individuals with low income have a higher attrition rate.",
        "Those from life science and medical fields are more likely to leave the job."
    ]

    # Display observations in Streamlit
        for observation in observations:
            st.write(f"- {observation}")
        st.header('Factors Influencing Attrition Rate:')
        st.write("To decrease the attrition rate, the following factors play a key role:")
        st.write("- Monthly Income")
        st.write("- Percent Salary Hike")
        st.write("- Total Satisfaction")







                





                
        


                    
            
                
                    
                

                    
                    
            


                