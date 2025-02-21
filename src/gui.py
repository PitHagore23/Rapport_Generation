import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from src.report_generator import generate_report

def on_drop(event, status_label):
    xml_file = event.data
    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)

    template_file = os.path.join(config['template_dir'], config['current_template'])
    output_file = config['output_file']
    generate_report(xml_file, template_file, output_file)

    if messagebox.askyesno("Open Report", "Do you want to open the generated report?"):
        os.startfile(os.path.abspath(output_file))
    else:
        save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")])
        if save_path:
            os.rename(output_file, save_path)

def select_template(status_label):
    template_file = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
    if template_file:
        template_name = os.path.basename(template_file)
        destination = os.path.join('../Template_Directory', template_name)

        if os.path.exists(destination):
            new_name = simpledialog.askstring("Template Exists", "A template with this name already exists. Please enter a new name:")
            if not new_name:
                return
            template_name = new_name + ".docx"
            destination = os.path.join('../Template_Directory', template_name)

        shutil.copy(template_file, destination)

        with open('../config.json', 'r') as config_file:
            config = json.load(config_file)
        config['templates'].append(template_name)
        config['current_template'] = template_name
        with open('../config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
        status_label.config(text=f"Current Template: {template_name}")
        messagebox.showinfo("Template Selected", f"Template set to: {template_name}")

def select_existing_template(root, status_label):
    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)

    templates = config.get('templates', [])

    if not templates:
        messagebox.showinfo("No Templates", "No existing templates found.")
        return

    def set_template(template_name):
        config['current_template'] = template_name
        with open('../config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
        status_label.config(text=f"Current Template: {template_name}")

    template_menu = tk.Menu(root, tearoff=0)
    for template in templates:
        template_menu.add_command(label=template, command=lambda t=template: set_template(t))

    template_menu.post(root.winfo_pointerx(), root.winfo_pointery())

def manage_templates(root):
    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)

    templates = config.get('templates', [])

    if not templates:
        messagebox.showinfo("No Templates", "No templates available to manage.")
        return

    def remove_template(template_name):
        template_path = os.path.join('../Template_Directory', template_name)
        if os.path.exists(template_path):
            os.remove(template_path)
        config['templates'].remove(template_name)
        if config['current_template'] == template_name:
            config['current_template'] = config['default_template']
        with open('../config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
        messagebox.showinfo("Template Removed", f"Template {template_name} has been removed.")

    manage_menu = tk.Menu(root, tearoff=0)
    for template in templates:
        manage_menu.add_command(label=template, command=lambda t=template: remove_template(t))

    manage_menu.post(root.winfo_pointerx(), root.winfo_pointery())

def view_selected_template():
    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)
    os.startfile(os.path.abspath(os.path.join('../Template_Directory', config['current_template'])))

def create_gui():
    root = TkinterDnD.Tk()
    root.title("Rapport Generator")

    with open('../config.json', 'r') as config_file:
        config = json.load(config_file)
    config['current_template'] = config['default_template']
    with open('../config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

    menu_bar = tk.Menu(root)
    template_menu = tk.Menu(menu_bar, tearoff=0)
    template_menu.add_command(label="From Existing Templates", command=lambda: select_existing_template(root, status_label))
    template_menu.add_command(label="New Template", command=lambda: select_template(status_label))
    template_menu.add_command(label="Template Management", command=lambda: manage_templates(root))
    menu_bar.add_cascade(label="Template Selection", menu=template_menu)
    root.config(menu=menu_bar)

    label = tk.Label(root, text="Drag and drop an XML file here", width=40, height=10, bg="lightgray")
    label.pack(padx=10, pady=10)

    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', lambda event: on_drop(event, status_label))

    status_label = tk.Label(root, text=f"Current Template: {config['default_template']}", anchor='e')
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    view_template_button = tk.Button(root, text="View Selected Template", command=view_selected_template)
    view_template_button.pack(pady=10)

    root.mainloop()