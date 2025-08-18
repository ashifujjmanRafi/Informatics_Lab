def reformat_md_to_txt(input_file, output_file, words_per_line=10):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    reformatted_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:  # preserve blank lines
            reformatted_lines.append("")
            continue

        words = line.split()
        for i in range(0, len(words), words_per_line):
            reformatted_lines.append(" ".join(words[i:i+words_per_line]))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(reformatted_lines))

    print(f"Formatted text saved to {output_file}")


# Example usage
input_md = "researchNote.md"     # your input file
output_txt = "output.txt" # your desired output file
reformat_md_to_txt(input_md, output_txt)
