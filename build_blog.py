import os
import re
import json
from datetime import datetime

# --- CONFIGURATION ---
POSTS_DIR = 'posts'
BLOG_OUTPUT = 'blog.html'
PUB_OUTPUT = 'publications.html'
PUB_DATA = 'publications.json'

# --- SHARED HTML (Sidebar & Head) ---
def get_html_structure(title, active_page, content_area):
    # Determine active class for nav
    nav_home = 'active' if active_page == 'home' else ''
    nav_pub  = 'active' if active_page == 'publications' else ''
    nav_blog = 'active' if active_page == 'blog' else ''
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2503/2503401.png">
    <style>
        /* Tag Cloud Styles */
        .tag-cloud {{ margin-bottom: 25px; display: flex; gap: 10px; flex-wrap: wrap; }}
        .tag-btn {{
            background: transparent; border: 1px solid var(--border-color);
            color: var(--text-dim); padding: 4px 12px; border-radius: 15px;
            cursor: pointer; font-size: 0.8rem; font-family: var(--font-text);
            transition: all 0.2s;
        }}
        .tag-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
        .tag-btn.active {{ background: var(--accent); color: #111; border-color: var(--accent); font-weight: bold; }}
        .blog-entry.hidden {{ display: none; }}
    </style>
</head>
<body>
    <button class="theme-toggle" id="theme-toggle"><i class="fas fa-sun"></i></button>
    <div class="container">
        <aside class="sidebar">
            <a href="index.html"><img src="pics/my_gif.gif" alt="Robert" class="my-photo"></a>
            <div class="name"><a href="index.html">Robert<br>Grinshtein</a></div>
            <div style="color: var(--text-dim); font-size: 0.9rem; margin-bottom: 20px;">Graduate student</div>
            <ul class="nav-links">
                <li><a href="index.html#about" class="{nav_home}">About</a></li>
                <li><a href="publications.html" class="{nav_pub}">Publications</a></li>
                <li><a href="index.html#career">Career</a></li>
                <li><a href="index.html#rewards">Rewards</a></li>
                <li><a href="blog.html" class="{nav_blog}">Blog</a></li>
                <li><a href="CV_2025.pdf">CV (PDF)</a></li>
            </ul>
            <div class="contacts">
                email:<a href="mailto:grinshtein.ra21@physics.msu.ru" style="color: var(--text-dim)"> grinshtein.ra21@<br>physics.msu.ru</a><br><br>
                github: <a href="https://github.com/robikgrin">@robikgrin</a><br>
                telegram: <a href="https://t.me/robikgrin">@robikgrin</a>
            </div>
        </aside>
        <main class="content">
            <section class="visible">
                {content_area}
            </section>
        </main>
    </div>
    <script src="scripts/script.js"></script>
    <!-- Optional: Blog Tag Filter Script (Only runs if tags exist) -->
    <script>
        if(document.querySelector('.tag-cloud')) {{
            function filterTags(tag) {{
                document.querySelectorAll('.tag-btn').forEach(btn => {{
                    btn.classList.remove('active');
                    if(btn.innerText.includes(tag) || (tag === 'all' && btn.innerText === 'All')) btn.classList.add('active');
                }});
                document.querySelectorAll('.blog-entry').forEach(entry => {{
                    if (tag === 'all') entry.classList.remove('hidden');
                    else {{
                        const tags = entry.getAttribute('data-tags');
                        if (tags && tags.includes(tag)) entry.classList.remove('hidden');
                        else entry.classList.add('hidden');
                    }}
                }});
            }}
        }}
    </script>
</body>
</html>"""

# --- 1. BUILD BLOG ---
def build_blog():
    posts = []
    all_tags = set()
    
    # Regex
    title_re = re.compile(r'<h1>(.*?)</h1>')
    meta_re = re.compile(r'<div class="post-meta">\s*(.*?)\s*•\s*(.*?)\s*</div>')

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith('.html') or filename == 'post-template.html': continue
        
        with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            t_match = title_re.search(content)
            title = t_match.group(1) if t_match else "Untitled"
            m_match = meta_re.search(content)
            
            if m_match:
                date_str = m_match.group(1).strip()
                tags = [t.replace('#', '').strip() for t in m_match.group(2).split()]
                try: date_obj = datetime.strptime(date_str, '%b %d, %Y')
                except: date_obj = datetime.min
                all_tags.update(tags)
            else:
                date_str, tags, date_obj = "Unknown", [], datetime.min

            posts.append({'title': title, 'date': date_str, 'dt': date_obj, 'tags': tags, 'url': f"{POSTS_DIR}/{filename}"})

    posts.sort(key=lambda x: x['dt'], reverse=True)

    # Generate Content HTML
    content_html = '<h2>Log / Blog</h2>\n<div class="tag-cloud">\n'
    content_html += '<button class="tag-btn active" onclick="filterTags(\'all\')">All</button>\n'
    for tag in sorted(list(all_tags)):
        content_html += f'<button class="tag-btn" onclick="filterTags(\'{tag}\')">#{tag}</button>\n'
    content_html += '</div>\n'

    for post in posts:
        content_html += f'''
        <a href="{post['url']}" class="blog-entry" data-tags="{",".join(post['tags'])}">
            <div class="blog-date">{post['date']}</div>
            <div class="blog-title">{post['title']}</div>
        </a>'''

    # Write File
    full_html = get_html_structure("Blog | Robert Grinshtein", "blog", content_html)
    with open(BLOG_OUTPUT, 'w', encoding='utf-8') as f: f.write(full_html)
    print(f"✅ Generated {BLOG_OUTPUT}")

# --- 2. BUILD PUBLICATIONS ---
def build_publications():
    if not os.path.exists(PUB_DATA):
        print(f"⚠️ {PUB_DATA} not found. Skipping publications.")
        return

    with open(PUB_DATA, 'r', encoding='utf-8') as f:
        pubs = json.load(f)

    content_html = '<h2>Publications</h2>\n'

    for pub in pubs:
        links_html = ""
        for key, url in pub.get('links', {}).items():
            links_html += f'<a href="{url}">[{key}]</a>\n'

        content_html += f'''
        <div class="pub-item">
            <img src="{pub['image']}" alt="Paper Preview" class="pub-thumb">
            <div class="pub-details">
                <div class="paper-title">{pub['title']}</div>
                <div class="authors">{pub['authors']}</div>
                <div class="venue">{pub['venue']}</div>
                <div class="links">{links_html}</div>
            </div>
        </div>'''

    full_html = get_html_structure("Publications | Robert Grinshtein", "publications", content_html)
    with open(PUB_OUTPUT, 'w', encoding='utf-8') as f: f.write(full_html)
    print(f"✅ Generated {PUB_OUTPUT}")

if __name__ == "__main__":
    build_blog()
    build_publications()