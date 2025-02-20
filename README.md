# Rapport_Generation

The goal of this project is to be able to generate a report in .docx format, starting from a .docx template and filling relevant data from a .xml file.

## Installation

### Step 1: Clone the Git Repository

```sh
git clone https://github.com/PitHagore23/Rapport_Generation.git
cd Rapport_Generation
```

### Step 2: Install Python

```sh
python -m venv venv
```

### Step 3: Activate the Virtual Environment

```sh
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
``` 

### Step 4: Install the Required Libraries

```sh
pip install -r requirements.txt
```

## Test the Application

```sh
python src/rapport_generator.py
```

## Usage

### Step 1: Open the Configuration File

```sh
nano config.json
```

### Step 2: Modify the Configuration File

```json
{
    "template": "new_template_path.docx",
    "output": "new_output_path.docx",
    "data": "new_data_path.xml"
}
```

### Step 3: Run the Application

```sh
python src/rapport_generator.py
```
