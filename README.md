The pre requisites required to run this code is to have the below modules installed in your machine.
streamlit,streamlit_option_menu,easyocr,PIL,Image,pandas,numpy,re,io,sqlite3. 
The code contains functional blocks of converting image to text using easyocr
And assigning the converted texts to its respective department.
Created a SQL database using sqlite3, where we can store our scanned data
The UI is built using streamlit.
The user has to upload the image file, as a result text data would be received
We have an option to modify the data if the values are mapped wrongly by simply editing the extracted values from the image
We too have a delete option to delete unwanted entries from the database
