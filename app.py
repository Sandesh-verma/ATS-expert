from dotenv import load_dotenv

load_dotenv()

import io
import base64
import streamlit as st
import os 
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    reponse=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="ATS EXPERT")
st.header("ATS TRACKING SYSTEM")
input_text=st.text_area("job Description ",key="input")
uploaded_file=st.file_uploader("upload resume",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded successfully")

submit1= st.button("info about resume")

submit2= st.button("percentage match")


input_prompt1 ="""
you are an experienced hr with tech experience in the filed of data science ,full stack web developmnt , big data , devops ,
your task is to review the provided resume against the job description for these profiles.please share your professional experience
on whether the candidate's profile aligns with Highlight the strengths and weaknesses of the applicant in relation to the specifies job role.

"""
input_prompt2="""
you are an skilled ATS scanner with a deep understanding of data science ,full stack web developmnt , big data , devops ,
your task is to evaluate the resume against the provided job description , give me the percentage of match if resume matches the job 
description . First the output should come as percentage and then keywords missing and last final thoughts.

"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("file not uploaded ")

if submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("file not uploaded ")


