from skim.cache import get_cached, save


def test_get_cached_miss(tmp_path):
    assert get_cached("2603.10165", "story", "abc123", tmp_path) is None


def test_save_and_get_cached(tmp_path):
    content = "# Test Summary\nSome content here."
    path = save("2603.10165", "story", "abc123", content, tmp_path)
    assert path == tmp_path / "2603.10165_story_abc123.md"
    assert path.read_text() == content
    assert get_cached("2603.10165", "story", "abc123", tmp_path) == content


def test_save_creates_output_dir(tmp_path):
    nested = tmp_path / "sub" / "dir"
    save("2603.10165", "deep", "def456", "content", nested)
    assert (nested / "2603.10165_deep_def456.md").exists()


def test_different_hash_is_cache_miss(tmp_path):
    save("2603.10165", "story", "hash_v1", "old content", tmp_path)
    assert get_cached("2603.10165", "story", "hash_v1", tmp_path) == "old content"
    assert get_cached("2603.10165", "story", "hash_v2", tmp_path) is None
