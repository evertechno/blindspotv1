import streamlit as st
import google.generativeai as genai
import io
import PyPDF2  # For PDF processing
import docx  # For DOCX processing

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(file):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return None

def analyze_insurance_document(document_text):
    """Analyzes the insurance document for hidden/risky clauses and generates FAQs."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Prompt for finding hidden/risky clauses
        hidden_clauses_prompt = f"""
        Analyze the following insurance document text and identify any hidden or potentially risky clauses:
        {document_text}

        Provide a summary of these clauses and explain why they might be risky.
        """
        hidden_clauses_response = model.generate_content(hidden_clauses_prompt)

        # Prompt for generating FAQs
        faq_prompt = f"""
        Based on the following insurance document text, generate a list of frequently asked questions (FAQs) and their answers:
        {document_text}
        """
        faq_response = model.generate_content(faq_prompt)

        return hidden_clauses_response.text, faq_response.text

    except Exception as e:
        st.error(f"Error during analysis: {e}")
        return None, None

# Streamlit App UI
st.title("Insurance Document Analyzer")
st.write("Upload your insurance document (PDF or DOCX) to analyze it.")

uploaded_file = st.file_uploader("Upload Insurance Document", type=["pdf", "docx"])

if uploaded_file is not None:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        document_text = None

    if document_text:
        if st.button("Analyze Document"):
            hidden_clauses, faqs = analyze_insurance_document(document_text)

            if hidden_clauses and faqs:
                st.subheader("Hidden/Risky Clauses Analysis:")
                st.write(hidden_clauses)

                st.subheader("Frequently Asked Questions (FAQs):")
                st.write(faqs)
            else:
                st.warning("Analysis failed. Please check your document and try again.")
