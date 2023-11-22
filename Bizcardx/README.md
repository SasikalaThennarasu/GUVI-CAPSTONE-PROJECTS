Business-Card-Extraction
Business Cards Data Extraction Hello guys this is the app i created to extract data from visiting and business cards.This app can also be used to extract data from any image files. Enjoy the app and HAPPY CODING😉

bz_front_page

This is the frontend view of Database side

You can find the data i used in the creative modern business card folder Lets see the codes step by step

To extract datas from image i used EASYOCR in this project.To use easyocr you need to install pytorch also.(please see the requirements.txt file) Please install requirements.txt.

step:1 I created a function.py file to create all required function in that file. And imported all required packages import

step:2 I created a function to extract datas from image and to separate all the extracted data using regular expression.(for detailed code see funtion.py file) upload database

step:3 To view extracted data in image format i used opencv package to view the Image view of data in app extract image data

After creating all the functions i created the streamlit app using the function and its very simple app only.(you can see the app code in app.py file)

I think this project will be useful to you foster your knowledge in Image data extraction using easyocr AND Happy coding😁
