import streamlit as st
import google.generativeai as genai
import PyPDF2

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def analyze_insurance_document(document_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')

        detailed_analysis_prompt = f"""
        Analyze the following insurance document text with a focus on complex terms, potential risks, and hidden clauses.

        {document_text}

        Provide:
        1. An easy-to-understand summary of the document.
        2. A breakdown and explanation of any complex terms or jargon.
        3. Highlight any potentially risky or hidden clauses, explaining why they are risky.
        4. Suggest potential questions to ask the insurance provider for clarification.
        """

        analysis_response = model.generate_content(detailed_analysis_prompt)
        return analysis_response.text

    except Exception as e:
        st.error(f"Error during analysis: {e}")
        return None

st.title("Insurance Document Deep Analyzer")
st.write("Upload your insurance document (PDF) for in-depth analysis.")

uploaded_file = st.file_uploader("Upload Insurance Document", type=["pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF file.")
        document_text = None

    if document_text:
        if st.button("Perform Deep Analysis"):
            with st.spinner("Analyzing document..."):
                analysis_result = analyze_insurance_document(document_text)

            if analysis_result:
                st.subheader("Detailed Analysis Results:")
                st.write(analysis_result)
            else:
                st.warning("Analysis failed. Please check your document and try again.")
