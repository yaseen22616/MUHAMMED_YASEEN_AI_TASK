import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for reading PDFs
from io import BytesIO
from pdfminer.high_level import extract_text
import re
import google.generativeai as genai
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

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
    - Suggested Career Role
    - Supporting Information (e.g., certifications, internships, projects)
    - Predict Industry Fit (Tech, Healthcare, Finance, etc.)
    
    Resume Content:
    {text}
    """
    
    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
        response_text = response.text  # Get the response text
        
        # Debug: Print the response text to understand its structure
        print("Gemini API Response:", response_text)
        
        # Manually parse the response text to extract details
        parsed_data = {}
        expected_fields = [
            "Name", "Contact Details", "University", "Year of Study", "Course",
            "Discipline", "CGPA/Percentage", "Key Skills", "AI/ML Experience Score",
            "Generative AI Experience Score", "Suggested Career Role",
            "Supporting Information (e.g., certifications, internships, projects)", "Predict Industry Fit"
        ]
        
        # Extract the details from response text and clean data
        for field in expected_fields:
            match = re.search(f"{field}:(.*?)(\n|$)", response_text)
            if match:
                value = match.group(1).strip()
                # Remove unwanted characters like asterisks
                value = re.sub(r'[^\w\s,.\-()]', '', value)  # Keep only valid characters
                parsed_data[field] = value
            else:
                parsed_data[field] = "Not Available"
        
        # Debug: Print the parsed data to understand what's being extracted
        print("Parsed Data:", parsed_data)
        
        return parsed_data
    
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return {field: "Error" for field in expected_fields}

def batch_process_pdfs(uploaded_files):
    """Process multiple resumes and extract structured data using Gemini AI."""
    results = []
    progress = 0
    total_files = len(uploaded_files)
    
    for file in uploaded_files:
        progress += 1
        st.progress(progress / total_files)
        pdf_text = extract_text_from_pdf(file)
        parsed_data = analyze_resume_with_gemini(pdf_text)
        results.append(parsed_data)
    
    return results

def generate_excel(results):
    """Generate an Excel file from extracted resume data with proper formatting."""

    # Define expected columns
    expected_columns = [
        "Name", "Contact Details", "University", "Year of Study", "Course",
        "Discipline", "CGPA/Percentage", "Key Skills", "AI/ML Experience Score",
        "Generative AI Experience Score", "Suggested Career Role",
        "Supporting Information (e.g., certifications, internships, projects)", "Predict Industry Fit"
    ]

    # Ensure all expected columns are in the results list of dictionaries
    for result in results:
        for column in expected_columns:
            if column not in result:
                result[column] = "Not Available"

    df = pd.DataFrame(results)

    # Reindex the DataFrame to ensure proper column order
    df = df.reindex(columns=expected_columns)


    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Resume Analysis")
        workbook = writer.book
        worksheet = writer.sheets["Resume Analysis"]
        # Auto-adjust column width
        for col in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in col) + 2
            worksheet.column_dimensions[col[0].column_letter].width = max_length

    output.seek(0)
    return output

def plot_skills_distribution(skills):
    """Plot a bar chart of key skills."""
    skills_counts = pd.Series(skills.split(',')).value_counts()
    plt.figure(figsize=(10, 5))
    skills_counts.plot(kind='bar', color='skyblue')
    plt.title('Key Skills Distribution')
    plt.xlabel('Skills')
    plt.ylabel('Frequency')
    plt.show()

def show_job_market_trends(role):
    """Show job market trends for the suggested career role."""
    # Placeholder implementation for job market trends
    # Replace this with actual job market trend analysis using APIs or data sources
    st.write(f"**Job Market Trends for {role}:**")
    st.write("Demand for this role has been steadily increasing over the past year. Key skills in demand are Python, Machine Learning, and Data Analysis.")

def generate_cover_letter(name, role):
    """Generate a personalized cover letter."""
    cover_letter = f"""
    Dear Hiring Manager,

    I am writing to express my interest in the {role} position at your esteemed organization. My name is {name}, and I am confident that my skills and experiences make me a strong candidate for this role.

    Throughout my academic and professional journey, I have developed a solid foundation in key areas relevant to this position, including Python, Machine Learning, and Data Analysis. I am excited about the opportunity to contribute to your team and grow as a professional in the field.

    Thank you for considering my application. I look forward to the possibility of discussing my candidacy further.

    Sincerely,
    {name}
    """
    return cover_letter

# Streamlit UI Design
st.set_page_config(page_title="Gemini AI Resume Analyzer", page_icon="🔍", layout="wide")
st.title("AI-Powered Resume Analyzer")
st.write("Upload resumes in PDF format to analyze and extract key details with AI-powered insights.")

# Upload PDF resumes
uploaded_files = st.file_uploader("Upload Resume PDFs", accept_multiple_files=True, type=["pdf"])

if uploaded_files:
    with st.spinner("Analyzing resumes with Gemini AI..."):
        extracted_data = batch_process_pdfs(uploaded_files)
        excel_file = generate_excel(extracted_data)
    
    st.success("✅ Resumes analyzed successfully!")
    st.dataframe(pd.DataFrame(extracted_data))  # Show results in a table
    
    st.download_button("⬇️ Download AI-Enhanced Report", excel_file, file_name="gemini_resume_analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Additional features
    for data in extracted_data:
        st.write(f"### Resume Analysis for {data['Name']}")
        plot_skills_distribution(data["Key Skills"])
        show_job_market_trends(data["Suggested Career Role"])
        cover_letter = generate_cover_letter(data["Name"], data["Suggested Career Role"])
        st.download_button("⬇️ Download Cover Letter", data=cover_letter, file_name=f"{data['Name']}_Cover_Letter.txt")

    st.write("## Summary Insights")
    total_resumes = len(extracted_data)
    st.write(f"**Total Resumes Processed:** {total_resumes}")
    unique_roles = set([data["Suggested Career Role"] for data in extracted_data])
    st.write(f"**Unique Suggested Career Roles:** {', '.join(unique_roles)}")
