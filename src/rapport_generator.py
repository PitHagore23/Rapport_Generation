import xml.etree.ElementTree as ET
from docx import Document
import os
import json

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = {}
    for child in root:
        data[child.tag] = child.text
    return data

def generate_report(xml_file, template_file, output_file):
    data = parse_xml(xml_file)
    doc = Document(template_file)

    for paragraph in doc.paragraphs:
        if '#NOM' in paragraph.text:
            paragraph.text = paragraph.text.replace('#NOM', data.get('Nom', ''))
        if '#PRENOM' in paragraph.text:
            paragraph.text = paragraph.text.replace('#PRENOM', data.get('Prénom', ''))
        if '#AGE' in paragraph.text:
            paragraph.text = paragraph.text.replace('#AGE', data.get('Age', ''))

    doc.save(output_file)

if __name__ == "__main__":
    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)

    xml_file = config['xml_file']
    template_file = config['template_file']
    output_file = config['output_file']
    generate_report(xml_file, template_file, output_file)
    os.startfile(os.path.abspath(output_file))