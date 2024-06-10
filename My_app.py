import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import sqlite3

def image_to_text(path):

  im = Image.open(path)

  #converting image to array

  im_arr = np.array(im)

  reader = easyocr.Reader(['en'])
  text = reader.readtext(im_arr,detail = 0)

  return(text,im)


def extracted_text(texts):

  extrd_dict = {"NAME":[], "DESIGNATION": [], "COMPANY_NAME":[], "CONTACT":[], "EMAIL": [], "WEBSITE": [],
                "ADDRESS":[], "PINCODE":[]}

  extrd_dict["NAME"].append(texts[0])
  extrd_dict["DESIGNATION"].append(texts[1])

  for i in range(2,len(texts)):
    if texts[i].startswith("+") or (texts[i].replace("-","").isdigit() and '-' in texts[i]):
      extrd_dict["CONTACT"].append(texts[i])

    elif "@" in texts[i] and ".com" in texts[i]:
      extrd_dict["EMAIL"].append(texts[i])

    elif "www" in texts[i] or "WWW" in texts[i] or "wWW" in texts[i] or "WwW" in texts[i] or "WWw" in texts[i] or "wwW" in texts[i]:
      small = texts[i].lower()
      extrd_dict["WEBSITE"].append(small)

    elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
      extrd_dict["PINCODE"].append(texts[i])

    elif re.match(r'^[A-Za-z]',texts[i]):
      extrd_dict["COMPANY_NAME"].append(texts[i])

    else:
      remove_colon = re.sub(r'[,;]','',texts[i])
      extrd_dict["ADDRESS"].append(remove_colon)

  for key,value in extrd_dict.items():
    if len(value)>0:
      concatenate = " ".join(value)
      extrd_dict[key] = [concatenate]

    else:
      value = "N/A"
      extrd_dict[key] = [value]

  return extrd_dict



#streamlit part

st.set_page_config(layout = "wide")
st.title ("EXTRACTING BUSINESS CARD DATA WITH OCR")

with st.sidebar:
  select = option_menu("Main Menu",["Home", "Upload and Modify", "Delete"])

if select == "Home":

  st.markdown("### :blue[**Technologies Used :**] Python,easy OCR, Streamlit, SQL, Pandas")
  st.write(
            "### :green[**About :**] Bizcard is a Python application designed to extract information from business cards.")
  st.write(
            '### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')

elif select == "Upload and Modify":
    img = st.file_uploader("Upload the Image",type = ["png","jpg","jpeg"])

    if img is not None:
      st.image(img,width =300)

      text_image, input_img = image_to_text(img)

      text_dict = extracted_text(text_image)

      if text_dict:
        st.success("TEXT IS EXTRACTED SUCCESSFULLY")

      df = pd.DataFrame(text_dict)

#converting images to bytes

      Image_bytes = io.BytesIO()
      input_img.save(Image_bytes,format="PNG")

      image_data = Image_bytes.getvalue()

