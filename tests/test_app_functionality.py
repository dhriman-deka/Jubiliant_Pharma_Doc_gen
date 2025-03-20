import os
import sys
from pathlib import Path

# Try to import pytest, but make it optional
try:
    import pytest
except ImportError:
    pytest = None

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utility modules
from app.utils.document_processor import (
    fill_template, generate_pdf, generate_docx
)
from app.utils.template_manager import (
    get_available_templates, save_template, 
    save_uploaded_template, get_template_path, read_template
)
from app.utils.gemini_api import (
    initialize_gemini, extract_document_content, analyze_template
)

# Import document processing functions
from app.utils.document_processor import read_pdf, read_docx

# Test directories
TEST_DIR = Path(__file__).parent
TEST_TEMPLATES_DIR = TEST_DIR / "templates"
TEST_DOCUMENTS_DIR = TEST_DIR / "documents"
TEST_OUTPUT_DIR = TEST_DIR / "output"

def test_template_reading():
    """Test that templates can be read correctly."""
    template_path = TEST_TEMPLATES_DIR / "test_contract.txt"
    template_content = read_template(str(template_path))
    
    assert template_content is not None
    assert "CONTRACT AGREEMENT" in template_content
    assert "[COMPANY_NAME]" in template_content
    assert "[CLIENT_NAME]" in template_content
    
    print("✅ Template reading test passed")

def test_template_filling():
    """Test that templates can be filled with data."""
    template_path = TEST_TEMPLATES_DIR / "test_contract.txt"
    template_content = read_template(str(template_path))
    
    test_data = {
        "COMPANY_NAME": "Test Company",
        "CLIENT_NAME": "Test Client",
        "EFFECTIVE_DATE": "2023-01-01",
        "SERVICE_DESCRIPTION": "Software Development",
        "PAYMENT_AMOUNT": "$10,000",
        "PAYMENT_TERMS": "30 days",
        "START_DATE": "2023-01-01",
        "END_DATE": "2023-12-31",
        "NOTICE_PERIOD": "30 days",
        "JURISDICTION": "California",
        "COMPANY_REPRESENTATIVE": "John Doe",
        "CLIENT_REPRESENTATIVE": "Jane Smith",
        "COMPANY_TITLE": "CEO",
        "CLIENT_TITLE": "CTO"
    }
    
    filled_content = fill_template(template_content, test_data)
    
    assert filled_content is not None
    assert "Test Company" in filled_content
    assert "Test Client" in filled_content
    assert "SOFTWARE DEVELOPMENT" not in filled_content  # This should not be in the filled content
    
    print("✅ Template filling test passed")

def test_document_reading():
    """Test that documents can be read correctly."""
    document_path = TEST_DOCUMENTS_DIR / "test_document.txt"
    
    # Read the document as text
    with open(document_path, 'r') as file:
        document_content = file.read()
    
    assert document_content is not None
    assert "SOFTWARE DEVELOPMENT AGREEMENT" in document_content
    assert "Acme Software Inc." in document_content
    
    print("✅ Document reading test passed")

def test_pdf_generation():
    """Test PDF generation."""
    template_path = TEST_TEMPLATES_DIR / "test_contract.txt"
    template_content = read_template(str(template_path))
    
    test_data = {
        "COMPANY_NAME": "PDF Test Company",
        "CLIENT_NAME": "PDF Test Client",
        "EFFECTIVE_DATE": "2023-01-01",
        "SERVICE_DESCRIPTION": "PDF Generation Testing",
        "PAYMENT_AMOUNT": "$10,000",
        "PAYMENT_TERMS": "30 days",
        "START_DATE": "2023-01-01",
        "END_DATE": "2023-12-31",
        "NOTICE_PERIOD": "30 days",
        "JURISDICTION": "California",
        "COMPANY_REPRESENTATIVE": "John Doe",
        "CLIENT_REPRESENTATIVE": "Jane Smith",
        "COMPANY_TITLE": "CEO",
        "CLIENT_TITLE": "CTO"
    }
    
    filled_content = fill_template(template_content, test_data)
    output_path = TEST_OUTPUT_DIR / "test_output.pdf"
    
    success = generate_pdf(filled_content, str(output_path))
    
    assert success is True
    assert output_path.exists()
    
    print("✅ PDF generation test passed")

def test_docx_generation():
    """Test DOCX generation."""
    template_path = TEST_TEMPLATES_DIR / "test_contract.txt"
    template_content = read_template(str(template_path))
    
    test_data = {
        "COMPANY_NAME": "DOCX Test Company",
        "CLIENT_NAME": "DOCX Test Client",
        "EFFECTIVE_DATE": "2023-01-01",
        "SERVICE_DESCRIPTION": "DOCX Generation Testing",
        "PAYMENT_AMOUNT": "$10,000",
        "PAYMENT_TERMS": "30 days",
        "START_DATE": "2023-01-01",
        "END_DATE": "2023-12-31",
        "NOTICE_PERIOD": "30 days",
        "JURISDICTION": "California",
        "COMPANY_REPRESENTATIVE": "John Doe",
        "CLIENT_REPRESENTATIVE": "Jane Smith",
        "COMPANY_TITLE": "CEO",
        "CLIENT_TITLE": "CTO"
    }
    
    filled_content = fill_template(template_content, test_data)
    output_path = TEST_OUTPUT_DIR / "test_output.docx"
    
    success = generate_docx(filled_content, str(output_path))
    
    assert success is True
    assert output_path.exists()
    
    print("✅ DOCX generation test passed")

def test_template_field_extraction():
    """Test template field extraction."""
    template_path = TEST_TEMPLATES_DIR / "test_contract.txt"
    template_content = read_template(str(template_path))
    
    # Simple extraction without Gemini API
    fields = [
        field.strip("[]") for field in 
        template_content.split("[") if "]" in field
    ]
    fields = list(set(fields))
    
    expected_fields = [
        "COMPANY_NAME", "CLIENT_NAME", "EFFECTIVE_DATE", "SERVICE_DESCRIPTION",
        "PAYMENT_AMOUNT", "PAYMENT_TERMS", "START_DATE", "END_DATE",
        "NOTICE_PERIOD", "JURISDICTION", "COMPANY_REPRESENTATIVE",
        "CLIENT_REPRESENTATIVE", "COMPANY_TITLE", "CLIENT_TITLE"
    ]
    
    for field in expected_fields:
        assert field in fields
    
    print("✅ Template field extraction test passed")

def run_tests():
    """Run all tests."""
    print("Running tests...\n")
    
    # Make sure output directory exists
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    test_template_reading()
    test_template_filling()
    test_document_reading()
    test_pdf_generation()
    test_docx_generation()
    test_template_field_extraction()
    
    print("\nAll tests passed! ✅")

if __name__ == "__main__":
    run_tests() 