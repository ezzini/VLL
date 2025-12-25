import os
import re
import yaml
import glob
from pathlib import Path

# Base paths
BASE_DIR = r"c:\Users\wwwsa\OneDrive - KFUPM\Research\VLL\VLL"
CONTENT_DIR = os.path.join(BASE_DIR, "content")
AUTHORS_DIR = os.path.join(CONTENT_DIR, "authors")
PUBLICATION_DIR = os.path.join(CONTENT_DIR, "publication")
PROJECT_DIR = os.path.join(CONTENT_DIR, "project")

# Ensure directories exist
os.makedirs(AUTHORS_DIR, exist_ok=True)
os.makedirs(PUBLICATION_DIR, exist_ok=True)
os.makedirs(PROJECT_DIR, exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "ongoing"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "completed"), exist_ok=True)

# ---------------------------------------------------------
# 1. Update Authors
# ---------------------------------------------------------

# Define the team structure
team_structure = {
    "Principal Investigators": ["Dr. Hamza Luqman", "Dr. Saad Ezzini"],
    "Postdocs": ["Dr. Pavan Kumar", "Dr. Abderraouf Maoudj", "Dr. Muhammad Ghani"],
    "Graduate Researchers": [
        "Fatimah Alali", "Ahmed Abdelaal", "Aisha Alansari", "Doaa Dalaq",
        "Ahmed Abul Hasanaath", "Ogtay Hasanov", "Amneh Al Abdi", "Danah Aldossary",
        "Hind Alatawi", "Nour Zeghib", "Hania Ghouse", "Reem Alzahrani"
    ],
    "Collaborators": ["Dr. XX", "Dr. YY"]
}

# Helper to normalize names for folder naming
def get_slug(name):
    # Remove Dr. prefix and clean
    clean = name.replace("Dr. ", "").strip().lower()
    # Use first name or first-last
    # Keep it simple: first name if unique in list?
    # Better: first-last
    return clean.replace(" ", "-")

# Helper to find existing folder even if named differently (e.g. by first name)
def find_author_dir(name):
    # Try fuzzy match on first name
    clean_name = name.replace("Dr. ", "").strip()
    first_name = clean_name.split(" ")[0].lower()
    last_name = clean_name.split(" ")[-1].lower()
    
    # Check strict slug first
    slug = get_slug(name)
    if os.path.exists(os.path.join(AUTHORS_DIR, slug)):
        return os.path.join(AUTHORS_DIR, slug)
        
    # Check first name folder
    if os.path.exists(os.path.join(AUTHORS_DIR, first_name)):
        return os.path.join(AUTHORS_DIR, first_name)

    # Check common existing map from observation
    known_map = {
        "Dr. Saad Ezzini": "saad",
        "Dr. Abderraouf Maoudj": "abderaouf", # note spelling abderaouf vs abderraouf
        "Fatimah Alali": "fatimah",
        "Amneh Al Abdi": "amneh",
        "Danah Aldossary": "danah",
        "Hind Alatawi": "hind",
        "Ogtay Hasanov": "ogtay",
    }
    if name in known_map and os.path.exists(os.path.join(AUTHORS_DIR, known_map[name])):
         return os.path.join(AUTHORS_DIR, known_map[name])
         
    return None

def update_or_create_author(name, group):
    folder_path = find_author_dir(name)
    if not folder_path:
        # Create new
        slug = get_slug(name)
        folder_path = os.path.join(AUTHORS_DIR, slug)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Creating new author: {name} in {folder_path}")
        
    index_file = os.path.join(folder_path, "_index.md")
    
    content = ""
    frontmatter = {}
    
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            raw = f.read()
            # extract frontmatter
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', raw, re.DOTALL)
            if match:
                try:
                    frontmatter = yaml.safe_load(match.group(1))
                    content = match.group(2)
                except Exception as e:
                    print(f"Error parsing yaml for {name}: {e}")
            else:
                # Basic create
                pass
    
    # Update fields
    if "title" not in frontmatter:
        frontmatter["title"] = name.replace("Dr. ", "") # Display name without Dr? Or with? User listed with Dr.
        # Actually usually title is full name.
        frontmatter["title"] = name
        
    frontmatter["user_groups"] = [group]
    
    # Write back
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.dump(frontmatter, sort_keys=False))
        f.write("---\n")
        f.write(content)