#creating dictionary

      data = {"IMAGE":[image_data]}

      df1 = pd.DataFrame(data)

      concat_df = pd.concat([df,df1],axis = 1)

      st.dataframe(concat_df)

      button_1 = st.button("Save",use_container_width=True)
      if button_1:
        mydb = sqlite3.connect("Bizcard.db")
        cursor = mydb.cursor()

        #table creation

        create_table_query = '''CREATE TABLE IF NOT EXISTS Bizcard_Details(NAME VARCHAR (225),
                                                                          DESIGNATION VARCHAR (225),
                                                                          COMPANY_NAME VARCHAR (225),
                                                                          CONTACT VARCHAR (225),
                                                                          EMAIL VARCHAR (225),
                                                                          WEBSITE text,
                                                                          ADDRESS text,
                                                                          PINCODE VARCHAR (225),
                                                                          IMAGE text )'''
        cursor.execute(create_table_query)
        mydb.commit()

        # insert query

        insert_query = ''' INSERT INTO Bizcard_Details(NAME,DESIGNATION,COMPANY_NAME,CONTACT,EMAIL,WEBSITE,ADDRESS,
                                                      PINCODE,IMAGE)

                                                      values(?,?,?,?,?,?,?,?,?)'''

        datas = concat_df.values.tolist()[0]
        cursor.execute(insert_query,datas)
        mydb.commit()

        st.success("Saved Successfully")


    method = st.radio("Select the method",["None","Preview","Modify"])
    if method == "None":
      st.write("")

    if method == "Preview":
      mydb = sqlite3.connect("Bizcard.db")
      cursor = mydb.cursor()
      #select query

      select_query = "select * from Bizcard_Details"

      cursor.execute(select_query)
      table = cursor.fetchall()
      mydb.commit()

      table_df = pd.DataFrame(table,columns = ("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL","WEBSITE","ADDRESS",
                                                    "PINCODE","IMAGE"))
      st.dataframe(table_df)

    elif method == "Modify":

      mydb = sqlite3.connect("Bizcard.db")
      cursor = mydb.cursor()
      #select query

      select_query = "select * from Bizcard_Details"

      cursor.execute(select_query)
      table = cursor.fetchall()
      mydb.commit()

      table_df = pd.DataFrame(table,columns = ("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL","WEBSITE","ADDRESS",
                                                    "PINCODE","IMAGE"))
      col1,col2 = st.columns(2)
      with col1:

        selected_name = st.selectbox("Select The Name",table_df["NAME"])

      df_3 = table_df[table_df["NAME"] == selected_name]

      df_4 = df_3.copy()

      st.dataframe(df_4)

      col1,col2 = st.columns(2)

      with col1:

        mo_name = st.text_input("Name",df_3["NAME"].unique()[0])
        mo_desg = st.text_input("designation",df_3["DESIGNATION"].unique()[0])
        mo_comp_name = st.text_input("company_name",df_3["COMPANY_NAME"].unique()[0])
        mo_con = st.text_input("contact",df_3["CONTACT"].unique()[0])
        mo_email = st.text_input("email",df_3["EMAIL"].unique()[0])

        df_4["NAME"] = mo_name
        df_4["DESIGNATION"] = mo_desg
        df_4["COMPANY_NAME"] = mo_comp_name
        df_4["CONTACT"] = mo_con
        df_4["EMAIL"] = mo_email

      with col2:

        mo_web = st.text_input("website",df_3["WEBSITE"].unique()[0])
        mo_add = st.text_input("address",df_3["ADDRESS"].unique()[0])
        mo_pin = st.text_input("pincode",df_3["PINCODE"].unique()[0])
        mo_img = st.text_input("image",df_3["IMAGE"].unique()[0])

        df_4["WEBSITE"] = mo_web
        df_4["ADDRESS"] = mo_add
        df_4["PINCODE"] = mo_pin
        df_4["IMAGE"] = mo_img

      st.dataframe(df_4)

      col1,col2 = st.columns(2)

      with col1:
        button_3 = st.button("Modify",use_container_width= True)

      if button_3:

        mydb = sqlite3.connect("Bizcard.db")
        cursor = mydb.cursor()

        cursor.execute(f"DELETE FROM Bizcard_Details WHERE NAME = '{selected_name}'")
        mydb.commit()

        insert_query = ''' INSERT INTO Bizcard_Details(NAME,DESIGNATION,COMPANY_NAME,CONTACT,EMAIL,WEBSITE,ADDRESS,
                                                      PINCODE,IMAGE)

                                                      values(?,?,?,?,?,?,?,?,?)'''

        datas = df_4.values.tolist()[0]
        cursor.execute(insert_query,datas)
        mydb.commit()

        st.success("Modified Successfully")

elif select == "Delete":
  mydb = sqlite3.connect("Bizcard.db")
  cursor = mydb.cursor()

  col1,col2 = st.columns(2)
  with col1:
    select_query = "select NAME from Bizcard_Details"

    cursor.execute(select_query)
    table1 = cursor.fetchall()
    mydb.commit()

    names = []

    for i in table1:
      names.append(i[0])

    Name_Select = st.selectbox("Select the Name",names)

  with col2:

    select_query = f"select DESIGNATION from Bizcard_Details WHERE NAME ='{Name_Select}' "

    cursor.execute(select_query)
    table2 = cursor.fetchall()
    mydb.commit()

    designations = []

    for j in table2:
      designations.append(j[0])

    Designation_Select = st.selectbox("Select the designation",designations)

  if Name_Select and Designation_Select:
    col1,col2,col3 = st.columns(3)

    with col1:
      st.write(f"Selected Name : {Name_Select}")
      st.write("")
      st.write("")
      st.write("")
      st.write(f"Selected Designation : {Designation_Select}")

    with col2:
      st.write("")
      st.write("")
      st.write("")
      st.write("")

      remove = st.button("Delete",use_container_width=True)
      if remove:

        cursor.execute(f"DELETE FROM Bizcard_Details WHERE NAME ='{Name_Select}' AND DESIGNATION = '{Designation_Select}'")
        mydb.commit()

        st.warning("DELETED")
