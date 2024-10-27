# Summarize Tube *by Dr. Dror*

**TL;DR** By giving a link to a YouTube video and providing prompts to title, description and hashtags, the tool will generate the needed meta data.

Let's discuss 😎 [here](https://github.com/drorata/summarize_tube/discussions)

## Getting Started

1. Clone the repo
2. Set up the environment: `poetry install`
3. Obtain OpenAI token and place it in `.env` by using the line: `OPENAI_API_KEY=<sk-YOUR_TOKEN_>`. Alternatively, you can use an environment variable with the same name.
4. Run `poetry run streamlit run summarize_tube/gui_app.py` from the root of the project.
5. Go to `http://localhost:8501/`
