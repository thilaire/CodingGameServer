from wcwidth import wcswidth


def leftPadding(s: str, n: int):
    """perform left padding, even with emojis"""
    return " " * (n - wcswidth(s)) + s

