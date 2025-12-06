import os
import argparse
import datetime
import re
import shutil
import sys

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
                # "report an error to the user and exit" - we can exit or continue. 
                # Prompt says "report an error to the user and exit" in context of "if neither name exist". 
                # But here the directory exists but no md file. It's safer to probably warn or error.
                # I'll stick to warning here to match previous behavior unless strict error requested.
                # Re-reading prompt: "if neiter name exist, report an error to the user and exit."
                # This refers to finding the section itself. If directory exists, section exists.
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

if __name__ == "__main__":
    main()
