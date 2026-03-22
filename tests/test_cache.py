from skim.cache import get_cached, save


def test_get_cached_miss(tmp_path):
    assert get_cached("2603.10165", "story", tmp_path) is None


def test_save_and_get_cached(tmp_path):
    content = "# Test Summary\nSome content here."
    path = save("2603.10165", "story", content, tmp_path)
    assert path == tmp_path / "2603.10165_story.md"
    assert path.read_text() == content
    assert get_cached("2603.10165", "story", tmp_path) == content


def test_save_creates_output_dir(tmp_path):
    nested = tmp_path / "sub" / "dir"
    save("2603.10165", "deep", "content", nested)
    assert (nested / "2603.10165_deep.md").exists()
