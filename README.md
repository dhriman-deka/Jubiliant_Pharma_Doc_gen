# Document Generation App - Comprehensive User Guide

## Overview

The Document Generation App is a powerful Streamlit-based application designed to simplify the creation of professional documents from templates. It leverages advanced language model APIs for intelligent document analysis and content generation.

## Table of Contents

1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [API Key Setup](#api-key-setup)
5. [Starting the Application](#starting-the-application)
6. [Using the Application](#using-the-application)
   - [Template Management](#template-management)
   - [Document Upload and Analysis](#document-upload-and-analysis)
   - [Template Filling](#template-filling)
   - [Document Export](#document-export)
   - [AI Assistant](#ai-assistant)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)
9. [Sample Data](#sample-data)
10. [Best Practices](#best-practices)
11. [Advanced Usage](#advanced-usage)
12. [Testing](#testing)
13. [Project Structure](#project-structure)
14. [License](#license)

## Features

- **Template Selection**: Choose from pre-defined document templates
- **Custom Template Upload**: Upload your own templates in text or PDF format
- **Document Analysis**: Extract key information from uploaded documents using AI
- **Intelligent Field Extraction**: Automatically identify template fields
- **Smart Field Filling**: Pre-fill template fields with data from analyzed documents
- **Multiple Export Formats**: Generate documents in PDF or DOCX formats
- **AI Assistant**: Get help and guidance through the integrated chat interface
- **Comprehensive Testing**: Ensure reliability with extensive test coverage

## System Requirements

- Python 3.7 or higher
- 4GB RAM (minimum)
- 100MB of disk space for the application
- Internet connection for API communication

## Installation

### Option 1: Using the Installation Script

The easiest way to set up the Document Generation App is to use the provided installation script:

```bash
chmod +x install.sh
./install.sh
```

This will:
1. Create a virtual environment
2. Install all required dependencies
3. Set up the necessary folder structure
4. Create a `.env` file for your API key

### Option 2: Manual Installation

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Create a `.env` file** in the project root directory with your API key:

```
GEMINI_API_KEY=your_api_key_here
```

## API Key Setup

The application requires an API key to function properly:

1. Visit the language model provider's website to obtain an API key
2. Create a `.env` file in the root directory of the project
3. Add your API key to the `.env` file:

```
API_KEY=your_api_key_here
```

4. Important notes about API usage:
   - Free API tiers often have quota limitations (usage resets daily)
   - If you encounter quota errors, wait for it to reset or obtain a new key
   - The application includes fallback mechanisms for field extraction when quota is exhausted

## Starting the Application

There are two ways to start the application:

### Method 1: Using the run_app.py script (Recommended)

```bash
./run_app.py
```

This method performs environment checks before starting the application, ensuring all dependencies are correctly installed.

### Method 2: Direct Streamlit execution

```bash
streamlit run app.py
```

Once started, the application will be available at:
- Local URL: http://localhost:8501
- Network URL: http://your-ip-address:8501 (for accessing from other devices on the same network)

## Using the Application

The application interface is divided into several sections:

### Template Management

Located in the sidebar, this section allows you to:

#### Selecting a Template:

1. Click on the dropdown menu under "Select Template"
2. Choose from the available templates
3. The template will be loaded for use in the "Fill Template" tab

#### Uploading a Custom Template:

1. Click "Browse files" under "Upload a custom template"
2. Select a text (.txt) or PDF (.pdf) file from your computer
3. Enter a name for your template in the "Template Name" field
4. Click "Save Template" to add it to your template library
5. Your template should now appear in the template selection dropdown

**Template Format Requirements:**
- Templates should use placeholder fields in the format: `[FIELD_NAME]`
- Example: `Dear [RECIPIENT_NAME],`
- Field names should be descriptive and use only letters, numbers, and underscores
- Avoid special characters in field names

### Document Upload and Analysis

This tab allows you to upload and analyze documents:

1. Click "Browse files" under "Upload a document for analysis"
2. Select a PDF (.pdf) or Word (.docx) document
3. After the document appears as successfully uploaded, click "Analyze Document"
4. The system will:
   - Extract text from the document
   - Display the extracted content in the "Document Content" expander
   - Use AI to analyze the content and identify key information
   - Display structured information in the "Document Analysis" section
5. This analyzed data can be used to automatically fill template fields

**Supported Document Types:**
- PDF files (.pdf)
- Microsoft Word documents (.docx)

**Best Practices for Document Analysis:**
- Use clearly formatted documents for best results
- Ensure text is extractable (not scanned images)
- Documents with clear sections and headings work best

### Template Filling

This tab allows you to fill template fields with data:

1. Select a template from the sidebar first
2. The system will:
   - Display the template content in the "Template Content" expander
   - Automatically identify fields in the template
   - Create input fields for each template field
3. If you've analyzed a document, some fields may be pre-filled with extracted data
4. Fill in the remaining fields manually
5. Click "Generate Document" to create your document
6. The filled document will be displayed in the "Filled Document" expander

**Template Field Tips:**
- Field names are case-sensitive
- If a field appears but shouldn't be there, check for formatting issues in your template
- You can edit pre-filled data if the AI extraction wasn't accurate

### Document Export

This tab allows you to export your generated document:

1. After filling a template, navigate to the "Export Document" tab
2. The system will display your document in the "Document to Export" expander
3. Choose an export format (PDF or DOCX)
4. Enter a filename (default is the template name with "_filled" suffix)
5. Click "Export Document" to generate the file
6. After successful export, click "Download PDF" or "Download DOCX" to save the file to your computer

**Export Options:**
- PDF: Creates a standard PDF document, suitable for printing and sharing
- DOCX: Creates a Microsoft Word document, suitable for further editing

**Note:** Exported documents are also saved in the `app/exports` directory on the server.

### AI Assistant

The AI Assistant at the bottom of the page can help you use the application:

1. Type your question or request in the chat input
2. The AI will provide guidance on:
   - How to use specific features
   - Suggestions for document creation
   - Explanations about the application
   - Help with specific templates

**Sample Questions for the AI Assistant:**
- "How do I upload a custom template?"
- "What should I do after analyzing a document?"
- "How can I create a business letter?"
- "What fields are required for the invoice template?"

## Customization

The Document Generation App is designed to be highly customizable. Here's how you can adapt it to your specific needs:

### Change the Language Model API

1. Edit the API configuration file:
   ```
   app/utils/api.py
   ```

2. Update the API initialization function to use your preferred language model:
   - Change the API endpoint
   - Modify the request/response handling
   - Adjust prompt templates for your specific model

3. Update the environment variable name in the `.env` file from `API_KEY` to match your chosen provider

### Add Custom Templates

1. Create new template files in the `app/templates/` directory using the `[FIELD_NAME]` syntax
2. Templates can include conditional logic or specialized formatting based on your needs

### Modify Document Processing

1. Edit the document processing functions in `app/utils/document_processor.py`:
   - Add support for additional document formats
   - Implement specialized extraction for specific document types
   - Customize field extraction logic

### Change UI Layout and Features

1. Modify the Streamlit interface in `app.py`:
   - Add new tabs or sections
   - Customize styling and layout
   - Implement additional visualization components
   - Add your company branding

### Extend AI Assistant Capabilities

1. Edit the chat functionality:
   - Customize prompt templates in `app.py`
   - Add domain-specific knowledge
   - Implement guided workflows for specific document types

### Add New Export Formats

1. Extend the document export functionality in `app/utils/document_processor.py`:
   - Add support for additional export formats (HTML, TXT, etc.)
   - Implement specialized formatting for specific document types

## Troubleshooting

### API Key Issues

**Error: "Failed to initialize AI API"**
- Ensure your `.env` file exists and contains the correct API key
- Check that the API key is valid and not expired
- Try using a different API key

**Error: "Error analyzing template: 429 Resource has been exhausted"**
- The API quota has been reached
- The application will fall back to manual field extraction
- Wait until the quota resets (typically 24 hours) or use a different API key

### Template Issues

**Error: "Failed to read template"**
- Ensure the template file exists and is not corrupted
- Check file permissions
- Try uploading the template again

**No fields detected in template**
- Ensure your template uses the correct field format: `[FIELD_NAME]`
- Check that there are no formatting issues in your template

### Document Upload Issues

**Error: "Error reading PDF/DOCX"**
- Ensure the document is not corrupted
- Check that the document is not password-protected
- Try converting to another format and uploading again

### Export Issues

**Error: "Failed to export document as PDF/DOCX"**
- Check that the filled content is not empty
- Ensure the export directory (`app/exports`) exists and is writable
- Check that required libraries (reportlab for PDF, python-docx for DOCX) are installed

## Sample Data

The application can be used with various business data. Here's an example of company information that could be used for document generation:

### Jubilant Pharmova Business Information

This pharmaceutical company data can be used to test various templates:

**Company Overview:**
- Name: Jubilant Pharmova
- Industry: Pharmaceuticals
- Business Segments: Specialty Pharmaceuticals (45%), CDMO (33.2%), Generics (20.6%), CRDS (7%)

**Financial Data (FY22):**
- Total Revenue: Rs 6,130 Crore
- EBITDA: Rs 1,168 Crore (19.0% margin)
- PAT: Rs 413 Crore
- EPS: Rs 26.0
- Capital Expenditure: Rs 437 Crore

**Segment Details:**
- Radiopharma: #3 in US by revenue, leader in lung/thyroid imaging
- Allergy Immunotherapy: #2 in US SCIT extract market, 100+ products
- CDMO CMO: Sterile injectables (80%), non-sterile (20%)
- API: 90+ APIs across CNS, CVS, anti-infective, anti-diabetic categories

## Best Practices

### Template Creation

1. **Use Descriptive Field Names:** 
   - Good: `[COMPANY_NAME]`, `[INVOICE_NUMBER]`
   - Avoid: `[FIELD1]`, `[X]`

2. **Maintain Consistent Formatting:**
   - Use consistent spacing around field placeholders
   - Keep templates well-structured with clear sections

3. **Test Templates Thoroughly:**
   - Fill with sample data before using in production
   - Check for any missing or incorrectly formatted fields

### Document Analysis

1. **Prepare Documents for Analysis:**
   - Ensure clear formatting and structure
   - Use documents with extractable text (not scanned images)
   - Remove any sensitive information before uploading

2. **Verify Extracted Data:**
   - Always review AI-extracted information for accuracy
   - Correct any misidentified data before generating documents

### General Usage

1. **Save Work Regularly:**
   - Export important documents immediately
   - Don't rely on browser sessions to maintain state

2. **Organize Templates:**
   - Use descriptive names for uploaded templates
   - Consider creating template categories for different document types

## Advanced Usage

### Custom Templates for Different Business Scenarios

1. **Business Correspondence:**
   - Create letterhead templates with your company branding
   - Include placeholders for recipient details, subject, and body content

2. **Financial Documents:**
   - Design invoice templates with line items and calculation fields
   - Create quote templates with product/service descriptions

3. **Legal Documents:**
   - Develop contract templates with standard clauses
   - Include placeholders for specific terms and conditions

### Batch Processing Workflow

For processing multiple documents:

1. Upload and analyze each document individually
2. Save the analyzed data for each document (copy from JSON display)
3. Select the appropriate template for each document
4. Fill templates using the saved analysis data
5. Export documents in batch

## Testing

The application includes comprehensive test coverage:

1. Run all tests to ensure everything is working correctly:

```bash
python3 run_all_tests.py
```

2. Check your environment setup:

```bash
python3 check_environment.py
```

### Test Types

1. **Unit Tests:** Test individual components
2. **Integration Tests:** Test component interactions
3. **UI Tests:** Test Streamlit interface functionality
4. **API Tests:** Test language model API integration

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── run_app.py              # Script to run the app with environment checks
├── run_all_tests.py        # Script to run all tests
├── check_environment.py    # Script to check environment setup
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── tests/                  # Test files
│   ├── test_streamlit_app.py     # Streamlit app tests
│   ├── test_app_functionality.py # Core functionality tests
│   ├── mock_api.py               # Mock implementation of language model API
│   ├── templates/                # Test templates
│   └── documents/                # Test documents
└── app
    ├── exports/            # Generated documents
    ├── templates/          # Document templates
    │   ├── business_letter.txt
    │   └── invoice.txt
    └── utils/              # Utility modules
        ├── document_processor.py  # Document processing utilities
        ├── api.py                 # Language model API integration
        └── template_manager.py    # Template management utilities
```

## License

MIT

---

## Command Quick Reference

| Task | Command |
|------|---------|
| Start application | `./run_app.py` |
| Run all tests | `python3 run_all_tests.py` |
| Check environment | `python3 check_environment.py` |
| Install dependencies | `pip install -r requirements.txt` |

---

Created with ❤️ for efficient document generation 