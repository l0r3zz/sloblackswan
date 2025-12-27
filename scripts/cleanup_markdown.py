import sys
import os

def cleanup_markdown(file_path):
    """
    Strips specific HTML tags that were added for PDF generation
    to make the Markdown file preview-friendly on GitHub.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Remove the 'preface' div wrapper
        content = content.replace('<div class="preface" markdown="1">', '')
        
        # 2. Remove the 'toc-container' div wrapper
        content = content.replace('<div class="toc-container" markdown="1">', '')
        
        # 3. Remove closing divs (verified that these are the only ones in the content)
        content = content.replace('</div>', '')
        
        # 4. Optional: Clean up potential triple newlines created by removing tags
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Successfully removed HTML tags from {file_path}")
        
    except Exception as e:
        print(f"Error cleaning up markdown: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cleanup_markdown.py <md_file_path>")
        sys.exit(1)
        
    cleanup_markdown(sys.argv[1])

