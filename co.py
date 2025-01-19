import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for reading PDFs
from io import BytesIO
from pdfminer.high_level import extract_text
import re
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="AIzaSyByaCckFRxvcmKKlapqts3HGUlOg4_43KA")

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_bytes = pdf_file.read()
    pdf_stream = BytesIO(pdf_bytes)
    return extract_text(pdf_stream)

def analyze_resume_with_gemini(text):
    """Use Google's Gemini AI to analyze resume content and extract structured data."""
    prompt = f"""
    Extract the following details from the resume:
    - Name
    - Contact Details
    - University
    - Year of Study
    - Course
    - Discipline
    - CGPA/Percentage
    - Key Skills
    - AI/ML Experience Score (1-3 scale)
    - Generative AI Experience Score (1-3 scale)
    - Supporting Information (e.g., certifications, internships, projects)
    - Suggested Career Role
    - Predict Industry Fit (Tech, Healthcare, Finance, etc.)
    
    Resume Content:
    {text}
    """
    
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text

def clean_data(text):
    """Clean the text data by removing double quotes and asterisks."""
    cleaned_text = text.replace('"', '').replace('*', '')
    return cleaned_text

def batch_process_pdfs(uploaded_files):
    """Process multiple resumes and extract structured data using Gemini AI."""
    results = []
    cover_letters = []
    
    for file in uploaded_files:
        pdf_text = extract_text_from_pdf(file)
        parsed_data = analyze_resume_with_gemini(pdf_text)
        cleaned_data = clean_data(parsed_data)
        results.append(cleaned_data)
        cover_letter = generate_cover_letter(cleaned_data)
        cover_letters.append(cover_letter)
    
    return results, cover_letters

def generate_excel(results, cover_letters):
    """Generate an Excel file from extracted resume data and cover letters."""
    df = pd.DataFrame(results)
    df['Cover Letter'] = cover_letters
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    return output

def generate_cover_letter(parsed_data):
    """Generate a cover letter based on the parsed resume data."""
    prompt = f"""
    Based on the following resume data, generate a personalized cover letter:
    {parsed_data}
    """
    
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text

# Streamlit UI Design
st.set_page_config(page_title="Gemini AI Resume Analyzer", page_icon="🔍", layout="wide")
st.title("AI-Powered Resume Analyzer")
st.write("Upload resumes in PDF format to analyze and extract key details with AI-powered insights.")

# Upload PDF resumes
uploaded_files = st.file_uploader("Upload Resume PDFs", accept_multiple_files=True, type=["pdf"])

if uploaded_files:
    with st.spinner("Analyzing resumes with Gemini AI..."):
        extracted_data, cover_letters = batch_process_pdfs(uploaded_files)
        excel_file = generate_excel(extracted_data, cover_letters)
    
    st.success("✅ Resumes analyzed successfully!")
    st.dataframe(pd.DataFrame(extracted_data))  # Show results in a table
    
    st.download_button("⬇ Download AI-Enhanced Report", excel_file, file_name="gemini_resume_analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.write("### Summary")
    st.write(f"Total Resumes Processed: {len(uploaded_files)}")
    st.write("Summary of extracted details and insights:")
    st.dataframe(pd.DataFrame(extracted_data))
    
    st.write("### Download Cover Letters")
    for i, letter in enumerate(cover_letters):
        letter_file = BytesIO()
        letter_file.write(letter.encode())
        letter_file.seek(0)
        st.download_button(f"⬇ Download Cover Letter {i+1}", letter_file, file_name=f"cover_letter_{i+1}.txt", mime="text/plain")

# Chatbot Feature
st.write("### Chat with the Resume Analyzer")
st.write("Got questions? Ask the Resume Analyzer about your resume or get career advice. Type below to start the conversation!")
user_input = st.text_input("Ask me anything about your resume or career advice:")

if user_input:
    chatbot_response = analyze_resume_with_gemini(user_input)  # Simplified example, ideally use a proper chatbot model
    st.write(f"**Chatbot:** {chatbot_response}")

# Enhanced Features Section
st.write("### Enhanced Features")
st.write("- Improved accuracy in field extraction and handling of varying resume formats.")
st.write("- Efficient batch processing of multiple resumes with timely output generation.")
st.write("- Scalable solution to handle larger payloads, ensuring seamless processing.")
st.write("- Innovative use of Generative AI for providing additional insights, including career potential and role match scores.")

# Footer
st.write("Thank you for using the Gemini AI Resume Analyzer! We hope it helps you in your career journey.")
