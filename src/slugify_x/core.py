"""Core slug generation logic for slugify-x."""

import re
import unicodedata


class SlugifyError(ValueError):
    """Raised when slugify receives invalid arguments."""


# Matches a word character (letter, digit, underscore) in ASCII mode.
_WORD_CHAR_ASCII = re.compile(r"[a-zA-Z0-9]+")
# Matches a word character in Unicode mode (letters, digits, marks).
_WORD_CHAR_UNICODE = re.compile(r"[\w]+", re.UNICODE)
# Separator chars that are not word characters (safe as field delimiters).
_SAFE_SEPARATOR = re.compile(r"^[^a-zA-Z0-9]$|^$")


def _validate_arguments(
    text: object,
    separator: str,
    max_length: int | None,
) -> None:
    """Raise SlugifyError for invalid call arguments."""
    if not isinstance(text, str):
        raise SlugifyError(
            f"slugify() expects a str, got {type(text).__name__!r}"
        )
    if max_length is not None and max_length < 0:
        raise SlugifyError(
            f"max_length must be a non-negative integer, got {max_length!r}"
        )
    # separator must be a single non-word char OR the empty string
    if separator != "" and not _SAFE_SEPARATOR.match(separator):
        raise SlugifyError(
            f"separator must be a single non-word character or '', "
            f"got {separator!r}"
        )


def _transliterate(text: str) -> str:
    """Return an ASCII approximation via Unicode NFKD decomposition."""
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("ascii", errors="ignore").decode("ascii")


def _extract_tokens(text: str, allow_unicode: bool) -> list[str]:
    """Split *text* into word tokens, optionally keeping Unicode chars."""
    if allow_unicode:
        return _WORD_CHAR_UNICODE.findall(text)
    ascii_text = _transliterate(text)
    return _WORD_CHAR_ASCII.findall(ascii_text)


def _apply_max_length(slug: str, max_length: int, separator: str) -> str:
    """Truncate *slug* to at most *max_length* characters.

    Truncation never leaves a trailing separator.
    """
    if max_length == 0:
        return ""
    truncated = slug[:max_length]
    if separator and truncated.endswith(separator):
        truncated = truncated[: -len(separator)]
    return truncated


def _build_slug(
    tokens: list[str],
    separator: str,
    lowercase: bool,
    max_length: int | None,
) -> str:
    """Join validated tokens into a slug and apply optional constraints."""
    if lowercase:
        tokens = [token.lower() for token in tokens]
    slug = separator.join(tokens)
    if max_length is not None:
        slug = _apply_max_length(slug, max_length, separator)
    return slug


def slugify(
    text: str,
    separator: str = "-",
    lowercase: bool = True,
    max_length: int | None = None,
    allow_unicode: bool = False,
) -> str:
    """Convert *text* to a URL-safe slug.

    Raises SlugifyError if *text* is not a str, *max_length* is negative,
    or *separator* is a word character (letter, digit, underscore).
    Empty separator ``""`` is allowed and joins tokens with no delimiter.
    """
    _validate_arguments(text, separator, max_length)
    tokens = _extract_tokens(text, allow_unicode)
    return _build_slug(tokens, separator, lowercase, max_length)
