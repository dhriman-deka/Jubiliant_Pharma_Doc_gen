import os
import streamlit as st
import json
import tempfile
from pathlib import Path
from datetime import datetime
import google.generativeai as genai

# Import utility modules
from utils.document_processor import (
    read_pdf, read_docx, 
    fill_template, generate_pdf, generate_docx
)
from utils.api import initialize_api, extract_document_content, analyze_template
from utils.template_manager import (
    get_available_templates, save_template, 
    save_uploaded_template, get_template_path, read_template, list_templates
)

# Ensure exports directory exists
EXPORTS_DIR = Path("app/exports")
os.makedirs(EXPORTS_DIR, exist_ok=True)

# Configure page
st.set_page_config(
    page_title="Document Generation App",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API
api_initialized = False
try:
    initialize_api()
    api_initialized = True
except Exception as e:
    st.error(f"Failed to initialize AI API: {str(e)}")
    st.sidebar.error("API key not found or invalid")
    st.sidebar.info("You'll need to add API_KEY to your environment variables or .env file.")

# Set up main title
st.title("Document Generation App")
st.write("Generate documents from templates with AI assistance.")

# Sidebar for template selection and upload
with st.sidebar:
    st.header("Template Management")
    
    # Template selection
    st.subheader("Select Template")
    templates = get_available_templates()
    selected_template = st.selectbox(
        "Choose a template",
        [""] + templates,
        key="template_select"
    )
    
    # Template upload
    st.subheader("Upload Template")
    uploaded_template = st.file_uploader(
        "Upload a custom template",
        type=["txt", "pdf"],
        key="template_upload"
    )
    
    if uploaded_template is not None:
        template_name = st.text_input("Template Name", 
                                    value=uploaded_template.name.split('.')[0])
        
        if st.button("Save Template"):
            save_path = save_uploaded_template(uploaded_template, template_name)
            if save_path:
                st.success(f"Template '{template_name}' saved successfully!")
                # Refresh template list
                templates = get_available_templates()
                # Select the newly uploaded template
                st.session_state.template_select = template_name
            else:
                st.error("Failed to save template.")

# Main content area
tab1, tab2, tab3 = st.tabs(["Upload Document", "Fill Template", "Export Document"])

# Tab 1: Document Upload and Analysis
with tab1:
    st.header("Upload and Analyze Document")
    
    uploaded_document = st.file_uploader(
        "Upload a document for analysis",
        type=["pdf", "docx"],
        key="document_upload"
    )
    
    if uploaded_document is not None:
        # Create a temporary file to store the uploaded document
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_document.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_document.getvalue())
            tmp_file_path = tmp_file.name
        
        st.success(f"Document '{uploaded_document.name}' uploaded successfully!")
        
        if st.button("Analyze Document", key="analyze_btn"):
            with st.spinner("Analyzing document... This may take a moment."):
                # Extract text based on file type
                if uploaded_document.name.lower().endswith('.pdf'):
                    document_text = read_pdf(tmp_file_path)
                elif uploaded_document.name.lower().endswith('.docx'):
                    document_text = read_docx(tmp_file_path)
                else:
                    document_text = "Unsupported file format"
                
                # Remove the temporary file
                os.unlink(tmp_file_path)
                
                if document_text.startswith("Error"):
                    st.error(document_text)
                else:
                    # Display document text
                    with st.expander("Document Content"):
                        st.text(document_text)
                    
                    # Analyze with AI if initialized
                    if api_initialized:
                        analysis_result = extract_document_content(document_text)
                        
                        if isinstance(analysis_result, str) and analysis_result.startswith("Error"):
                            st.error(analysis_result)
                        else:
                            st.session_state.analysis_result = analysis_result
                            
                            # Try to parse the analysis result
                            try:
                                analyzed_data = json.loads(analysis_result)
                                st.session_state.analyzed_data = analyzed_data
                                
                                # Display analysis result
                                st.subheader("Document Analysis")
                                st.json(analyzed_data)
                                
                                # Add a success message with instructions
                                st.success("Document analyzed successfully! Go to the 'Fill Template' tab to use this data to fill a template.")
                                
                                # Add a button to go to the Fill Template tab
                                if st.button("Go to Fill Template"):
                                    # Set active tab to Fill Template
                                    st.session_state.active_tab = "Fill Template"
                            except Exception as e:
                                st.error(f"Error parsing analysis result: {str(e)}")
                                st.text(analysis_result)  # Display the raw result
                    else:
                        st.warning("AI service not initialized. Cannot analyze document.")
                        # Store the document text for manual processing
                        st.session_state.document_text = document_text

