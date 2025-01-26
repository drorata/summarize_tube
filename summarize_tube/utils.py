import json
from typing import Type
from urllib.parse import parse_qs, urlparse

from loguru import logger
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

from summarize_tube.models import SummeryTube
from summarize_tube.settings import Settings


def get_video_id(video_url) -> str:
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US

    Original code from: https://stackoverflow.com/a/7936523/671013
    """
    query = urlparse(video_url)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            p = parse_qs(query.query)
            return p["v"][0]
        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]

    raise ValueError("Invalid YouTube URL")


def get_full_transcription(video_id: str, language: str = "en") -> str:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript([language])
    res = ""
    for t in transcript.fetch():
        res += t["text"] + " "

    return res


def construct_prompt(model: Type[SummeryTube], transcript: str) -> str:
    intro = """You are a marketing and youtube specialist.
    You will be given a transcript of a youtube video.
    Based on the transcription you must generate the following fields in a
    JSON format:

    """
    fields_prompts = json.dumps(SummeryTube.construct_prompt_for_fields_as_dict())

    return (
        intro
        + "\n"
        + fields_prompts
        + f"""

    The transcript is:

    {transcript}
"""
    )


def gen_summary_from_transcript(
    transcript: str,
    model: str = "gpt-4o",
) -> str | None:
    settings = Settings()  # pyright: ignore
    client = OpenAI(
        # # Using OpenAI
        # api_key=settings.openai_api_key
        # Using GitHub Models
        api_key=settings.github_token,
        base_url="https://models.inference.ai.azure.com",
    )

    prompt = construct_prompt(SummeryTube, transcript=transcript)

    chat_completion = client.chat.completions.create(
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        n=1,
        temperature=0.2,
    )

    return chat_completion.choices[0].message.content


def struct_summary(summery: str | None) -> SummeryTube:
    logger.info(f"About to structure the following summary:\n{summery}")
    if summery is None:
        raise ValueError("Summery is None")

    raw_summary_json = json.loads(summery)
    return SummeryTube(**raw_summary_json)
