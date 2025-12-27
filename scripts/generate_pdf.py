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

    # CSS Styling - Updated for Swiss Style with Smart Page Numbering
    css_string = textwrap.dedent("""\
        /* Define Page Size and Footer Area */
        @page { 
            size: Letter; 
            margin: .75in; 
            @bottom-right {
                content: "Page " counter(page);
                font-family: 'Helvetica Neue', Helvetica, sans-serif;
                font-size: 10pt;
                color: #888888;
            }
        }

        /* Define a 'Title' page type that has no footer */
        @page:first {
            @bottom-right { content: none; }
        }

        /* Named page for TOC - no footer */
        @page toc {
            @bottom-right { content: none; }
        }

        .toc-container {
            page: toc;
        }

        /* Named page for Preface - resets page numbering */
        @page preface {
            counter-reset: page 1;
            @bottom-right {
                content: "Page " counter(page);
                font-family: 'Helvetica Neue', Helvetica, sans-serif;
                font-size: 10pt;
                color: #888888;
            }
        }

        .preface { 
            page: preface;
        }

        body { 
            font-family: 'Helvetica Neue', Helvetica, 'Liberation Sans', 'DejaVu Sans', Arial, sans-serif; 
            font-variant-numeric: lining-nums tabular-nums; 
            line-height: 1.55; 
            color: #333333; 
            font-size: 10pt; 
            -webkit-font-smoothing: antialiased;
        }

        h1, h2, h3, h4 { 
            font-family: 'Helvetica Neue', Helvetica, 'Liberation Sans', 'DejaVu Sans', Arial, sans-serif; 
            color: #111111; 
            margin-top: 1.6em; 
            margin-bottom: 0.6em; 
            font-weight: 700; 
            line-height: 1.2;
        }

        h1 { font-size: 2.2em; letter-spacing: -0.02em; }
        h2 { font-size: 1.6em; border-bottom: 1px solid #eeeeee; padding-bottom: 0.2em; }
        
        code, pre { 
            font-family: 'Menlo', 'Monaco', 'Liberation Mono', 'DejaVu Sans Mono', monospace; 
            font-size: 0.9em; 
            background-color: #f8f8f8; 
        }

        pre { padding: 1.2em; border-radius: 4px; border: 1px solid #e1e4e8; line-height: 1.45; overflow-x: auto; }
        
        .pagebreak { break-before: always; }
        
        img { max-width: 100%; height: auto; display: block; margin: 1.5em auto; }
        
        blockquote { border-left: 3px solid #dddddd; padding: 0 1.2em; color: #666666; margin: 1.5em 0; font-style: italic; }

        /* Swiss Table Styling */
        table { border-collapse: collapse; width: 100%; margin: 2em 0; font-size: 0.95em; }
        table th { font-weight: 700; text-align: left; border-bottom: 2px solid #333333; padding: 10px 12px; }
        table td { padding: 10px 12px; border-bottom: 1px solid #eeeeee; color: #444444; }
        table tr:nth-child(even) { background-color: #fafafa; }
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

