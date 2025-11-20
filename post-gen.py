import sys
import os
from datetime import datetime
from build_blog import build_blog
# CONFIGURATION
TEMPLATE_PATH = 'posts/post-template.html'
POSTS_DIR = 'posts'

def create_post(title, tags):
    # 1. Generate a filename from the title
    # e.g. "My New Post" -> "my-new-post.html"
    slug = title.lower().strip().replace(' ', '-')
    # Remove weird characters to keep filename clean
    slug = "".join(c for c in slug if c.isalnum() or c == '-')
    filename = f"{slug}.html"
    filepath = os.path.join(POSTS_DIR, filename)

    # Check if file already exists to prevent overwriting
    if os.path.exists(filepath):
        print(f"❌ Error: File '{filename}' already exists!")
        return

    # 2. Get Current Date from PC
    current_date = datetime.now().strftime("%b %d, %Y") # e.g. Nov 20, 2025

    # 3. Read the Template
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find template at {TEMPLATE_PATH}")
        return

    # 4. Replace Placeholders
    new_content = content.replace('{{TITLE}}', title)
    new_content = new_content.replace('{{DATE}}', current_date)
    new_content = new_content.replace('{{TAGS}}', tags)
    print(current_date)
    # 5. Write the new file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Success! Created: {filepath}")
    print(f"📅 Date stamped: {current_date}")

if __name__ == "__main__":
    # Check if user provided arguments
    if len(sys.argv) < 2:
        print("Usage: python new.py \"Post Title\" \"#tag1 #tag2\"")
    else:
        post_title = sys.argv[1]
        # If tags are provided, use them, otherwise default to #untagged
        post_tags = sys.argv[2] if len(sys.argv) > 2 else "#untagged"
        
        create_post(post_title, post_tags)