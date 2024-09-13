import logging
import os
from lxml import etree
import sys

# Function to generate filename
def generate_filename(base_path, extension):
    return f"{base_path}.{extension}"

# Function to find the most recent XML file
def find_most_recent_xml(directory):
    xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]
    if not xml_files:
        raise FileNotFoundError(f"No XML files found in directory: {directory}")
    most_recent_file = max(xml_files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, most_recent_file)

# Function to ensure a directory exists
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")

# Get command line arguments
if len(sys.argv) != 5:
    raise ValueError("Expected 4 arguments: XML directory, HTML directory, build number, job name")

xml_dir = sys.argv[1]
html_dir = sys.argv[2]
build_number = sys.argv[3]
job_name = sys.argv[4]

# Hardcoded paths 
xslt_file = 'C:\\Users\\LKiruba\\Desktop\\Calculator_Soapui_CICD\\report-transform.xslt'
log_dir = 'C:\\Reports\\CICD_SOAPUI\\Log'

# Ensure the necessary directories exist
ensure_directory(html_dir)
ensure_directory(log_dir)

# Find the most recent XML file
xml_file = find_most_recent_xml(xml_dir)

# Generate a timestamped HTML filename
html_file = generate_filename(os.path.join(html_dir, f'TEST-{job_name}'), 'html')

# Generate a timestamped log filename
log_filename = generate_filename(os.path.join(log_dir, f'transform_{job_name}'), 'log')

# Configure logging
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def transform_xml_to_html(xml_file, xslt_file, html_file, build_number, job_name):
    try:
        if not os.path.exists(xml_file):
            raise FileNotFoundError(f"XML file not found: {xml_file}")
        if not os.path.exists(xslt_file):
            raise FileNotFoundError(f"XSLT file not found: {xslt_file}")

        logging.info(f"Loading XML file: {xml_file}")
        xml = etree.parse(xml_file)
        logging.info(f"Loading XSLT file: {xslt_file}")
        xslt = etree.parse(xslt_file)

        transform = etree.XSLT(xslt)
        result = transform(xml)

        with open(html_file, 'wb') as f:
            f.write(etree.tostring(result, pretty_print=True, method='html'))
        logging.info(f"Transformation successful. HTML saved to: {html_file}")

        logging.info(f"Transformation details - Build Number: {build_number}, Job Name: {job_name}")

    except Exception as e:
        logging.error(f"Error during XML to HTML transformation: {str(e)}")
        raise

transform_xml_to_html(xml_file, xslt_file, html_file, build_number, job_name)
