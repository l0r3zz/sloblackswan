import os
import argparse
import datetime
import re
import shutil
import sys
import subprocess
import textwrap

# Try to import weasyprint and markdown
try:
    import markdown
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

# Try to import ebooklib for EPUB generation
try:
    from ebooklib import epub
    EBOOKLIB_AVAILABLE = True
except ImportError:
    EBOOKLIB_AVAILABLE = False

def parse_manifest(manifest_path):
    names = []
    with open(manifest_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith('- '):
            names.append(line[2:].strip())
            
    return names

def process_file(file_path, version, image_defs_list):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Transformation 1: Date
    today = datetime.date.today().strftime("%Y-%m-%d")
    content = content.replace("__$DATE__", today)
    
    # Transformation 2: Version
    content = content.replace("__$VERSION__", version)
    
    # Transformation 3: Extract Image Definitions
    lines = content.splitlines()
    new_lines = []
    
    # Regex to match image definition at start of line
    image_def_pattern = re.compile(r'^\[(.*?)\]:\s*(.*)$')
    
    for line in lines:
        match = image_def_pattern.match(line)
        if match:
            image_defs_list.append(line)
        else:
            new_lines.append(line)
            
    transformed_content = "\n".join(new_lines)
    return transformed_content

def main():
    parser = argparse.ArgumentParser(description="Build book from source markdown files.")
    parser.add_argument("-s", "--source_dir", required=True, help="Source directory containing content")
    parser.add_argument("-d", "--root_dir", required=True, help="Root name of the target directory")
    parser.add_argument("-v", "--version", required=True, help="Version string")
    parser.add_argument("-m", "--manifest", required=True, help="Path to manifest file")
    parser.add_argument("-P", "--pdf", action="store_true", help="Generate PDF output using WeasyPrint")
    parser.add_argument("-E", "--epub", action="store_true", help="Generate EPUB output using ebooklib")
    parser.add_argument("--title", default="SLOs can't catch a Black Swan", help="Book title for EPUB metadata")
    parser.add_argument("--author", default="Geoff White", help="Author name for EPUB metadata")
    
    args = parser.parse_args()
    
    source_dir = os.path.abspath(args.source_dir)
    manifest_path = os.path.abspath(args.manifest)
    
    output_dir_name = f"{args.root_dir}-{args.version}"
    output_dir_path = os.path.abspath(output_dir_name)
    
    if os.path.exists(output_dir_path):
        print(f"Warning: Output directory {output_dir_path} already exists.")
    else:
        os.makedirs(output_dir_path)
        
    output_md_filename = f"{args.root_dir}-{args.version}.md"
    output_md_path = os.path.join(output_dir_path, output_md_filename)
    
    # Initialize/Clear the main output file
    with open(output_md_path, 'w') as f:
        f.write("")
        
    manifest_names = parse_manifest(manifest_path)
    all_image_defs = []
    
    for name in manifest_names:
        target_path = os.path.join(source_dir, name)
        
        # Check if it's a directory
        if os.path.isdir(target_path):
            # It is a directory. Find the .md file.
            md_file = None
            potential_md = os.path.join(target_path, f"{name}.md")
            if os.path.exists(potential_md):
                md_file = potential_md
            else:
                for f in os.listdir(target_path):
                    if f.endswith(".md"):
                        md_file = os.path.join(target_path, f)
                        break
            
            if md_file:
                transformed_content = process_file(md_file, args.version, all_image_defs)
                with open(output_md_path, 'a') as outfile:
                    outfile.write(transformed_content)
                    outfile.write("\n\n")
            else:
                print(f"Error: No .md file found in directory {target_path}")
                pass

            # Copy other files (images)
            for f in os.listdir(target_path):
                full_file_path = os.path.join(target_path, f)
                if os.path.isfile(full_file_path):
                    if not f.endswith(".md"):
                        shutil.copy2(full_file_path, output_dir_path)
        
        # Check if it's a file
        elif os.path.isfile(target_path + ".md"):
             file_path = target_path + ".md"
             transformed_content = process_file(file_path, args.version, all_image_defs)
             with open(output_md_path, 'a') as outfile:
                outfile.write(transformed_content)
                outfile.write("\n\n")
        
        # Check if it's a file with explicit extension in manifest? (Less likely per prompt "section-name")
        elif os.path.isfile(target_path):
             file_path = target_path
             transformed_content = process_file(file_path, args.version, all_image_defs)
             with open(output_md_path, 'a') as outfile:
                outfile.write(transformed_content)
                outfile.write("\n\n")
        
        else:
            # Neither exists
            print(f"Error: Section '{name}' not found as directory or .md file in {source_dir}")
            sys.exit(1)

    # Finalize: Append image definitions
    with open(output_md_path, 'a') as outfile:
        outfile.write("\n---\n\n")
        for img_def in all_image_defs:
            outfile.write(img_def + "\n")
            
    print(f"Build complete. Output in {output_dir_path}")

    # PDF Generation Logic with WeasyPrint
    if args.pdf:
        if not WEASYPRINT_AVAILABLE:
            print("Error: weasyprint and markdown libraries are not installed.")
            print("Please run: pip install weasyprint markdown")
            return

        print("Generating PDF with WeasyPrint...")
        output_pdf_filename = f"{args.root_dir}-{args.version}.pdf"
        output_pdf_path = os.path.join(output_dir_path, output_pdf_filename)
        
        # Read the generated markdown content
        with open(output_md_path, 'r') as f:
            md_content = f.read()
            
        # Replace pagebreaks with HTML div
        # Pattern: {::pagebreak /}
        # Replacement: <div class="pagebreak"></div>
        html_ready_md = md_content.replace("{::pagebreak /}", '<div class="pagebreak"></div>')
        
        # Convert Markdown to HTML
        # Using extensions for tables, code highlighting, etc. might be good, 
        # but sticking to basic for now as per minimal requirements.
        html_content = markdown.markdown(html_ready_md, extensions=['extra', 'codehilite', 'tables'])

        # Fix Image Paths
        # Markdown conversion usually leaves paths relative. We need them absolute for WeasyPrint 
        # (or valid relative to base_url, but absolute is safer given mixed sources).
        # Actually, WeasyPrint base_url handles relative paths if set correctly.
        # We will set base_url to output_dir_path.
        
        # CSS Styling - Updated for GitHub Style (Linux-compatible fonts for GitHub Actions)
        css_string = textwrap.dedent("""\
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
                font-family: "DejaVu Sans", "Liberation Sans", "Noto Sans", Helvetica, Arial, sans-serif;
                font-variant-numeric: lining-nums tabular-nums;
                line-height: 1.55;
                color: #24292f;
                font-size: 10pt;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: "DejaVu Sans", "Liberation Sans", "Noto Sans", Helvetica, Arial, sans-serif;
                font-variant-numeric: lining-nums tabular-nums;
                color: #1f2328;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
                font-weight: 600;
            }
            h1 {
                font-size: 2em;
                border-bottom: 1px solid #d0d7de;
                padding-bottom: 0.3em;
            }
            h2 {
                font-size: 1.3em;
                border-bottom: 1px solid #d0d7de;
                padding-bottom: 0.3em;
            }
            code, pre {
                font-family: "DejaVu Sans Mono", "Liberation Mono", Consolas, monospace;
                font-size: 85%;
            }
            .pagebreak {
                break-before: always;
                page-break-before: always;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            pre {
                background-color: #f6f8fa;
                padding: 16px;
                overflow-x: auto;
                border-radius: 6px;
            }
            blockquote {
                border-left: 0.25em solid #d0d7de;
                padding: 0 1em;
                color: #656d76;
                margin-left: 0;
            }
            table {
                border-spacing: 0;
                border-collapse: collapse;
                display: block;
                width: max-content;
                max-width: 100%;
                overflow: auto;
            }
            table th, table td {
                padding: 6px 13px;
                border: 1px solid #d0d7de;
            }
            table tr {
                background-color: #ffffff;
                border-top: 1px solid #d8dee4;
            }
            table tr:nth-child(2n) {
                background-color: #f6f8fa;
            }
        """).strip()
        
        try:
            # Render PDF
            HTML(string=html_content, base_url=output_dir_path).write_pdf(
                output_pdf_path,
                stylesheets=[CSS(string=css_string)]
            )
            print(f"PDF generated successfully: {output_pdf_path}")
            
        except Exception as e:
            print(f"An unexpected error occurred during PDF generation: {e}")

    # EPUB Generation Logic with ebooklib
    if args.epub:
        if not EBOOKLIB_AVAILABLE:
            print("Error: ebooklib library is not installed.")
            print("Please run: pip install ebooklib lxml")
            return

        print("Generating EPUB with ebooklib...")
        output_epub_filename = f"{args.root_dir}-{args.version}.epub"
        output_epub_path = os.path.join(output_dir_path, output_epub_filename)
        
        # Use the standalone generate_epub script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        generate_epub_script = os.path.join(script_dir, "generate_epub.py")
        
        if os.path.exists(generate_epub_script):
            try:
                result = subprocess.run(
                    [sys.executable, generate_epub_script, output_md_path, output_epub_path, 
                     output_dir_path, args.title, args.author],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(result.stdout.strip())
                else:
                    print(f"EPUB generation failed: {result.stderr}")
            except Exception as e:
                print(f"An unexpected error occurred during EPUB generation: {e}")
        else:
            print(f"Error: generate_epub.py not found at {generate_epub_script}")

if __name__ == "__main__":
    main()
