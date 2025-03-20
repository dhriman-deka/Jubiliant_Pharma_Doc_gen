"""
Mock implementation of Gemini API for testing purposes.
"""
import json
import os
import sys
from unittest.mock import MagicMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create mock objects
mock_generate_content = MagicMock()
mock_generate_content.text = json.dumps({
    "names": ["Acme Software Inc.", "XYZ Corporation", "John Doe", "Jane Smith"],
    "dates": ["June 1, 2023", "July 1, 2023", "December 31, 2023"],
    "addresses": ["123 Tech Lane, Silicon Valley, CA 94088", "456 Business Park, New York, NY 10001"],
    "contact_information": {
        "phone": "(555) 123-4567",
        "email": "contracts@acmesoftware.com"
    },
    "financial_information": {
        "total_cost": "$75,000",
        "payment_schedule": [
            {"percentage": "30%", "amount": "$22,500", "description": "upon contract signing"},
            {"percentage": "30%", "amount": "$22,500", "description": "at midpoint milestone completion"},
            {"percentage": "40%", "amount": "$30,000", "description": "upon project completion and acceptance"}
        ],
        "payment_terms": "Net 30 days from invoice date"
    },
    "key_topics": ["software development", "inventory management", "barcode scanning", "ERP integration"],
    "important_statements": [
        "The parties agree to the terms and conditions attached to this agreement."
    ]
})

mock_model = MagicMock()
mock_model.generate_content = MagicMock(return_value=mock_generate_content)

mock_generative_model = MagicMock(return_value=mock_model)

mock_genai = MagicMock()
mock_genai.GenerativeModel = mock_generative_model
mock_genai.configure = MagicMock()

# Mock the analyze_template function
def mock_analyze_template(template_text):
    """
    Mock the analyze_template function to return field names.
    """
    fields = []
    parts = template_text.split('[')
    for part in parts:
        if ']' in part:
            field = part.split(']')[0]
            fields.append(field)
    return list(set(fields))

# Create a patch function to apply mocks
def apply_mocks():
    """
    Apply mock implementations to the app modules.
    """
    import app.utils.gemini_api as gemini_api
    
    # Save the original objects
    original_genai = gemini_api.genai
    original_extract_content = gemini_api.extract_document_content
    original_analyze_template = gemini_api.analyze_template
    
    # Replace with mocks
    gemini_api.genai = mock_genai
    gemini_api.extract_document_content = lambda text: mock_generate_content.text
    gemini_api.analyze_template = mock_analyze_template
    gemini_api.initialize_gemini = lambda: None  # Do nothing
    
    return {
        'original_genai': original_genai,
        'original_extract_content': original_extract_content,
        'original_analyze_template': original_analyze_template
    }

# Create a function to restore original implementations
def restore_mocks(originals):
    """
    Restore original implementations.
    """
    import app.utils.gemini_api as gemini_api
    
    gemini_api.genai = originals['original_genai']
    gemini_api.extract_document_content = originals['original_extract_content']
    gemini_api.analyze_template = originals['original_analyze_template'] 