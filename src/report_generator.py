import xml.etree.ElementTree as ET
from docx import Document
import json
import os

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