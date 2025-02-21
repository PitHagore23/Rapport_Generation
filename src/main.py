import os
import json
from src.gui import create_gui

def ensure_resources():
    template_dir = os.path.join(os.path.dirname(__file__), '../Template_Directory')
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')

    if not os.path.exists(template_dir):
        os.makedirs(template_dir)

    if not os.path.exists(config_path):
        config = {
            "template_dir": template_dir,
            "templates": [],
            "default_template": "",
            "current_template": "",
            "xml_file": "",
            "output_file": os.path.join(template_dir, 'report.docx')
        }
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)

if __name__ == "__main__":
    ensure_resources()
    create_gui()