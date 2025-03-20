"""
Mock implementation of language model API for testing purposes.
"""

class MockGenerativeModel:
    """Mock implementation of the GenerativeModel class."""
    
    def __init__(self, model_name):
        self.model_name = model_name
    
    def generate_content(self, prompt):
        """Mock implementation that returns a predefined response."""
        return MockGenerationResponse("This is a mock response for testing.")

class MockGenerationResponse:
    """Mock implementation of the generation response."""
    
    def __init__(self, text):
        self.text = text

# Mock implementation of the genai module
class MockGenAI:
    """Mock implementation of the genai module."""
    
    def __init__(self):
        self.models = []
        self.api_key = "mock_api_key"
    
    def configure(self, api_key=None):
        """Mock implementation of configure."""
        self.api_key = api_key
    
    def list_models(self):
        """Mock implementation that returns a list of models."""
        return [
            MockModel("models/text-model-001"),
            MockModel("models/text-model-002"),
            MockModel("models/ai-model-001"),
            MockModel("models/ai-model-002")
        ]
    
    def GenerativeModel(self, model_name):
        """Mock implementation that returns a GenerativeModel instance."""
        return MockGenerativeModel(model_name)

class MockModel:
    """Mock implementation of a model object."""
    
    def __init__(self, name):
        self.name = name

# Create a mock instance of genai
mock_genai = MockGenAI()

# Mock functions for the document processor
def mock_generate_content(prompt):
    """Mock implementation for generate_content."""
    return MockGenerationResponse("This is mock extracted content for testing.")

def mock_analyze_template(template_text):
    """Mock implementation for analyze_template."""
    # Simple logic to extract field names from a template
    fields = []
    for line in template_text.split("\n"):
        start = 0
        while True:
            start = line.find("[", start)
            if start == -1:
                break
            end = line.find("]", start)
            if end == -1:
                break
            field = line[start+1:end]
            if field and field not in fields:
                fields.append(field)
            start = end + 1
    return fields

# Dictionary to store original implementations
originals = {}

def apply_mocks():
    """Apply mock implementations for testing."""
    global originals
    import app.utils.api as api
    
    # Store original implementations
    originals = {
        'original_genai': api.genai,
        'original_extract_content': api.extract_document_content,
        'original_analyze_template': api.analyze_template
    }
    
    # Apply mocks
    api.genai = mock_genai
    api.extract_document_content = lambda text: mock_generate_content.text
    api.analyze_template = mock_analyze_template
    api.initialize_api = lambda: None  # Do nothing
    
    return originals

def restore_mocks():
    """Restore original implementations after testing."""
    global originals
    import app.utils.api as api
    
    api.genai = originals.get('original_genai')
    api.extract_document_content = originals.get('original_extract_content')
    api.analyze_template = originals.get('original_analyze_template')
    
    return True 