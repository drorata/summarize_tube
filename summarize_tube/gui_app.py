import streamlit as st
from loguru import logger

from summarize_tube import utils
from summarize_tube.models import SummeryTube, configure_prompts_of_fields

st.sidebar.write(
    """
    # Summarize YouTube Videos

    Generate a title, description, and tags for a YouTube video.
    All you need to do is paste the video ID below and click continue.

    * Made by Dr. Dror
    * Code available [here](https://github.com/drorata/summarize_tube)
    * Be, nice - don't exploit the OpenAI API too much!
    * Say hello over [LinkedIn](https://www.linkedin.com/in/atariah/)
    """
)

# Initialize session state for each step
if "video_id" not in st.session_state:
    st.session_state.video_id = ""
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "transcript_confirmed" not in st.session_state:
    st.session_state.transcript_confirmed = False
if "prompt_confirmed" not in st.session_state:
    st.session_state.prompt_confirmed = False

# Step 1: Input YouTube Video ID
video_id = st.text_input(
    "Enter YouTube Video ID",
    st.session_state.video_id,
    help="Paste here the ID of the YouTube video you want to summarize",
)

if video_id:
    st.session_state.video_id = video_id
    st.video(data=f"https://www.youtube.com/watch?v={video_id}")
    if st.button("🚀 Click here if this is the video you want to process"):
        logger.info(f"Processing video with ID: {video_id}")
        st.write("Fetching transcript...")

        # Fetch the transcript if it hasn't been fetched yet
        if st.session_state.transcript is None:
            try:
                st.session_state.transcript = utils.get_full_transcription(video_id)
            except Exception as e:
                st.error(
                    "Failed to retrieve the transcript. "
                    "Please check the video ID and try again."
                )
                logger.error(
                    f"Error retrieving transcript for video ID {video_id}: {e}"
                )
                st.stop()

# Step 2: Confirm Transcript
if st.session_state.transcript:
    st.text_area(
        "Transcript",
        st.session_state.transcript,
        height=200,
        disabled=True,
    )
    if st.button("🚀 Click here if the transcript is correct"):
        st.session_state.transcript_confirmed = True

# Step 3: Configure prompts of the fields
if st.session_state.transcript_confirmed:

    st.session_state.fields_prompt_dict = (
        SummeryTube.construct_prompt_for_fields_as_dict()
    )
    for k in st.session_state.fields_prompt_dict.keys():
        st.session_state.fields_prompt_dict[k] = st.text_area(
            k.capitalize(),
            st.session_state.fields_prompt_dict[k],
            height=10,
            help=f"Provide a prompt for the {k.capitalize()}",
        )

    configure_prompts_of_fields(**st.session_state.fields_prompt_dict)
    st.table(SummeryTube.construct_prompt_for_fields_as_dict())

    if st.button("🚀 Click here if you are happy with the prompts"):
        st.session_state.prompt_confirmed = True

    if st.session_state.prompt_confirmed:
        st.write("Generating summary...")
        if st.session_state.summary is None and st.session_state.transcript is not None:
            try:
                st.session_state.summary = utils.gen_summary_from_transcript(
                    st.session_state.transcript
                )
            except Exception as e:
                st.error("Failed to generate the summary.")
                logger.error(f"Error generating summary for video ID {video_id}: {e}")
        if st.session_state.summary:
            st.write("## Summary:")
            st.session_state.summary = utils.struct_summary(st.session_state.summary)
            for field in st.session_state.summary.model_fields:
                st.write(f"### {field.capitalize()}")
                st.write(getattr(st.session_state.summary, field))