# Tab 2: Fill Template
with tab2:
    st.header("Fill Template")
    
    # Get template content if a template is selected
    template_content = None
    template_fields = []
    
    if selected_template:
        template_path = get_template_path(selected_template)
        template_content = read_template(template_path)
        
        if not template_content.startswith("Error"):
            # Display template
            with st.expander("Template Content"):
                st.text(template_content)
            
            # Extract fields from template
            if api_initialized:
                template_fields = analyze_template(template_content)
                if isinstance(template_fields, str) and template_fields.startswith("Error"):
                    st.error(template_fields)
                    template_fields = []
            else:
                # Simple field extraction as fallback
                template_fields = [
                    field.strip("[]") for field in 
                    template_content.split("[") if "]" in field
                ]
                template_fields = list(set(template_fields))
        else:
            st.error(template_content)
    
    # Form for filling template fields
    if template_fields:
        st.subheader("Fill Template Fields")
        
        # Check if we have analysis results to pre-fill
        analysis_data = {}
        if 'analyzed_data' in st.session_state:
            try:
                # Flatten the JSON structure to a dictionary
                def flatten_json(json_obj, parent_key='', sep='_'):
                    items = {}
                    for k, v in json_obj.items():
                        new_key = f"{parent_key}{sep}{k}" if parent_key else k
                        if isinstance(v, dict):
                            items.update(flatten_json(v, new_key, sep))
                        elif isinstance(v, list):
                            # For lists, join items with commas
                            if all(isinstance(item, str) for item in v):
                                items[new_key] = ", ".join(v)
                            else:
                                # For lists of complex objects, try to extract useful information
                                for i, item in enumerate(v):
                                    if isinstance(item, dict):
                                        items.update(flatten_json(item, f"{new_key}_{i}", sep))
                        else:
                            items[new_key] = str(v)
                    return items
                
                analysis_data = flatten_json(st.session_state.analyzed_data)
                
                # Display the flattened data for debugging
                with st.expander("Available Data from Document Analysis"):
                    st.write(analysis_data)
                
                # Map field names to possible keys in analysis_data
                field_mapping = {}
                for field in template_fields:
                    # Try exact match
                    if field in analysis_data:
                        field_mapping[field] = field
                    else:
                        # Try case-insensitive match
                        field_lower = field.lower()
                        matches = [k for k in analysis_data.keys() if field_lower in k.lower()]
                        if matches:
                            field_mapping[field] = matches[0]  # Use the first match
                
                # Display the field mapping
                with st.expander("Field Mapping"):
                    st.write("The following template fields were mapped to document data:")
                    for template_field, data_field in field_mapping.items():
                        if data_field:
                            st.write(f"- {template_field} → {data_field} = {analysis_data.get(data_field, '')}")
                        else:
                            st.write(f"- {template_field} → No matching data found")
            except Exception as e:
                st.error(f"Error processing analysis data: {str(e)}")
                st.write("Raw analysis data:")
                st.write(st.session_state.get('analyzed_data', {}))
        
        # Create a form for filling out template fields
        with st.form("template_form"):
            field_values = {}
            
            for field in template_fields:
                # Try to get a default value from the analysis data
                default_value = ""
                if 'analyzed_data' in st.session_state and analysis_data:
                    # Check if we have a mapping for this field
                    if field in field_mapping and field_mapping[field]:
                        mapped_field = field_mapping[field]
                        default_value = analysis_data.get(mapped_field, "")
                    else:
                        # Try to find a field with similar name
                        field_lower = field.lower()
                        for k, v in analysis_data.items():
                            if field_lower in k.lower():
                                default_value = v
                                break
                
                field_values[field] = st.text_input(
                    field, 
                    value=default_value,
                    key=f"field_{field}"
                )
            
            submit_button = st.form_submit_button("Generate Document")
            
            if submit_button:
                filled_content = fill_template(template_content, field_values)
                st.session_state.filled_content = filled_content
                st.session_state.current_template = selected_template
                
                st.success("Template filled successfully! Go to the Export Document tab to export your document.")
                
                # Display filled content
                with st.expander("Filled Document"):
                    st.text(filled_content)
                    # Debug information about content length
                    st.info(f"Content length: {len(filled_content)} characters")
                
                # Add a button to go to the Export Document tab
                if st.button("Go to Export Document"):
                    # Set active tab to Export Document
                    st.session_state.active_tab = "Export Document"

# Tab 3: Export Document
with tab3:
    st.header("Export Document")
    
    if 'filled_content' in st.session_state:
        # Display filled content
        with st.expander("Document to Export"):
            st.text(st.session_state.filled_content)
            # Debug information about the filled content
            st.info(f"Content length: {len(st.session_state.filled_content)} characters")
        
        # Export options
        st.subheader("Export Options")
        
        export_format = st.radio("Export Format", ["PDF", "DOCX"])
        export_name = st.text_input("File Name", 
                                  value=f"{st.session_state.current_template}_filled")
        
        if st.button("Export Document"):
            filled_content = st.session_state.filled_content
            
            # Debug check for content
            if not filled_content or len(filled_content.strip()) == 0:
                st.error("Error: Document content is empty. Make sure you have filled the template.")
                st.stop()
            
            # Create export path
            if export_format == "PDF":
                export_path = EXPORTS_DIR / f"{export_name}.pdf"
                success = generate_pdf(filled_content, str(export_path))
            else:  # DOCX
                export_path = EXPORTS_DIR / f"{export_name}.docx"
                success = generate_docx(filled_content, str(export_path))
            
            if success:
                st.success(f"Document exported successfully to {export_path}")
                
                # Check file size for debugging
                file_size = os.path.getsize(export_path)
                st.info(f"Generated file size: {file_size} bytes")
                
                # Create a download button
                with open(export_path, "rb") as file:
                    file_data = file.read()
                    st.download_button(
                        label=f"Download {export_format}",
                        data=file_data,
                        file_name=export_path.name,
                        mime=("application/pdf" if export_format == "PDF" 
                              else "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    )
            else:
                st.error(f"Failed to export document as {export_format}")
    else:
        st.info("Please fill a template in the 'Fill Template' tab before exporting.")

# Add a chat interface at the bottom
st.divider()
st.subheader("AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Define the chat API status
chat_api_available = api_initialized

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if chat_api_available:
    prompt = st.chat_input("Ask about your document...")
    
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from AI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get current document context if available
                context = ""
                if 'filled_content' in st.session_state:
                    context = f"Current document content:\n{st.session_state.filled_content}\n\n"
                
                # Create the prompt with context
                full_prompt = f"""You are an AI assistant embedded in a Document Generation App. 
                Your purpose is to help users with:
                1. Selecting and filling document templates
                2. Analyzing uploaded documents
                3. Generating documents from templates
                4. Exporting documents in PDF or DOCX format
                
                The app has templates like business letters, invoices, and contracts.
                
                When users ask to generate documents, help them use the app's features rather than just describing what you would do.
                Refer them to use the template selection, document upload, or export functions in the app interface.
                
                Current document context:
                {context}
                
                User query: {prompt}"""
                
                try:
                    # Import the preferred model function and genai
                    from utils.api import get_preferred_model, genai
                    
                    # Get the preferred model
                    model_name = get_preferred_model()
                    
                    if not model_name:
                        st.error("Error: No suitable AI models available with your API key")
                    else:
                        print(f"Using model: {model_name} for chat")
                        model = genai.GenerativeModel(model_name)
                        
                        try:
                            response = model.generate_content(full_prompt)
                            st.write(response.text)
                            
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        except Exception as api_error:
                            error_str = str(api_error)
                            if "429" in error_str or "quota" in error_str.lower() or "exhausted" in error_str.lower():
                                error_msg = "AI service quota has been exhausted. Please try again later or update your API key."
                                st.error(error_msg)
                                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                            else:
                                raise api_error
                except Exception as e:
                    st.error(f"Error communicating with AI service: {str(e)}")
else:
    st.warning("Chat functionality requires AI service to be initialized.")

if __name__ == "__main__":
    st.run() 