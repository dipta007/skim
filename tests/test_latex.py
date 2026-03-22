import pytest
from skim.latex import latex_to_unicode


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (r"R \in \{0, 1\}", "R ∈ {0, 1}"),
        (r"3 \times 4", "3 × 4"),
        (r"x \geq 0", "x ≥ 0"),
        (r"x \leq 10", "x ≤ 10"),
        (r"\sum r_i", "∑ r_i"),
        (r"\pi_\theta", "π_θ"),
        (r"\(R = 0\)", "R = 0"),
        (r"\[R = 0\]", "R = 0"),
        (r"\alpha + \beta", "α + β"),
        (r"A \neq B", "A ≠ B"),
        (r"a \cdot b", "a · b"),
        (r"\infty", "∞"),
        (r"\rightarrow", "→"),
        (r"\leftarrow", "←"),
        ("no latex here", "no latex here"),
    ],
)
def test_latex_to_unicode(input_str, expected):
    assert latex_to_unicode(input_str) == expected
