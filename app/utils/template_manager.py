import os
import json
from pathlib import Path

# Default templates directory
TEMPLATES_DIR = Path("app/templates")

def get_available_templates():
    """
    Get a list of available templates.
    
    Returns:
        list: List of available template names
    """
    templates = []
    try:
        for file in os.listdir(TEMPLATES_DIR):
            if file.endswith('.txt'):
                templates.append(file.rsplit('.', 1)[0])
        return templates
    except Exception as e:
        print(f"Error getting templates: {str(e)}")
        return []

def list_templates():
    """
    List all available templates with their paths.
    
    Returns:
        dict: Dictionary of template names and paths
    """
    templates = {}
    try:
        for file in os.listdir(TEMPLATES_DIR):
            if file.endswith('.txt'):
                template_name = file.rsplit('.', 1)[0]
                templates[template_name] = str(TEMPLATES_DIR / file)
        return templates
    except Exception as e:
        print(f"Error listing templates: {str(e)}")
        return {}

def save_template(template_name, template_content):
    """
    Save a new template.
    
    Args:
        template_name (str): Name of the template
        template_content (str): Content of the template
        
    Returns:
        bool: Success status
    """
    try:
        template_path = TEMPLATES_DIR / f"{template_name}.txt"
        with open(template_path, 'w') as file:
            file.write(template_content)
        return True
    except Exception as e:
        print(f"Error saving template: {str(e)}")
        return False

def read_template(template_path):
    """
    Read a template file.
    
    Args:
        template_path (str): Path to the template file
        
    Returns:
        str: Content of the template
    """
    try:
        with open(template_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading template: {str(e)}")
        return f"Error reading template: {str(e)}"

def save_uploaded_template(uploaded_file, template_name=None):
    """
    Save an uploaded template file.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        template_name (str, optional): Name to save the template as
        
    Returns:
        str: Path to the saved template
    """
    try:
        if template_name is None:
            template_name = uploaded_file.name.rsplit('.', 1)[0]
        
        # Ensure the templates directory exists
        os.makedirs(TEMPLATES_DIR, exist_ok=True)
        
        # Save the file
        template_path = TEMPLATES_DIR / f"{template_name}.txt"
        
        with open(template_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
            
        return str(template_path)
    except Exception as e:
        print(f"Error saving uploaded template: {str(e)}")
        return None

def get_template_path(template_name):
    """
    Get the path to a template file.
    
    Args:
        template_name (str): Name of the template
        
    Returns:
        str: Path to the template file
    """
    return str(TEMPLATES_DIR / f"{template_name}.txt") 