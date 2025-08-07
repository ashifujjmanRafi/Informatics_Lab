#!/usr/bin/env python3
"""
Script to process research notes and limit each line to 12 words maximum.
"""

def process_file(input_file, output_file, max_words=12):
    """
    Process the input file and limit each line to max_words words.
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output file
        max_words (int): Maximum number of words per line
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            processed_lines.append('')
            continue
        
        # Check if line starts with ## (date headers)
        if line.startswith('##'):
            processed_lines.append(line)
            continue
        
        # Check if line starts with - [ ] or - [x] (task list items)
        if line.strip().startswith('- [') and ']' in line:
            # Keep the task list format intact
            processed_lines.append(line)
            continue
        
        # Check if line contains markdown formatting
        if any(marker in line for marker in ['**', '*', '`', '[', ']', '<', '>', '![']):
            # Keep markdown formatted lines intact
            processed_lines.append(line)
            continue
        
        # Process regular text lines
        words = line.split()
        if len(words) <= max_words:
            processed_lines.append(line)
        else:
            # Split into chunks of max_words
            for i in range(0, len(words), max_words):
                chunk = words[i:i + max_words]
                processed_lines.append(' '.join(chunk))
    
    # Write processed content to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_lines))
    
    print(f"Processing complete! Output saved to: {output_file}")

if __name__ == "__main__":
    input_file = "Reserch_note/researchNote.md"
    output_file = "Reserch_note/researchNote_processed.md"
    
    try:
        process_file(input_file, output_file, max_words=12)
        print("File processed successfully!")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    except Exception as e:
        print(f"Error processing file: {e}") 