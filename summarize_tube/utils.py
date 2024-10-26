from openai import OpenAI
import json
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

    prompt = (
        f"""You are a marketing and youtube specialist.
    You will be given a transcript of a youtube video.
    Based on the transcription you must generate the following details:

    - a title of at most {title_max_len} characters
    - a description for the video of at most {description_max_len} characters
    - a list of 12 hashtags recommended for the video

    """
        + """
    You should only a valid json object of the following schema:
    {
        "title": <generated title>,
        "description": <generated description>,
        "hashtags": <list of comma separated suggested hashtags>
    }
    """
        + f"""
    The transcript is:

    {transcript}
    """
    )

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

    hashtags = [
        "#" + x.strip() for x in raw_summary_json["hashtags"].split("#") if x != ""
    ]
    res_dict_final = {}
    for k, v in raw_summary_json.items():
        if k != "hashtags":
            res_dict_final[k] = v
    res_dict_final["hashtags"] = hashtags

    return SummeryTube(**res_dict_final)
