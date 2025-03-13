import streamlit as st
import google.generativeai as genai
import PyPDF2
import re

# Configure the API key for google.generativeai
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            except Exception as page_e:
                st.warning(f"Warning: Error extracting text from page {page_num + 1}: {page_e}")
        if not text.strip(): #check if the string is empty or contains only whitespace.
            st.error("Error: Extracted text is empty or contains only whitespace.")
            return None
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def extract_relevant_clauses(document_text, max_length=3000):
    try:
        clause_patterns = [
            r'\bterm\b',
            r'\bclause\b',
            r'\bcondition\b',
            r'\brisk\b',
            r'\bexclusion\b',
            r'\bcoverage\b',
            r'\bliability\b',
            r'\bpolicy\b'
        ]

        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', document_text)
        relevant_sentences = [sentence for sentence in sentences if any(re.search(pattern, sentence, re.IGNORECASE) for pattern in clause_patterns)]
        relevant_text = ' '.join(relevant_sentences)

        if len(relevant_text) > max_length:
            relevant_text = relevant_text[:max_length] + "..."

        return relevant_text

    except Exception as e:
        st.error(f"Error extracting relevant clauses: {e}")
        return None

def analyze_insurance_document(relevant_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')

        detailed_analysis_prompt = f"""
        Analyze the following insurance document text with a focus on complex terms, potential risks, and hidden clauses.

        {relevant_text}

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

# Streamlit UI
st.title("Insurance Document Deep Analyzer")
st.write("Upload your insurance document (PDF) for in-depth analysis.")

uploaded_file = st.file_uploader("Upload Insurance Document", type=["pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
        if document_text:
            relevant_text = extract_relevant_clauses(document_text)
            if relevant_text:
                if st.button("Perform Deep Analysis"):
                    with st.spinner("Analyzing document..."):
                        analysis_result = analyze_insurance_document(relevant_text)

                    if analysis_result:
                        st.subheader("Detailed Analysis Results:")
                        st.write(analysis_result)
                    else:
                        st.warning("Analysis failed. Please check your document and try again.")
            else:
                st.warning("No relevant clauses or terms found in the document.")
        else:
            # Error message is already in extract_text_from_pdf
            pass
    else:
        st.error("Unsupported file type. Please upload a PDF file.")
