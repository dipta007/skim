from unittest.mock import MagicMock, patch

from skim.config import Config
from skim.llm import generate_summary, PROMPT_MAP


def test_prompt_map_has_all_types():
    assert "story" in PROMPT_MAP
    assert "deep" in PROMPT_MAP


def test_generate_summary_calls_openai(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake content")

    config = Config(
        api_key="sk-test",
        base_url="https://api.openai.com/v1",
        model="gpt-5.4-nano",
        output_dir=tmp_path / "output",
    )

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "# Summary\nHere is the story."

    with patch("skim.llm.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response

        result = generate_summary(pdf_path, "story", config)

    assert result == "# Summary\nHere is the story."
    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["model"] == "gpt-5.4-nano"
    assert call_kwargs["messages"][0]["role"] == "system"
    assert len(call_kwargs["messages"][0]["content"]) > 0
