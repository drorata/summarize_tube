import pytest

from summarize_tube.utils import get_video_id


@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://youtu.be/SA2iWivDJiE", "SA2iWivDJiE"),
        ("http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu", "_oPAwA_Udwc"),
        ("http://www.youtube.com/embed/SA2iWivDJiE", "SA2iWivDJiE"),
        ("http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US", "SA2iWivDJiE"),
    ],
)
def test_main(url, expected):
    assert get_video_id(url) == expected
