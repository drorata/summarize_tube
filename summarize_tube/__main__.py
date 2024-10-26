import typer
from loguru import logger

from summarize_tube.settings import Settings
from summarize_tube.utils import (
    gen_summary_from_transcript,
    get_full_transcription,
    struct_summary,
)

settings = Settings()  # pyright: ignore


def main(video_id: str):
    logger.info(f"Start processing of video with ID: {video_id}")
    transcript = get_full_transcription(video_id)
    logger.info(f"Transcript length: {len(transcript)} characters")

    title_and_description = gen_summary_from_transcript(transcript)
    summary = struct_summary(title_and_description)

    logger.info(f"Title and description:\n{summary.model_dump_json(indent=3)}")


def run():
    typer.run(main)
