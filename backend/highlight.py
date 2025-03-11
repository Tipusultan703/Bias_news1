from difflib import ndiff

def highlight_changes(original, rewritten):
    original_words = original.split()
    rewritten_words = rewritten.split()

    diff = list(ndiff(original_words, rewritten_words))
    
    highlighted_text = []
    for word in diff:
        if word.startswith("- "):  # Removed word (biased)
            highlighted_text.append(f"<del style='color:red;'>{word[2:]}</del>")
        elif word.startswith("+ "):  # Added word (neutralized)
            highlighted_text.append(f"<ins style='color:green;'>{word[2:]}</ins>")
        else:
            highlighted_text.append(word[2:])

    return ' '.join(highlighted_text)
