import pytest

from summarize_tube.models import SummeryTube


@pytest.mark.parametrize(
    "hashtags",
    [
        ["a", "b", "c"],
        ["a", "b", "#c"],
        "a b c",
        "a b #c",
        "a, b, c",
        "a, b, #c",
    ],
)
def test_asserting_hashtags_is_a_list_each_item_prefixed_with_hash(hashtags) -> None:
    print(hashtags)
    expected_res = SummeryTube(title="a", description="b", hashtags=hashtags)
    assert expected_res.hashtags == ["#a", "#b", "#c"]
