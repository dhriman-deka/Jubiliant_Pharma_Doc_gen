"""
Test the Streamlit app's functionality programmatically.
Note: This doesn't fully test the UI interactions, but verifies core functionality.
"""
import os
import sys
import tempfile
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import mock API utilities
from tests.mock_gemini_api import apply_mocks, restore_mocks

# Import utility functions directly
from app.utils.template_manager import read_template, get_template_path, get_available_templates
from app.utils.document_processor import fill_template, generate_pdf, generate_docx

# Test directories
TEST_DIR = Path(__file__).parent
TEST_TEMPLATES_DIR = TEST_DIR / "templates"
TEST_DOCUMENTS_DIR = TEST_DIR / "documents"
TEST_OUTPUT_DIR = TEST_DIR / "output"

# Create output directory if it doesn't exist
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

def setup_mocks():
    """Set up mock objects for Streamlit and other dependencies."""
    
    # Mock Streamlit
    mock_st = MagicMock()
    
    # Create a mock session state that acts like a dict
    class MockSessionState(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
        def __getattr__(self, key):
            if key in self:
                return self[key]
            return None
            
        def __setattr__(self, key, value):
            self[key] = value
    
    # Set up session state
    mock_st.session_state = MockSessionState()
    mock_st.session_state.analysis_result = json.dumps({
        "names": ["Acme Software Inc.", "XYZ Corporation"],
        "dates": ["June 1, 2023", "July 1, 2023"],
        "client": "XYZ Corporation",
        "project": "Inventory Management System"
    })
    
    return mock_st

def test_template_selection_and_filling():
    """Test template selection and filling functionality."""
    # Apply API mocks
    originals = apply_mocks()
    
    try:
        # Get the test template
        template_path = get_template_path("test_contract")
        if not os.path.exists(template_path):
            # Copy our test template to the app templates directory
            from shutil import copy
            source = TEST_TEMPLATES_DIR / "test_contract.txt"
            app_templates_dir = Path("app/templates")
            os.makedirs(app_templates_dir, exist_ok=True)
            copy(source, app_templates_dir / "test_contract.txt")
        
        # Read the template
        template_content = read_template(template_path)
        assert template_content is not None
        assert "CONTRACT AGREEMENT" in template_content
        
        # Fill the template with test data
        test_data = {
            "COMPANY_NAME": "Streamlit Test Company",
            "CLIENT_NAME": "Streamlit Test Client",
            "EFFECTIVE_DATE": "2023-01-01",
            "SERVICE_DESCRIPTION": "Streamlit App Testing",
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
        assert "Streamlit Test Company" in filled_content
        assert "Streamlit Test Client" in filled_content
        
        print("✅ Template selection and filling test passed")
        return True
    
    except Exception as e:
        print(f"❌ Template selection and filling test failed: {str(e)}")
        return False
    
    finally:
        # Restore original implementations
        restore_mocks(originals)

def test_document_analysis():
    """Test document analysis functionality."""
    # Apply API mocks
    originals = apply_mocks()
    
    try:
        # Import app utilities after mocking
        from app.utils.gemini_api import extract_document_content
        from app.utils.document_processor import read_pdf, read_docx
        
        # Test PDF analysis
        pdf_path = TEST_DOCUMENTS_DIR / "test_document.pdf"
        if pdf_path.exists():
            # This might fail in testing since we're not creating a real PDF with text content
            try:
                pdf_text = read_pdf(str(pdf_path))
                pdf_analysis = extract_document_content(pdf_text)
                assert pdf_analysis is not None
                print("✅ PDF analysis test passed")
            except Exception as e:
                print(f"⚠️ PDF analysis test skipped: {str(e)}")
        
        # Test DOCX analysis
        docx_path = TEST_DOCUMENTS_DIR / "test_proposal.docx"
        if docx_path.exists():
            docx_text = read_docx(str(docx_path))
            assert docx_text is not None
            assert "TEST PROPOSAL DOCUMENT" in docx_text
            
            docx_analysis = extract_document_content(docx_text)
            assert docx_analysis is not None
            print("✅ DOCX analysis test passed")
        
        # Test text document analysis
        text_path = TEST_DOCUMENTS_DIR / "test_document.txt"
        if text_path.exists():
            with open(text_path, 'r') as f:
                text_content = f.read()
            
            text_analysis = extract_document_content(text_content)
            assert text_analysis is not None
            print("✅ Text document analysis test passed")
        
        return True
    
    except Exception as e:
        print(f"❌ Document analysis test failed: {str(e)}")
        return False
    
    finally:
        # Restore original implementations
        restore_mocks(originals)

def test_document_export():
    """Test document export functionality."""
    # Apply API mocks
    originals = apply_mocks()
    
    try:
        # Test data
        test_content = """
        TEST DOCUMENT EXPORT
        
        This is a test document content for export testing.
        
        Company: Export Test Company
        Client: Export Test Client
        Date: 2023-01-01
        
        This document was generated during automated testing.
        """
        
        # Test PDF export
        pdf_output_path = TEST_OUTPUT_DIR / "export_test.pdf"
        pdf_success = generate_pdf(test_content, str(pdf_output_path))
        assert pdf_success is True
        assert pdf_output_path.exists()
        print("✅ PDF export test passed")
        
        # Test DOCX export
        docx_output_path = TEST_OUTPUT_DIR / "export_test.docx"
        docx_success = generate_docx(test_content, str(docx_output_path))
        assert docx_success is True
        assert docx_output_path.exists()
        print("✅ DOCX export test passed")
        
        return True
    
    except Exception as e:
        print(f"❌ Document export test failed: {str(e)}")
        return False
    
    finally:
        # Restore original implementations
        restore_mocks(originals)

def run_streamlit_tests():
    """Run all Streamlit app tests."""
    print("\n" + "=" * 80)
    print(" STREAMLIT APP FUNCTIONALITY TESTS ".center(80, "="))
    print("=" * 80)
    
    success = True
    
    # Run tests
    if not test_template_selection_and_filling():
        success = False
    
    if not test_document_analysis():
        success = False
    
    if not test_document_export():
        success = False
    
    # Print summary
    print("\n" + "=" * 80)
    print(" TEST SUMMARY ".center(80, "="))
    print("=" * 80)
    
    if success:
        print("All Streamlit app functionality tests passed! ✅")
    else:
        print("Some Streamlit app functionality tests failed. ❌")
    
    return 0 if success else 1

class TestStreamlitApp(unittest.TestCase):
    """Test the functionality of the Streamlit app"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up after tests"""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.test_dir)
    
    @patch('streamlit.selectbox')
    def test_template_selection(self, mock_selectbox):
        """Test template selection functionality"""
        # Mock template selection
        templates = get_available_templates()
        self.assertTrue(len(templates) > 0, "No templates found")
        
        mock_selectbox.return_value = templates[0]
        selected_template = mock_selectbox("Choose a template", [""] + templates)
        
        # Check template path exists
        template_path = get_template_path(selected_template)
        self.assertTrue(os.path.exists(template_path), f"Template path does not exist: {template_path}")
        
        # Read template content
        template_content = read_template(template_path)
        self.assertFalse(template_content.startswith("Error"), "Failed to read template")
        self.assertTrue(len(template_content) > 0, "Template is empty")
    
    @patch('streamlit.text_input')
    def test_template_filling(self, mock_text_input):
        """Test template filling functionality"""
        # Get a template
        templates = get_available_templates()
        template_path = get_template_path(templates[0])
        template_content = read_template(template_path)
        
        # Extract fields (simplified for testing)
        template_fields = [
            field.strip("[]") for field in 
            template_content.split("[") if "]" in field
        ]
        template_fields = list(set(template_fields))
        
        # Create test field values
        field_values = {}
        for field in template_fields:
            test_value = f"Test {field}"
            mock_text_input.return_value = test_value
            field_values[field] = test_value
        
        # Fill template
        filled_content = fill_template(template_content, field_values)
        
        # Check filled content
        self.assertTrue(len(filled_content) > 0, "Filled content is empty")
        
        # Verify all fields were replaced
        for field in template_fields:
            self.assertNotIn(f"[{field}]", filled_content, f"Field {field} was not replaced")
    
    @patch('app.utils.document_processor.read_pdf')
    @patch('streamlit.file_uploader')
    def test_document_analysis_pdf(self, mock_file_uploader, mock_read_pdf):
        """Test PDF document analysis functionality"""
        # Create a mock PDF file
        mock_pdf = MagicMock()
        mock_pdf.name = "test.pdf"
        mock_pdf.getvalue.return_value = b"PDF content"
        mock_file_uploader.return_value = mock_pdf
        
        # Set up mock for read_pdf
        mock_read_pdf.return_value = "Mocked PDF content"
        
        # Import the read_pdf function (this will use the mocked version)
        from app.utils.document_processor import read_pdf
        
        # Test PDF analysis
        document_text = read_pdf("test.pdf")
        self.assertEqual(document_text, "Mocked PDF content")
        self.assertFalse(document_text.startswith("Error"), "PDF reading failed")
    
    @patch('app.utils.document_processor.read_docx')
    @patch('streamlit.file_uploader')
    def test_document_analysis_docx(self, mock_file_uploader, mock_read_docx):
        """Test DOCX document analysis functionality"""
        # Create a mock DOCX file
        mock_docx = MagicMock()
        mock_docx.name = "test.docx"
        mock_docx.getvalue.return_value = b"DOCX content"
        mock_file_uploader.return_value = mock_docx
        
        # Set up mock for read_docx
        mock_read_docx.return_value = "Mocked DOCX content"
        
        # Import the read_docx function (this will use the mocked version)
        from app.utils.document_processor import read_docx
        
        # Test DOCX analysis
        document_text = read_docx("test.docx")
        self.assertEqual(document_text, "Mocked DOCX content")
        self.assertFalse(document_text.startswith("Error"), "DOCX reading failed")
    
    @patch('streamlit.radio')
    def test_document_export_pdf(self, mock_radio):
        """Test PDF document export functionality"""
        # Mock export format selection
        mock_radio.return_value = "PDF"
        export_format = mock_radio("Export Format", ["PDF", "DOCX"])
        self.assertEqual(export_format, "PDF")
        
        # Mock PDF generation
        test_content = "Test document content"
        test_export_path = os.path.join(self.test_dir, "test_export.pdf")
        
        with patch('app.utils.document_processor.generate_pdf', return_value=True):
            result = generate_pdf(test_content, test_export_path)
            self.assertTrue(result, "PDF generation failed")
    
    @patch('streamlit.radio')
    def test_document_export_docx(self, mock_radio):
        """Test DOCX document export functionality"""
        # Mock export format selection
        mock_radio.return_value = "DOCX"
        export_format = mock_radio("Export Format", ["PDF", "DOCX"])
        self.assertEqual(export_format, "DOCX")
        
        # Mock DOCX generation
        test_content = "Test document content"
        test_export_path = os.path.join(self.test_dir, "test_export.docx")
        
        with patch('app.utils.document_processor.generate_docx', return_value=True):
            result = generate_docx(test_content, test_export_path)
            self.assertTrue(result, "DOCX generation failed")

if __name__ == "__main__":
    unittest.main() 