print("Updating authors...")
for group, names in team_structure.items():
    for name in names:
        update_or_create_author(name, group)

# ---------------------------------------------------------
# 2. Projects
# ---------------------------------------------------------
print("Updating projects...")
ongoing_index = os.path.join(PROJECT_DIR, "ongoing", "_index.md")
completed_index = os.path.join(PROJECT_DIR, "completed", "_index.md")

def create_project_index(path, title):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"title: {title}\n")
            f.write("view: card\n")
            f.write("---\n")

create_project_index(ongoing_index, "Ongoing Projects")
create_project_index(completed_index, "Completed Projects")

# Create main project index if not exists to list subfolders
main_project_index = os.path.join(PROJECT_DIR, "_index.md")
if not os.path.exists(main_project_index):
    with open(main_project_index, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("title: Projects\n")
        f.write("view: card\n") # This might just list everything
        f.write("---\n")
        f.write("Below you can find our ongoing and completed projects.\n\n")
        
        # We can add explicit links or rely on the theme listing subsections?
        # Theme usually lists child pages. Subsections are child sections.
        # We'll leave it simple.
        
# ---------------------------------------------------------
# 3. Bibtex Publications
# ---------------------------------------------------------
print("Updating publications...")
# Simple regex-based bibtex parser because installing libraries might be restricted or slow
def parse_bibtex(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    entries = []
    # Split by @type{
    # This regex matches @entrytype{citekey, content}
    # It assumes standard formatting.
    pattern = re.compile(r'@(\w+)\s*{\s*([^,]+),', re.MULTILINE)
    
    pos = 0
    while True:
        match = pattern.search(content, pos)
        if not match:
            break
            
        entry_type = match.group(1).lower()
        cite_key = match.group(2).strip()
        start = match.end()
        
        # Find matching brace
        brace_count = 1
        end = start
        while brace_count > 0 and end < len(content):
            if content[end] == '{':
                brace_count += 1
            elif content[end] == '}':
                brace_count -= 1
            end += 1
            
        entry_content = content[start:end-1] # content inside braces
        
        # Parse fields
        fields = {}
        # field = {value} or field = "value" or field = value
        field_pattern = re.compile(r'(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|"((?:[^"]|\\")*)"|(\w+))', re.DOTALL)
        
        for f_match in field_pattern.finditer(entry_content):
            key = f_match.group(1).lower()
            val = f_match.group(2) or f_match.group(3) or f_match.group(4)
            val = re.sub(r'\s+', ' ', val).strip() # clean whitespace
            fields[key] = val
            
        entries.append({
            "type": entry_type,
            "key": cite_key,
            "fields": fields
        })
        
        pos = end
        
    return entries

bib_path = os.path.join(BASE_DIR, "my_publications.bib")
if os.path.exists(bib_path):
    entries = parse_bibtex(bib_path)
    
    for entry in entries:
        cite_key = entry['key']
        fields = entry['fields']
        
        # Create directory
        pub_folder = os.path.join(PUBLICATION_DIR, cite_key)
        os.makedirs(pub_folder, exist_ok=True)
        
        index_file = os.path.join(pub_folder, "index.md")
        
        # Prepare frontmatter
        title = fields.get('title', 'Untitled').replace('{', '').replace('}', '').replace('"', '')
        date = fields.get('year', '2025') + "-01-01" # Default date
        
        # Authors list
        authors_raw = fields.get('author', '')
        authors = [a.strip().replace('{', '').replace('}', '') for a in authors_raw.split(' and ')]
        
        # Publication type
        # 0: Uncategorized, 1: Conference paper, 2: Journal article, 3: Preprint, 4: Report, 5: Book, 6: Book section
        pub_type = '2' # Default journal
        if entry['type'] == 'inproceedings' or entry['type'] == 'conference':
            pub_type = '1'
        elif entry['type'] == 'article':
            pub_type = '2'
        elif entry['type'] == 'book':
            pub_type = '5'
        
        publication_name = fields.get('journal') or fields.get('booktitle') or fields.get('publisher', '')
        
        frontmatter = {
            "title": title,
            "date": date,
            "authors": authors,
            "publication_types": [pub_type],
            "publication": publication_name,
            "abstract": "" # Bibtex doesn't always have abstract, leave empty
        }
        
        # Write file
        with open(index_file, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml.dump(frontmatter, sort_keys=False))
            f.write("---\n")

print("Docs generated.")
