import random
import re

def clean_result(text):
    """Clean the result by removing unnecessary newlines and formatting the text based on `---` for new paragraphs."""
    if isinstance(text, str):
        # Remove all instances of '#' and '**'
        cleaned_text = text.replace('#', '').replace('**', '')

        # Ensure "Overview" starts from a new line (replacing it with a space for now, since we'll remove \n)
        cleaned_text = cleaned_text.replace("Daily Overview", "Daily Overview: ")

        # Replace all `\n` with spaces to remove line breaks completely
        cleaned_text = cleaned_text.replace('\n', ' ').replace('  ', ' ')  # Replace double spaces after removal

        # Split the cleaned text by the `---` pattern (indicating new days or sections)
        parts = re.split(r'(---)', cleaned_text)

        # Group the parts back together, ensuring that each section after `---` starts as a new paragraph
        paragraphs = []
        current_paragraph = ""
        for part in parts:
            if part == "---":
                if current_paragraph:
                    paragraphs.append(current_paragraph.strip())  # Append current paragraph before new section
                current_paragraph = ""  # Reset paragraph after `---`
            else:
                # Handle cases where "Day" is at the beginning of a new section
                if current_paragraph:
                    current_paragraph += " " + part.strip()
                else:
                    current_paragraph = part.strip()

        if current_paragraph:
            paragraphs.append(current_paragraph.strip())

        # Join paragraphs with double newlines, but ensure no extra newline comes before a new "Day"
        final_output = '\n\n'.join(paragraphs).replace('\n\n---', '---')  # Ensure no extra newline before "Day"

        return final_output.strip()
    
    return text
