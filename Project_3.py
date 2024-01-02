#!/usr/bin/env python
# coding: utf-8

# In[3]:


import easyocr
import re
import pandas as pd
import pymysql
import streamlit as st
from PIL import Image
st.header(":green[BizCardX: Extracting Business Card Details With OCR]")
from streamlit_option_menu import option_menu
read = easyocr.Reader(['en'])
SELECT=option_menu(
    menu_title=None,
    options=["Home","Upload card","Delete & Modify"],
    icons=["house","upload","eraser"],
    default_index=2,
    orientation="horizontal",
    styles={"container":{"padding":"0!important","background-color":"white","size":"cover","width":"100%"},
            "icon":{"color":"black","font-size":"20px"},
            "nav-link":{"font-size":"20px","test-align":"center","margin":"-2px","--hover-color":"#6F36AD"},
            "nav-link-selected":{"background-color":"#6F36ADj"}})
if SELECT=="Home":
    image = Image.open(r"C:\Users\babyk\OneDrive\Documents\projects\project 3\business-card.jpg")
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.header(":green[Technolgies Used:-]")
    st.sidebar.write("* Python")
    st.sidebar.write("* Pandas")
    st.sidebar.write("* mysql")
    st.sidebar.write("* Streamlit")
    st.sidebar.write("* easyocr")
    st.sidebar.divider()
    st.header(":green[About:]")
    st.markdown('''##### - Bizcard is a Python application designed to extract information from business cards -''')
    st.markdown('''##### Our project incorporates a Business Card module designed to manage and display contact information efficiently. Leveraging Python's object-oriented capabilities, we've developed a BusinessCard class that encapsulates essential details like the individual's name, job title, company, email, and phone number. This class enables easy creation and customization of business cards for various users within our system. ''')


# Path to your image file
def image_path(p):
    result = read.readtext(p)
    a = []
    for i in result:
        a.append(i[1])
    return a
# In[24]:

#a = image_path(r"C:\Users\babyk\OneDrive\Documents\projects\project 3\2.png")

def data_extraction(data):
    details = {'company_name': [], 'cardholder_name': [], 'designation': [], 'mob_no': [], 'email': [], 'website': [],
               'area': [], 'city': [], 'state': [], 'pincode': []}
    data1 = []
    value = []
    for index, i in enumerate(data):
        # To get cardholder name
        if index == 0:
            details['cardholder_name'].append(i)
            data1.append(i)
        # To get website
        if i.lower() == 'www' or i.lower() == 'www ':
            k = data.index(i)
            details['website'].append(i + '.' + data[k + 1])
            data.pop(k + 1)
            data1.append(i)
        elif 'www' in i.lower() or 'www ' in i.lower() or 'www.' in i.lower() and '.com' in i:
            details['website'].append(i)
            data1.append(i)
        # To get email
        if '@' in i:
            details['email'].append(i)
            data1.append(i)

        # To get designation
        if index == 1:
            details['designation'].append(i)
            data1.append(i)

        # To get mobile no.
        if '-' in i:
            details['mob_no'].append(i)
            data1.append(i)
    for i in data:
        if i not in data1:
            value.append(i)
    value2 = []
    data2 = []
    for i in value:
        if re.search("^6.*", i):
            details['pincode'].append(i)
            data2.append(i)
        if re.search("^[A-Z,a-z].*6.*$", i):
            lit = i.split(" ")
            details['state'].append(lit[0])
            details['pincode'].append(lit[1])
            data2.append(i)
    for i in value:
        if i not in data2:
            value2.append(i)
    for index, i in enumerate(value2):
        if index == len(value2) - 1:
            if i.lower() not in "st ,":
                if len(i.split()) == 1:
                    details['company_name'].append(value2[index - 1] + " " + i)
                else:
                    details['company_name'].append(i)
                m = value2[0]
                m = m.replace(";", ",")
                k = m.split(",")
                k = [i for i in k if i.strip()]
                if len(k) == 1:
                    details['area'].append(k)
                    o = value2.index(m)
                    details['city'].append(value2[o + 1])
                elif len(k) == 2:
                    details['area'].append(k[0])
                    details['city'].append(k[1])
                else:
                    details['area'].append(k[0])
                    details['city'].append(k[1])
                    details['state'].append(k[2])
        if index == len(value2) - 1:
            if i.lower() in "st ,":
                rv = value2.pop(index)
                value2[0] += " "
                value2[0] += rv
                m = value2[len(value2) - 1]
                k = value2.index(m)
                details['company_name'].append(value2[k - 1] + " " + m)
                details['area'].append(value2[0])
                details['city'].append(value2[1])
    return details['company_name'][0], details['cardholder_name'][0], details['designation'][0], details['mob_no'][0], \
    details['email'][0], details['website'][0], details['area'][0], details['city'][0], details['state'][0], \
    details['pincode'][0]

