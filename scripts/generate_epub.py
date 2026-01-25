import sys
import os
import re
import mimetypes

try:
    import markdown
    from ebooklib import epub
    EBOOKLIB_AVAILABLE = True
except ImportError:
    EBOOKLIB_AVAILABLE = False

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())


def extract_image_definitions(md_content):
    """Extract image reference definitions from markdown content."""
    definitions = {}
    pattern = re.compile(r'^\[([^\]]+)\]:\s*(.+)$', re.MULTILINE)
    for match in pattern.finditer(md_content):
        ref_name = match.group(1)
        ref_path = match.group(2).strip()
        definitions[ref_name] = ref_path
    return definitions


def generate_epub(md_path, output_epub_path, output_dir, title=None, author=None, cover_image=None):
    if not EBOOKLIB_AVAILABLE:
        print("Error: ebooklib and markdown libraries are not installed.")
        print("Please run: pip install ebooklib markdown lxml")
        sys.exit(1)

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
        sys.exit(1)

    html_ready_md = md_content.replace('{::pagebreak /}', '')

    image_definitions = extract_image_definitions(html_ready_md)

    book = epub.EpubBook()

    if title is None:
        title = os.path.splitext(os.path.basename(md_path))[0]
    if author is None:
        author = "Unknown Author"

    book.set_identifier(f'sloblackswan-{title}')
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    book.add_metadata('DC', 'description', 
        'An exploration of Black Swan events in the context of SRE and SLOs')

    css_content = '''
body {
    font-family: Georgia, serif;
    line-height: 1.6;
    color: #333333;
    margin: 1em;
}
h1, h2, h3, h4, h5, h6 {
    font-family: Helvetica, Arial, sans-serif;
    color: #111111;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    line-height: 1.2;
}
h1 { font-size: 2em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #cccccc; padding-bottom: 0.3em; }
h3 { font-size: 1.2em; }
code, pre {
    font-family: "Courier New", Courier, monospace;
    font-size: 0.9em;
    background-color: #f5f5f5;
}
pre {
    padding: 1em;
    overflow-x: auto;
    border: 1px solid #dddddd;
    border-radius: 4px;
    white-space: pre-wrap;
    word-wrap: break-word;
}
blockquote {
    border-left: 3px solid #cccccc;
    padding-left: 1em;
    margin-left: 0;
    color: #666666;
    font-style: italic;
}
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
table th, table td {
    border: 1px solid #dddddd;
    padding: 8px;
    text-align: left;
}
table th {
    background-color: #f5f5f5;
    font-weight: bold;
}
table tr:nth-child(even) {
    background-color: #fafafa;
}
a {
    color: #0066cc;
    text-decoration: none;
}
'''

    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=css_content.encode('utf-8')
    )
    book.add_item(nav_css)

    image_files = {}
    cover_item = None

    if os.path.isdir(output_dir):
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            if os.path.isfile(filepath):
                mime_type, _ = mimetypes.guess_type(filename)
                if mime_type and mime_type.startswith('image/'):
                    try:
                        with open(filepath, 'rb') as img_file:
                            img_content = img_file.read()

                        img_item = epub.EpubItem(
                            uid=f"img_{filename.replace(' ', '_').replace('.', '_')}",
                            file_name=f"images/{filename}",
                            media_type=mime_type,
                            content=img_content
                        )
                        book.add_item(img_item)
                        image_files[filename] = f"images/{filename}"

                        if cover_image and filename == cover_image:
                            cover_item = (img_content, mime_type, filename)
                        elif cover_item is None and 'SLO-SWAN' in filename:
                            cover_item = (img_content, mime_type, filename)

                    except Exception as e:
                        print(f"Warning: Could not add image {filename}: {e}")

    if cover_item:
        content, mime_type, filename = cover_item
        book.set_cover(f"cover{os.path.splitext(filename)[1]}", content)
        print(f"Cover image set: {filename}")

    full_html = markdown.markdown(html_ready_md, extensions=['extra', 'codehilite', 'tables'])
    full_html = update_image_paths(full_html, image_files, image_definitions)

    sections = re.split(r'(<h1[^>]*>.*?</h1>)', full_html, flags=re.DOTALL)

    chapters = []
    chapter_num = 0

    if sections[0].strip():
        intro_content = sections[0]
        if intro_content.strip():
            intro = epub.EpubHtml(
                title='Introduction',
                file_name='intro.xhtml',
                lang='en'
            )
            intro.set_content(f'''<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Introduction</title><link rel="stylesheet" href="style/nav.css"/></head>
<body>{intro_content}</body>
</html>'''.encode('utf-8'))
            intro.add_item(nav_css)
            book.add_item(intro)
            chapters.append(intro)

    for i in range(1, len(sections), 2):
        if i < len(sections):
            heading_html = sections[i]
            content_html = sections[i + 1] if i + 1 < len(sections) else ""

            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', heading_html, re.DOTALL)
            chapter_title = title_match.group(1).strip() if title_match else f"Chapter {chapter_num + 1}"
            chapter_title = re.sub(r'<[^>]+>', '', chapter_title)

            chapter_num += 1
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=f'chapter_{chapter_num:02d}.xhtml',
                lang='en'
            )
            chapter.set_content(f'''<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{chapter_title}</title><link rel="stylesheet" href="style/nav.css"/></head>
<body>{heading_html}{content_html}</body>
</html>'''.encode('utf-8'))
            chapter.add_item(nav_css)
            book.add_item(chapter)
            chapters.append(chapter)

    if not chapters:
        single_chapter = epub.EpubHtml(
            title=title,
            file_name='content.xhtml',
            lang='en'
        )
        single_chapter.set_content(f'''<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{title}</title><link rel="stylesheet" href="style/nav.css"/></head>
<body>{full_html}</body>
</html>'''.encode('utf-8'))
        single_chapter.add_item(nav_css)
        book.add_item(single_chapter)
        chapters.append(single_chapter)

    book.toc = tuple(chapters)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ['nav'] + chapters

    try:
        epub.write_epub(output_epub_path, book, {})
        print(f"EPUB generated successfully: {output_epub_path}")
    except Exception as e:
        print(f"An unexpected error occurred during EPUB generation: {e}")
        sys.exit(1)


def update_image_paths(html_content, image_files, image_definitions):
    """Update image src attributes to point to EPUB image paths."""

    for ref_name, ref_path in image_definitions.items():
        filename = os.path.basename(ref_path)
        if filename in image_files:
            epub_path = image_files[filename]
            html_content = html_content.replace(f'src="{ref_path}"', f'src="{epub_path}"')
            html_content = html_content.replace(f"src='{ref_path}'", f"src='{epub_path}'")

    for original_name, new_path in image_files.items():
        html_content = html_content.replace(f'src="{original_name}"', f'src="{new_path}"')
        html_content = html_content.replace(f"src='{original_name}'", f"src='{new_path}'")

    return html_content


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_epub.py <md_path> <output_epub_path> <output_dir> [title] [author] [cover_image]")
        sys.exit(1)

    md_path = sys.argv[1]
    output_epub_path = sys.argv[2]
    output_dir = sys.argv[3]
    title = sys.argv[4] if len(sys.argv) > 4 else None
    author = sys.argv[5] if len(sys.argv) > 5 else None
    cover_image = sys.argv[6] if len(sys.argv) > 6 else None

    generate_epub(md_path, output_epub_path, output_dir, title, author, cover_image)
