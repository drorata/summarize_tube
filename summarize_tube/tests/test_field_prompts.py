from summarize_tube.models import SummeryTube, configure_prompts_of_fields


def test_main():
    prompt = SummeryTube.construct_prompt_for_fields_as_dict()

    assert prompt == {
        "title": "A title of at most 60 characters based on the transcript",
        "description": "A description for the video of at most 250 characters based on the transcript",
        "hashtags": "A list of 12 hashtags recommended for the video",
    }


def test_adjusted_prompts():
    configure_prompts_of_fields(
        title="My title",
        description="My description",
        hashtags="My hashtags",
    )

    prompt = SummeryTube.construct_prompt_for_fields_as_dict()

    assert prompt == {
        "title": "My title",
        "description": "My description",
        "hashtags": "My hashtags",
    }
