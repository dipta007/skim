from skim.viewer import _sanitize, _extract_math


def test_sanitize_normal_text():
    assert _sanitize("hello world") == "hello world"


def test_sanitize_unicode():
    assert _sanitize("α + β") == "α + β"


def test_sanitize_surrogates():
    text = "hello \ud800 world"
    result = _sanitize(text)
    assert "hello" in result
    assert "world" in result


def test_extract_math_inline():
    content = r"The value \(x + 1\) is positive."
    processed, blocks = _extract_math(content)
    assert len(blocks) == 1
    assert blocks[0]["math"] == "x + 1"
    assert blocks[0]["display"] is False
    assert "%%MATH0%%" in processed


def test_extract_math_display():
    content = "Before\n\\[\nx^2 + y^2 = 1\n\\]\nAfter"
    processed, blocks = _extract_math(content)
    assert len(blocks) == 1
    assert "x^2 + y^2 = 1" in blocks[0]["math"]
    assert blocks[0]["display"] is True


def test_extract_math_dollar_inline():
    content = "The cost is $n^2$ complexity."
    processed, blocks = _extract_math(content)
    assert len(blocks) == 1
    assert blocks[0]["math"] == "n^2"
    assert blocks[0]["display"] is False


def test_extract_math_dollar_display():
    content = "Formula:\n$$E = mc^2$$\nDone."
    processed, blocks = _extract_math(content)
    assert len(blocks) == 1
    assert "E = mc^2" in blocks[0]["math"]
    assert blocks[0]["display"] is True


def test_extract_math_ampersand_escaped():
    content = "\\[\n\\text{objects & actions}\n\\]"
    processed, blocks = _extract_math(content)
    assert len(blocks) == 1
    assert r"\&" in blocks[0]["math"]


def test_extract_math_no_math():
    content = "No math here, just text."
    processed, blocks = _extract_math(content)
    assert len(blocks) == 0
    assert processed == content


def test_extract_math_multiple():
    content = r"Given \(x\) and \(y\), we have \(z\)."
    processed, blocks = _extract_math(content)
    assert len(blocks) == 3
    assert blocks[0]["math"] == "x"
    assert blocks[1]["math"] == "y"
    assert blocks[2]["math"] == "z"
