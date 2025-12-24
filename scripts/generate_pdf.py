import sys
import os
import textwrap

# Try to import weasyprint and markdown with error handling
try:
    import markdown
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

# Ensure we can import from the same directory if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Or from the root if called from there
sys.path.append(os.getcwd())

def generate_pdf(md_path, output_pdf_path, output_dir):
    if not WEASYPRINT_AVAILABLE:
        print("Error: weasyprint and markdown libraries are not installed.")
        print("Please run: pip install weasyprint markdown")
        sys.exit(1)

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
        sys.exit(1)

    # Replace pagebreak syntax with HTML
    html_ready_md = md_content.replace('{::pagebreak /}', '<div class="pagebreak"></div>')
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(html_ready_md, extensions=['extra', 'codehilite', 'tables'])

    # CSS Styling - Updated for GitHub Style (Linux-compatible fonts for GitHub Actions)
    css_string = textwrap.dedent("""\
        @page { size: Letter; margin: 1in; }
        body { font-family: 'DejaVu Sans', 'Liberation Sans', 'Noto Sans', Helvetica, Arial, sans-serif; font-variant-numeric: lining-nums tabular-nums; line-height: 1.5; color: #24292f; font-size: 16px; }
        h1, h2, h3, h4, h5, h6 { font-family: 'DejaVu Sans', 'Liberation Sans', 'Noto Sans', Helvetica, Arial, sans-serif; font-variant-numeric: lining-nums tabular-nums; color: #1f2328; margin-top: 1.5em; margin-bottom: 0.5em; font-weight: 600; }
        h1 { font-size: 2em; border-bottom: 1px solid #d0d7de; padding-bottom: 0.3em; }
        h2 { font-size: 1.5em; border-bottom: 1px solid #d0d7de; padding-bottom: 0.3em; }
        code, pre { font-family: 'DejaVu Sans Mono', 'Liberation Mono', Consolas, monospace; font-size: 85%; }
        .pagebreak { break-before: always; page-break-before: always; }
        img { max-width: 100%; height: auto; }
        pre { background-color: #f6f8fa; padding: 16px; overflow-x: auto; border-radius: 6px; }
        blockquote { border-left: 0.25em solid #d0d7de; padding: 0 1em; color: #656d76; margin-left: 0; }
        table { border-spacing: 0; border-collapse: collapse; display: block; width: max-content; max-width: 100%; overflow: auto; }
        table th, table td { padding: 6px 13px; border: 1px solid #d0d7de; }
        table tr { background-color: #ffffff; border-top: 1px solid #d8dee4; }
        table tr:nth-child(2n) { background-color: #f6f8fa; }
    """).strip()

    try:
        # Render PDF
        HTML(string=html_content, base_url=output_dir).write_pdf(
            output_pdf_path,
            stylesheets=[CSS(string=css_string)]
        )
        print(f"PDF generated successfully: {output_pdf_path}")
    except Exception as e:
        print(f"An unexpected error occurred during PDF generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_pdf.py <md_path> <output_pdf_path> <output_dir>")
        sys.exit(1)
    
    generate_pdf(sys.argv[1], sys.argv[2], sys.argv[3])

