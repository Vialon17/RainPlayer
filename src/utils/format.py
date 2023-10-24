import re

def get_pure_string(target: str) -> str:
    bracket_pattern = r"\([^)]*\)|\（[^)]*\）"
    return re.sub(bracket_pattern, '', target)