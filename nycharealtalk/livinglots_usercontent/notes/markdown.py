import re

import bleach
from bleach.callbacks import nofollow, target_blank
from html5lib.tokenizer import HTMLTokenizer
import markdown2


single_newline_pattern = re.compile(r'([^\n])(?:\n)([^\n])')


def text_to_markdown(text):
    # Convert text that is in Markdown to HTML
    text = markdown2.markdown(text, extras=['code-friendly', 'cuddled-lists', 'nofollow',])

    # Convert single newlines to breaks
    text = single_newline_pattern.sub(r'\1<br>\2', text)

    # Catch links that were not converted since they were not in a proper
    # Markdown format
    return bleach.linkify(text, [nofollow, target_blank,], parse_email=True,
                          tokenizer=HTMLTokenizer)
