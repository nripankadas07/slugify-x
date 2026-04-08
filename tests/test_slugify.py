"""Tests for slugify-x.

Naming convention: test_[unit]_[scenario]_[expected_result]
"""
import pytest

from slugify_x import SlugifyError, slugify


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_slugify_simple_ascii_returns_lowercase_slug() -> None:
    assert slugify("Hello World") == "hello-world"


def test_slugify_already_lowercase_unchanged() -> None:
    assert slugify("hello-world") == "hello-world"


def test_slugify_multiple_spaces_collapsed_to_one_separator() -> None:
    assert slugify("hello   world") == "hello-world"


def test_slugify_mixed_punctuation_stripped() -> None:
    assert slugify("hello, world!") == "hello-world"


def test_slugify_numbers_preserved() -> None:
    assert slugify("Python 3 is great") == "python-3-is-great"


def test_slugify_custom_separator_underscore() -> None:
    assert slugify("hello world", separator="_") == "hello_world"


def test_slugify_lowercase_false_preserves_case() -> None:
    assert slugify("Hello World", lowercase=False) == "Hello-World"


def test_slugify_accented_chars_transliterated() -> None:
    result = slugify("café résumé")
    assert result == "cafe-resume"


def test_slugify_german_umlauts_transliterated() -> None:
    # ß has no ASCII NFKD decomposition, so it is dropped entirely.
    # ü → "u" via NFKD; ß → dropped → "strae"
    result = slugify("Über straße")
    assert result == "uber-strae"


def test_slugify_max_length_truncates_output() -> None:
    result = slugify("hello world foo bar", max_length=10)
    assert len(result) <= 10


def test_slugify_max_length_does_not_end_with_separator() -> None:
    result = slugify("hello world foo bar", max_length=10)
    assert not result.endswith("-")


def test_slugify_allow_unicode_true_retains_unicode_word_chars() -> None:
    result = slugify("héllo wörld", allow_unicode=True)
    # Non-ASCII word chars should be preserved when allow_unicode=True
    assert "h" in result
    assert "-" in result


def test_slugify_already_clean_slug_unchanged() -> None:
    assert slugify("clean-slug-123") == "clean-slug-123"


def test_slugify_leading_trailing_separators_stripped() -> None:
    assert slugify("  hello world  ") == "hello-world"


def test_slugify_tabs_and_newlines_treated_as_whitespace() -> None:
    assert slugify("hello\tworld\nfoo") == "hello-world-foo"


# ---------------------------------------------------------------------------
# Edge cases — empty / whitespace / special-only
# ---------------------------------------------------------------------------


def test_slugify_empty_string_returns_empty_string() -> None:
    assert slugify("") == ""


def test_slugify_only_spaces_returns_empty_string() -> None:
    assert slugify("   ") == ""


def test_slugify_only_punctuation_returns_empty_string() -> None:
    assert slugify("!@#$%^&*()") == ""


def test_slugify_only_dashes_returns_empty_string() -> None:
    assert slugify("---") == ""


def test_slugify_single_char_returns_single_char() -> None:
    assert slugify("a") == "a"


def test_slugify_single_digit_returns_single_digit() -> None:
    assert slugify("7") == "7"


# ---------------------------------------------------------------------------
# Edge cases — max_length
# ---------------------------------------------------------------------------


def test_slugify_max_length_zero_returns_empty_string() -> None:
    assert slugify("hello world", max_length=0) == ""


def test_slugify_max_length_larger_than_slug_unchanged() -> None:
    assert slugify("hi", max_length=100) == "hi"


def test_slugify_max_length_exact_fit() -> None:
    # "hello-world" is 11 chars; max_length=11 should return it intact
    assert slugify("hello world", max_length=11) == "hello-world"


def test_slugify_max_length_cuts_cleanly_between_words() -> None:
    # "hello-world" → max_length=5 should give "hello" (not "hello-")
    result = slugify("hello world", max_length=5)
    assert result == "hello"


def test_slugify_max_length_strips_trailing_separator_after_cut() -> None:
    # "hello-world"[:6] = "hello-" → trailing separator must be stripped
    result = slugify("hello world", max_length=6)
    assert result == "hello"


# ---------------------------------------------------------------------------
# Edge cases — allow_unicode
# ---------------------------------------------------------------------------


def test_slugify_allow_unicode_false_strips_non_ascii() -> None:
    result = slugify("hello 世界", allow_unicode=False)
    assert result == "hello"


def test_slugify_allow_unicode_true_keeps_cjk_chars() -> None:
    result = slugify("hello 世界", allow_unicode=True)
    assert "世界" in result


# ---------------------------------------------------------------------------
# Error cases — invalid input types
# ---------------------------------------------------------------------------


def test_slugify_none_input_raises_slugify_error() -> None:
    with pytest.raises(SlugifyError, match="str"):
        slugify(None)  # type: ignore[arg-type]


def test_slugify_integer_input_raises_slugify_error() -> None:
    with pytest.raises(SlugifyError, match="str"):
        slugify(42)  # type: ignore[arg-type]


def test_slugify_list_input_raises_slugify_error() -> None:
    with pytest.raises(SlugifyError, match="str"):
        slugify(["hello"])  # type: ignore[arg-type]


def test_slugify_invalid_max_length_negative_raises_slugify_error() -> None:
    with pytest.raises(SlugifyError, match="max_length"):
        slugify("hello", max_length=-1)


def test_slugify_invalid_separator_raises_slugify_error() -> None:
    # Separator must not be a word character
    with pytest.raises(SlugifyError, match="separator"):
        slugify("hello", separator="a")


def test_slugify_separator_cannot_be_empty_string() -> None:
    # Empty separator joins everything: "hello world" → "helloworld"
    # This is allowed — no error expected
    result = slugify("hello world", separator="")
    assert result == "helloworld"
