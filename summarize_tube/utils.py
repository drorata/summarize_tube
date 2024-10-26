import json
from typing import Type

from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

from summarize_tube.models import SummeryTube
from summarize_tube.settings import Settings


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
    title_max_len: int = 60,
    description_max_len=150,
    model: str = "gpt-3.5-turbo",
) -> str | None:
    settings = Settings()  # pyright: ignore
    client = OpenAI(
        # This is the default and can be omitted
        api_key=settings.openai_api_key
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

    if summery is None:
        raise ValueError("Summery is None")

    raw_summary_json = json.loads(summery)
    return SummeryTube(**raw_summary_json)
