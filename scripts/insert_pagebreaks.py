#!/usr/bin/env python3
"""
Markdown Pagebreak Inserter

Inserts '{::pagebreak /}' before ## headers, excluding those inside code blocks.
Code blocks are delimited by triple backticks (```).

Author: Geoff White
"""
import argparse
import sys
from pathlib import Path

def insert_pagebreaks(content: str, force_first: bool = False) -> str:
    """
    Insert pagebreaks before ## headers, but not inside code blocks.
    Preserves line ending style and avoids duplicate pagebreaks.

    Args:
        content: The markdown file content as a string
        force_first: If True, insert pagebreak even before the first header

    Returns:
        Modified content with pagebreaks inserted
    """
    lines = content.splitlines(keepends=True)
    result = []
    in_code_block = False
    
    # Detect line ending style from the original content
    # Check the first line that has a line ending, or default to \n
    line_ending = '\n'
    for line in lines:
        if line.endswith('\r\n'):
            line_ending = '\r\n'
            break
        elif line.endswith('\r'):
            line_ending = '\r'
            break
        elif line.endswith('\n'):
            line_ending = '\n'
            break
    
    for i, line in enumerate(lines):
        # Check if line starts with ``` at column 0 (not indented)
        if line.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        # Check if line starts with exactly ## (level-2 header) at column 0
        # Must start with ## followed by a space or end of line (not ### or deeper)
        if not in_code_block and line.startswith('##') and (len(line) < 3 or line[2] != '#'):
            # Look back through blank lines to find the last non-blank line
            has_existing_pagebreak = False
            has_prior_content = False
            for j in range(len(result) - 1, -1, -1):
                last_line = result[j].strip()
                if last_line == '{::pagebreak /}':
                    has_existing_pagebreak = True
                    break
                elif last_line:  # Non-blank line that's not a pagebreak
                    has_prior_content = True
                    break
            
            # Skip pagebreak if this is the first header (no prior content)
            if has_existing_pagebreak:
                result.append(line)
            elif has_prior_content or force_first:
                # Insert pagebreak if there's prior content OR if force_first is requested
                result.append(f'{{::pagebreak /}}{line_ending}')
                result.append(line)
            else:
                # First header in document - no pagebreak needed
                result.append(line)
        else:
            result.append(line)
    return ''.join(result)

def process_file(input_path: Path, output_path: Path = None, overwrite: bool = False, force_first: bool = False) -> None:
    """
    Process a markdown file to insert pagebreaks.

    Args:
        input_path: Path to input markdown file
        output_path: Path to output file (optional)
        overwrite: If True, overwrite the original file
        force_first: If True, insert pagebreak even before the first header
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Process the content
    modified_content = insert_pagebreaks(content, force_first=force_first)

    # Determine output path
    if overwrite:
        out_path = input_path
    elif output_path:
        out_path = output_path
    else:
        # Default: add _processed before the extension
        out_path = input_path.parent / f"{input_path.stem}_processed{input_path.suffix}"

    # Write the output file
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Successfully processed: {input_path}")
        print(f"Output written to: {out_path}")
    except Exception as e:
        print(f"Error writing to {out_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Insert pagebreaks before ## headers in markdown files, excluding code blocks.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.md                    # Creates input_processed.md
  %(prog)s input.md -o output.md       # Creates output.md
  %(prog)s input.md --overwrite        # Overwrites input.md
        """
    )

    parser.add_argument('input_file', type=Path, help='Input markdown file')
    parser.add_argument('-o', '--output', type=Path, help='Output file path (default: input_processed.md)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite the input file')
    parser.add_argument('--force-first', action='store_true', help='Force pagebreak before the first header even if it is at the start of the file')

    args = parser.parse_args()

    # Validate input file exists
    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Check for conflicting arguments
    if args.overwrite and args.output:
        print("Error: Cannot use both --overwrite and --output", file=sys.stderr)
        sys.exit(1)

    # Process the file
    process_file(args.input_file, args.output, args.overwrite, args.force_first)

if __name__ == '__main__':
    main()
