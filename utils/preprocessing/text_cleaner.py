import re

def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"@\w+", "", text)     # remove mentions
    text = re.sub(r"#\w+", "", text)     # remove hashtags
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # remove special chars
    return text.strip().lower()
