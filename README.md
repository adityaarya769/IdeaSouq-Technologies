# PDF Difference Analyzer

A Streamlit web application that allows users to compare two PDF documents and visualize their differences with color-coded highlighting.

## Features

- Upload and compare two PDF documents
- Color-coded visualization of differences:
  - Green: Added content
  - Red: Removed content
  - Yellow: Modified content
- Summary report showing number of additions, deletions, and modifications

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL
3. Upload two PDF documents using the file upload buttons
4. View the differences and summary report

## Technical Details

- Built with Streamlit for the frontend
- Uses pdfplumber for PDF text extraction
- Implements difflib for text comparison
- Handles various PDF formats and edge cases

## Requirements

See `requirements.txt` for a complete list of dependencies.

Deployed version: https://ideasouq-technologies-tpzxsubbppwplhz8ik8isy.streamlit.app/
