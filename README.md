# slugify-x

**Unicode-aware URL slug generator. Zero runtime dependencies.**

Converts arbitrary text into clean, URL-safe slugs with configurable
separators, optional Unicode preservation, and safe truncation.

---

## Install

```bash
pip install slugify-x
```

Or from source:

```bash
git clone https://github.com/nripankadas07/slugify-x.git
cd slugify-x
pip install -e .
```

---

## Usage

```python
from slugify_x import slugify

slugify("Hello, World!")          # "hello-world"
slugify("café résumé")            # "cafe-resume"
slugify("Python 3 is great")      # "python-3-is-great"
slugify("hello world", separator="_")   # "hello_world"
slugify("Hello World", lowercase=False) # "Hello-World"
slugify("a very long title here", max_length=12)  # "a-very-long"
slugify("héllo wörld", allow_unicode=True)         # "héllo-wörld"
```

---

## API Reference

### `slugify(text, *, separator="-", lowercase=True, max_length=None, allow_unicode=False) -> str`

Convert *text* into a URL-safe slug.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | — | Input string to slugify. |
| `separator` | `str` | `"-"` | Token delimiter. Must be a single non-word character or `""`. |
| `lowercase` | `bool` | `True` | Lowercase all tokens before joining. |
| `max_length` | `int \| None` | `None` | Truncate result to at most this many characters (no trailing separator). |
| `allow_unicode` | `bool` | `False` | Preserve non-ASCII word characters instead of transliterating to ASCII. |

**Returns** the slug string, which may be `""` if the input contains no
word characters after processing.

**Raises** `SlugifyError` (a `ValueError` subclass) when:
- `text` is not a `str`
- `max_length` is negative
- `separator` is a word character (letter, digit, or underscore)

### `SlugifyError`

A `ValueError` subclass raised for invalid arguments.

---

## Running Tests

```bash
pip install pytest
pytest
```

Expected output:

```
================================ N passed in Xs ================================
```

Coverage report (requires `pytest-cov`):

```bash
pytest --cov=slugify_x --cov-report=term-missing
```

---

## License

MIT © 2026 Nripanka Das
