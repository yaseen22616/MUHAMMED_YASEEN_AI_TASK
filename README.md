# AI-Powered Resume Analyzer

This repository contains an AI-powered resume analysis system that leverages Google’s Gemini AI for extracting key information from resumes in PDF format. It offers two versions of the code that provide different functionalities for processing resumes.

## Project Features:
- **Resume Analysis**: Automatically extracts details like name, contact information, university, CGPA, skills, career role suggestions, and more.
- **Cover Letter Generation**: Automatically creates personalized cover letters based on the extracted resume data.
- **Excel Export**: Export the analyzed data in an Excel file for easy storage and review.
- **Job Market Insights**: Displays job market trends for suggested career roles and skills.
- **Skills Visualization**: Visualizes key skills distribution using bar charts.

## Code Versions

### 1. **`ap.py` (Structured Output with Column Formatting)**

This version is designed for **structured data extraction** and ensures that the extracted details from resumes are presented in a consistent column format in an Excel sheet.

#### **Key Features:**
- **Structured Output**: Extracts detailed resume information (Name, Contact Details, University, CGPA, Key Skills, etc.) and formats it into columns.
- **Excel Export**: Generates an Excel file with all the extracted data neatly organized in a table with proper column width adjustments.
- **Skills Visualization**: Plots a bar chart showing the distribution of key skills mentioned across all resumes.

### 2. **`co.py` (Accurate Details Extraction with Cover Letters)**

This version is focused on **accurate data extraction** and **cover letter generation**. It retrieves more precise details from the resumes and provides the option to generate personalized cover letters for each resume.

#### **Key Features:**
- **Accurate Data Extraction**: Extracts more detailed and precise information from resumes, including career role predictions, industry fit, and AI experience scores.
- **Cover Letter Generation**: Automatically generates a personalized cover letter based on the parsed resume data.
- **Excel Export with Cover Letters**: In addition to the resume data, the generated cover letters are included in the Excel file.
- **Chatbot**: Includes a basic chatbot feature to interact with the resume data and receive career advice.



