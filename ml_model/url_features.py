import re
from urllib.parse import urlparse

def extract_url_features(url: str) -> dict:
    """Extract features matching the training dataset columns."""
    
    features = {
        "url_length": len(url),
        "n_dots": url.count('.'),
        "n_hypens": url.count('-'),  # Note: typo in CSV column name
        "n_underline": url.count('_'),
        "n_slash": url.count('/'),
        "n_questionmark": url.count('?'),
        "n_equal": url.count('='),
        "n_at": url.count('@'),
        "n_and": url.count('&'),
        "n_exclamation": url.count('!'),
        "n_space": url.count(' '),
        "n_tilde": url.count('~'),
        "n_comma": url.count(','),
        "n_plus": url.count('+'),
        "n_asterisk": url.count('*'),
        "n_hastag": url.count('#'),  # Note: typo in CSV column name
        "n_dollar": url.count('$'),
        "n_percent": url.count('%'),
        "n_redirection": url.count('//') - 1 if url.count('//') > 1 else 0,  # Extra '//' beyond protocol
    }
    return features