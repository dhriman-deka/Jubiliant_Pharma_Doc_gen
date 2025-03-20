import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def initialize_api():
    """Initialize the AI API with the API key."""
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=API_KEY)
    
    # Test the connection and model availability
    try:
        models = genai.list_models()
        available_models = [model.name for model in models]
        print(f"Available models: {available_models}")
        
        # Find the appropriate Gemini Pro model
        gemini_models = [name for name in available_models if "gemini" in name]
        if gemini_models:
            print(f"Found Gemini models: {gemini_models}")
        else:
            print("Warning: No Gemini models found")
    except Exception as e:
        print(f"Error checking available models: {str(e)}")

# For backward compatibility
def initialize_gemini():
    """Alias for initialize_api to maintain backward compatibility."""
    return initialize_api()

def get_preferred_model():
    """Get the preferred Gemini model, prioritizing Gemini 1.5 Pro."""
    try:
        models = genai.list_models()
        # First preference: Gemini 1.5 Pro
        for model in models:
            if "gemini-1.5-pro" in model.name and "vision" not in model.name:
                return model.name
        
        # Second preference: Any Gemini 1.5 model
        for model in models:
            if "gemini-1.5" in model.name and "vision" not in model.name:
                return model.name
        
        # Third preference: Any Gemini model that's not Vision
        for model in models:
            if "gemini" in model.name and "vision" not in model.name:
                return model.name
        
        # If no preferred models found, return the first Gemini model
        gemini_models = [model.name for model in models if "gemini" in model.name]
        if gemini_models:
            return gemini_models[0]
        
        return None
    except Exception as e:
        print(f"Error getting preferred model: {str(e)}")
        return None

def extract_document_content(document_text):
    """
    Use AI API to extract content from documents.
    
    Args:
        document_text (str): The text content of the document
        
    Returns:
        dict: Extracted information from the document
    """
    try:
        # Get preferred model
        model_name = get_preferred_model()
        
        if not model_name:
            return "Error: No suitable AI models available with your API key"
        
        print(f"Using model: {model_name} for document extraction")
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        Extract key information from the following document:
        
        {document_text}
        
        Identify and structure the following information in a JSON format:
        - Names of people or organizations
        - Dates
        - Addresses
        - Contact information
        - Financial information (if present)
        - Key topics or subjects
        - Any important statements or claims
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as api_error:
            error_str = str(api_error)
            if "429" in error_str or "quota" in error_str.lower() or "exhausted" in error_str.lower():
                # Provide a user-friendly message for quota exhaustion
                return """{"error": "API quota exhausted", 
                   "message": "The AI service quota has been exhausted. Please try again later or update your API key.",
                   "extracted_content": "Limited extraction available due to API quota limits."
                }"""
            else:
                raise api_error
                
    except Exception as e:
        return f"Error extracting content: {str(e)}"

def analyze_template(template_text):
    """
    Use AI API to analyze a template and identify fields.
    
    Args:
        template_text (str): The text content of the template
        
    Returns:
        list: List of fields found in the template
    """
    try:
        # Get preferred model
        model_name = get_preferred_model()
        
        if not model_name:
            return "Error: No suitable AI models available with your API key"
        
        print(f"Using model: {model_name} for template analysis")
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        Analyze the following document template and identify all placeholder fields.
        
        Template:
        {template_text}
        
        Extract all placeholders that are marked with [FIELD_NAME] format.
        Return only a Python list of the field names without the brackets.
        """
        
        try:
            response = model.generate_content(prompt)
            
            # Process response to extract field names
            # The response might be in various formats, so we need to handle it properly
            try:
                # Try to extract a Python list from the response
                response_text = response.text.strip()
                
                # Check if response is wrapped in code blocks
                if "```" in response_text:
                    # Extract content between code blocks
                    code_parts = response_text.split("```")
                    for part in code_parts:
                        if part.strip() and not part.strip().startswith("python"):
                            response_text = part.strip()
                            break
                
                # Clean up the response to get just the field names
                field_names = []
                for line in response_text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('[') and not line.startswith('"[') and not line.startswith("'["):
                        # Remove quotes, brackets, commas
                        line = line.strip('"\'[] ,')
                        if line:
                            field_names.append(line)
                
                return field_names
            except Exception as parsing_error:
                return f"Error parsing response: {str(parsing_error)}"
        except Exception as api_error:
            error_str = str(api_error)
            if "429" in error_str or "quota" in error_str.lower() or "exhausted" in error_str.lower():
                # Try to extract fields manually as a fallback
                print("API quota exhausted, falling back to manual extraction")
                return extract_fields_manually(template_text)
            else:
                raise api_error
            
    except Exception as e:
        return f"Error analyzing template: {str(e)}"

def extract_fields_manually(template_text):
    """
    Extract fields from a template manually when API is unavailable.
    
    Args:
        template_text (str): The text content of the template
        
    Returns:
        list: List of fields found in the template
    """
    try:
        print("Extracting fields manually...")
        # Look for patterns like [FIELD_NAME]
        fields = []
        start_idx = 0
        
        while True:
            # Find opening bracket
            open_bracket = template_text.find('[', start_idx)
            if open_bracket == -1:
                break
                
            # Find closing bracket
            close_bracket = template_text.find(']', open_bracket)
            if close_bracket == -1:
                break
                
            # Extract field name
            field_name = template_text[open_bracket+1:close_bracket]
            if field_name and field_name not in fields:
                fields.append(field_name)
                
            # Move to next position
            start_idx = close_bracket + 1
        
        return fields
    except Exception as e:
        print(f"Manual extraction failed: {str(e)}")
        # Return a message that will be displayed to the user
        return "API quota exhausted. Please try again later or update your API key." 