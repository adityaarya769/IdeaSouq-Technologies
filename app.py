import streamlit as st
import pdfplumber
from difflib import SequenceMatcher
import pandas as pd
import tempfile
import os

def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def compare_texts(text1, text2):
    """Compare two texts and return differences."""
    matcher = SequenceMatcher(None, text1, text2)
    differences = {
        'additions': 0,
        'deletions': 0,
        'modifications': 0
    }
    
    html_diff = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            html_diff.append(text1[i1:i2])
        elif tag == 'delete':
            html_diff.append(f'<span style="background-color: #ffcdd2">{text1[i1:i2]}</span>')
            differences['deletions'] += 1
        elif tag == 'insert':
            html_diff.append(f'<span style="background-color: #c8e6c9">{text2[j1:j2]}</span>')
            differences['additions'] += 1
        elif tag == 'replace':
            html_diff.append(f'<span style="background-color: #fff9c4">{text2[j1:j2]}</span>')
            differences['modifications'] += 1
    
    return ''.join(html_diff), differences

def main():
    st.set_page_config(
        page_title="PDF Diff Viewer",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("PDF Difference Analyzer")
    st.write("Upload two PDF documents to compare their contents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pdf1 = st.file_uploader("Upload first PDF", type="pdf", key="pdf1")
    
    with col2:
        pdf2 = st.file_uploader("Upload second PDF", type="pdf", key="pdf2")
    
    if pdf1 and pdf2:
        with st.spinner("Processing PDFs..."):
            # Create temporary files for PDFs
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp1, \
                 tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp2:
                tmp1.write(pdf1.getvalue())
                tmp2.write(pdf2.getvalue())
                tmp1_path, tmp2_path = tmp1.name, tmp2.name
            
            try:
                # Extract text from PDFs
                text1 = extract_text_from_pdf(tmp1_path)
                text2 = extract_text_from_pdf(tmp2_path)
                
                # Compare texts
                diff_html, differences = compare_texts(text1, text2)
                
                # Display summary
                st.subheader("Summary of Changes")
                summary_df = pd.DataFrame({
                    'Type': ['Additions', 'Deletions', 'Modifications'],
                    'Count': [differences['additions'], differences['deletions'], differences['modifications']]
                })
                st.dataframe(summary_df, use_container_width=True)
                
                # Display differences
                st.subheader("Detailed Comparison")
                st.markdown(diff_html, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Error processing PDFs: {str(e)}")
            
            finally:
                # Clean up temporary files
                os.unlink(tmp1_path)
                os.unlink(tmp2_path)
    
    st.markdown("""
    ### Color Legend
    - <span style='background-color: #c8e6c9'>Green</span>: Added content
    - <span style='background-color: #ffcdd2'>Red</span>: Removed content
    - <span style='background-color: #fff9c4'>Yellow</span>: Modified content
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