def sql(de):
    import pandas as pd
    import pymysql
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby")
    cur = myconnection.cursor()
    cur.execute("create database if not exists pro3")
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby", database="pro3")
    cur = myconnection.cursor()
    # creating a table:
    cur.execute('''create table if not exists card_details(company_name varchar(100) primary key,cardholder_name text,designation text,mob_no text,
    email text,website text,area text,city text,state text,pincode text)''')
    sql = '''insert ignore into card_details(company_name ,cardholder_name ,designation,mob_no ,email ,website ,area ,city ,state ,pincode)values(%s,%s,%s
    ,%s,%s,%s,%s,%s,%s,%s)'''
    cur.execute(sql, de)
    myconnection.commit()
    return "uploaded in database successfully"

def show_table():
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby")
    cur = myconnection.cursor()
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby", database="pro3")
    cur = myconnection.cursor()
    query = '''select * from card_details'''
    cur.execute(query)
    myconnection.commit()
    d1 = cur.fetchall()
    df = pd.DataFrame(d1,
                      columns=["company_name", "cardholder_name", "designation", "mob_no", "email", "website", "area",
                               "city", "state", "pincode"])
    return df


#de = data_extraction(a)
if SELECT=="Upload card":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Get the file path (temporary path where the uploaded file is stored)
        file_path = uploaded_file.name
        st.sidebar.image(image, caption='Uploaded Image.', use_column_width=True)
        if st.button("Extract Data and Upload"):
            a=image_path(file_path)
            de=data_extraction(a)
            st.markdown("### Data extracted")
            sql(de)
            st.markdown("### Data uploaded to SQL")
    if st.button("Card List"):
        df=show_table()
        st.write(df)



# to show list of cards to be deleted
def list_of_co():
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby")
    cur = myconnection.cursor()
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby", database="pro3")
    cur = myconnection.cursor()
    query = "Select company_name from card_details"
    cur.execute(query)
    d1 = cur.fetchall()
    df = pd.DataFrame(d1, columns=["company_name"])
    return df




def delete(a):
    # Connect to the database
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby", database="pro3")
    cur = myconnection.cursor()

    # Parameterized query for safety and correctness
    query = "DELETE FROM card_details WHERE company_name = %s;"
    cur.execute(query, (a,))

    # Commit the changes
    myconnection.commit()
    return "card is deleted"


def cln_to_be_altered():
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby")
    cur = myconnection.cursor()
    myconnection = pymysql.connect(host="127.0.0.1", user="root", passwd="11721200#Baby", database="pro3")
    cur = myconnection.cursor()
    cur.execute("SELECT * FROM card_details LIMIT 1;")

    # Fetch data into DataFrame
    df = pd.DataFrame(cur.fetchall(), columns=[description[0] for description in cur.description])

    # Get column names as a list
    column_names = df.columns.tolist()

    return column_names

#to make some alteration:
def alter(a,b,c):
    myconnection=pymysql.connect(host="127.0.0.1",user="root",passwd="11721200#Baby")
    cur=myconnection.cursor()
    myconnection=pymysql.connect(host="127.0.0.1",user="root",passwd="11721200#Baby",database="pro3")
    cur=myconnection.cursor()
    query="set sql_safe_updates=0"
    cur.execute(query)
    myconnection.commit()

    # Ensuring the query is safe and correctly formatted
    query = f"UPDATE card_details SET {a} = %s WHERE company_name = %s;"
    cur.execute(query, (b, c))

    myconnection.commit()
    return "Altered Successfully"

# Your existing condition
if SELECT == "Delete & Modify":
    SELECTIN = option_menu(
        menu_title=None,
        options=["Delete", "Modify"],
        icons=["trash","pencil"],
        default_index=0,
        orientation="horizontal",
        key="Delete_Modify_Menu",  # Unique key for this particular option menu
        styles={
            "container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100%"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}
        })
    if SELECTIN == "Delete":
        df=list_of_co()
        # Dropdown for selecting a company
        selected_company = st.selectbox("Select a company to delete:", df['company_name'])
        if st.button("Delete the Card"):
            h=delete(selected_company)
            st.header(h)
    if SELECTIN == "Modify":
        df = list_of_co()
        # Dropdown for selecting a company
        selected_company = st.sidebar.selectbox("Select a company to alter:", df['company_name'])
        d=cln_to_be_altered()
        detail=st.selectbox("Select the detail to be altered:",d)
        user_input = st.text_input("Enter your text here", )
        if st.button("Alter the Card"):
            alt=alter(detail,user_input,selected_company)
            st.header(alt)

# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:

