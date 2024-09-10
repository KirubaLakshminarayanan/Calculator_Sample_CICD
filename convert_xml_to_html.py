import logging
import os
from lxml import etree
from datetime import datetime

# Function to generate timestamped filename
def timestamped_filename(base_path, extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_path}_{timestamp}.{extension}"

# Function to find the most recent XML file
def find_most_recent_xml(directory):
    # Get all XML files in the directory
    xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]
    
    if not xml_files:
        raise FileNotFoundError(f"No XML files found in directory: {directory}")

    # Find the most recent XML file
    most_recent_file = max(xml_files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, most_recent_file)

# Function to ensure a directory exists
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")

# Hardcoded paths
xml_dir = 'C:\\Reports\\SoapUI_CICD_Calculator\\XML'
html_dir = 'C:\\Reports\\SoapUI_CICD_Calculator\\HTML'
xslt_file = 'C:\\Users\\LKiruba\\Desktop\\SoapUI_Automation_CICD\\report-transform.xslt'
log_dir = 'C:\\Reports\\SoapUI_CICD_Calculator\\Log'

# Ensure the necessary directories exist
ensure_directory(html_dir)
ensure_directory(log_dir)

# Find the most recent XML file
xml_file = find_most_recent_xml(xml_dir)

# Generate a timestamped HTML filename
html_file = timestamped_filename(os.path.join(html_dir, 'TEST-CalculatorTestSuite'), 'html')

# Generate a timestamped log filename
log_filename = timestamped_filename(os.path.join(log_dir, 'transform'), 'log')

# Configure logging
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def transform_xml_to_html(xml_file, xslt_file, html_file):
    try:
        # Check if files exist
        if not os.path.exists(xml_file):
            raise FileNotFoundError(f"XML file not found: {xml_file}")
        if not os.path.exists(xslt_file):
            raise FileNotFoundError(f"XSLT file not found: {xslt_file}")

        # Load XML and XSLT
        logging.info(f"Loading XML file: {xml_file}")
        xml = etree.parse(xml_file)
        logging.info(f"Loading XSLT file: {xslt_file}")
        xslt = etree.parse(xslt_file)
        transform = etree.XSLT(xslt)
        
        # Pass the current date and time as a parameter
        params = {
            'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Transform XML to HTML
        logging.info("Starting XML to HTML transformation")
        html = transform(xml, generation_date=etree.XSLT.strparam(params['generation_date']))
        
        # Save the HTML to a file
        logging.info(f"Saving HTML file: {html_file}")
        with open(html_file, 'wb') as f:
            f.write(etree.tostring(html, pretty_print=True))
        logging.info("Transformation completed successfully")

    except FileNotFoundError as e:
        logging.error(e)
    except etree.XMLSyntaxError as e:
        logging.error(f"XML syntax error: {e}")
    except etree.XSLTParseError as e:
        logging.error(f"XSLT parse error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Execute the transformation
transform_xml_to_html(xml_file, xslt_file, html_file)
