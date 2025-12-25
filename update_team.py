import os
import shutil
import yaml
import re

# Base paths
BASE_DIR = r"c:\Users\wwwsa\OneDrive - KFUPM\Research\VLL\VLL"
CONTENT_DIR = os.path.join(BASE_DIR, "content")
AUTHORS_DIR = os.path.join(CONTENT_DIR, "authors")

# Avatar sources (relative to AUTHORS_DIR)
FEMALE_AVATAR_SOURCE = os.path.join(AUTHORS_DIR, "fatimah", "avatar.jpg")
MALE_AVATAR_SOURCE = os.path.join(AUTHORS_DIR, "abderaouf", "avatar.jpg")

# Define Data
# Structure: Group -> list of (Name, Role, Gender)
# Gender: 'M' or 'F' or None (if keeping existing or specific)
# Role: specific title

team_data = {
    "Principal Investigators": [
        {"name": "Dr. Hamza Luqman", "role": "Principal Investigator", "gender": "M"},
        {"name": "Dr. Saad Ezzini", "role": "Principal Investigator", "gender": "M"} 
    ],
    "Postdocs": [
        {"name": "Dr. Pavan Kumar", "role": "Postdoctoral Researcher", "gender": "M"},
        {"name": "Dr. Abderraouf Maoudj", "role": "Postdoctoral Researcher", "gender": "M"},
        {"name": "Dr. Muhammad Ghani", "role": "Postdoctoral Researcher", "gender": "M"}
    ],
    "Graduate Researchers": [
        {"name": "Fatimah Alali", "role": "PhD Student", "gender": "F"}, # Assume existing
        {"name": "Ahmed Abdelaal", "role": "Master Student", "gender": "M"}, # New
        {"name": "Aisha Alansari", "role": "Master Student", "gender": "F"}, # New
        {"name": "Doaa Dalaq", "role": "Master Student", "gender": "F"}, # New
        {"name": "Ahmed Abul Hasanaath", "role": "Master Student", "gender": "M"}, # New
        {"name": "Ogtay Hasanov", "role": "Master Student", "gender": "M"}, 
        {"name": "Amneh Al Abdi", "role": "Master Student", "gender": "F"}, 
        {"name": "Danah Aldossary", "role": "PhD Student", "gender": "F"}, # Assume exist
        {"name": "Hind Alatawi", "role": "PhD Student", "gender": "F"}, # Assume exist
        {"name": "Nour Zeghib", "role": "PhD Student", "gender": "F"}, # New PhD
        {"name": "Hania Ghouse", "role": "PhD Student", "gender": "F"}, # New PhD
        {"name": "Reem Alzahrani", "role": "PhD Student", "gender": "F"} # New PhD
    ],
    "Collaborators": [
        {"name": "Dr. XX", "role": "Collaborator", "gender": "M"},
        {"name": "Dr. YY", "role": "Collaborator", "gender": "M"}
    ]
}

# New Students only logic provided: Reem, Hania, Nour = PhD. Rest new = Master.
# I manually applied this above.

# Helper to find existing folder
def find_author_dir(name):
    slug = name.replace("Dr. ", "").strip().lower().replace(" ", "-") # Standard slug
    
    # Check standard slug
    if os.path.exists(os.path.join(AUTHORS_DIR, slug)):
        return os.path.join(AUTHORS_DIR, slug)
        
    # Check first name (legacy folders like 'saad', 'fatimah')
    clean_name = name.replace("Dr. ", "").strip()
    first_name = clean_name.split(" ")[0].lower()
    if os.path.exists(os.path.join(AUTHORS_DIR, first_name)):
        return os.path.join(AUTHORS_DIR, first_name)
        
    return None # Not found, standard slug will be created by caller if needed

def get_slug_path(name):
    slug = name.replace("Dr. ", "").strip().lower().replace(" ", "-")
    return os.path.join(AUTHORS_DIR, slug)

print("Updating team details...")

for group, members in team_data.items():
    for member in members:
        name = member['name']
        role = member['role']
        gender = member['gender']
        
        # Find path
        path = find_author_dir(name)
        if not path:
            path = get_slug_path(name)
            os.makedirs(path, exist_ok=True)
            new = True
        else:
            new = False
            
        # Update _index.md
        index_file = os.path.join(path, "_index.md")
        frontmatter = {}
        content = ""
        
        if os.path.exists(index_file):
            with open(index_file, "r", encoding="utf-8") as f:
                raw = f.read()
                match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', raw, re.DOTALL)
                if match:
                    frontmatter = yaml.safe_load(match.group(1))
                    content = match.group(2)
        
        # Set fields
        frontmatter['title'] = name
        frontmatter['role'] = role
        frontmatter['user_groups'] = [group]
        
        # Write back
        with open(index_file, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml.dump(frontmatter, sort_keys=False))
            f.write("---\n")
            f.write(content)
            
        # Handle Avatar
        avatar_dest = os.path.join(path, "avatar.jpg")
        
        # Only copy if avatar doesn't exist OR if we want to enforce uniformity for new people
        # User said "use the same... for the new... and male for male ones"
        # I'll enforce for everyone in the list except PIs maybe?
        # Actually, let's only copy if missing or if it's one of the "New" people who likely don't have one or have a wrong one.
        # But determining "New" programmatically is hard without state.
        # I will check if avatar exists. If not, copy.
        # If it exists, I'll leave it alone (like for Saad, Fatimah, etc who have custom ones)
        # EXCEPT for the "New" people I just created folders for.
        # How do I know? I can't effectively.
        # But I assume the existing folders (from before this session) have avatars.
        # The new folders I created in previous turn likely DO NOT have avatars.
        # So: If avatar.jpg does not exist, copy based on gender.
        
        if not os.path.exists(avatar_dest):
            if gender == 'F':
                if os.path.exists(FEMALE_AVATAR_SOURCE):
                    shutil.copy(FEMALE_AVATAR_SOURCE, avatar_dest)
                    print(f"Copied Female avatar to {name}")
                else:
                    print(f"Warning: Female source avatar not found at {FEMALE_AVATAR_SOURCE}")
            elif gender == 'M':
                if os.path.exists(MALE_AVATAR_SOURCE):
                    shutil.copy(MALE_AVATAR_SOURCE, avatar_dest)
                    print(f"Copied Male avatar to {name}")
                else:
                    print(f"Warning: Male source avatar not found at {MALE_AVATAR_SOURCE}")

print("Team update complete.")
