from pydantic import BaseModel, Field


class SummeryTube(BaseModel):
    title: str = Field(
        description="The title of the video",
        prompt=(  # pyright: ignore
            "A title of at most 60 characters based on the transcript"
        ),
    )
    description: str = Field(
        description="The description of the video",
        prompt=(  # pyright: ignore
            "A description for the video of at most "
            "250 characters based on the transcript"
        ),
    )
    hashtags: list[str] = Field(
        description="The hashtags for the video",
        prompt="A list of 12 hashtags recommended for the video",  # pyright: ignore
    )

    @classmethod
    def construct_prompt_for_fields_as_dict(cls, **kwargs) -> dict[str, str]:
        schema = cls.model_json_schema()
        return {
            k: schema["properties"][k]["prompt"] for k in schema["properties"].keys()
        }


def configure_prompts_of_fields(**kwargs) -> None:
    for k in kwargs:
        if k not in SummeryTube.model_fields:
            raise ValueError(f"Field {k} not found in SummeryTube model")
        SummeryTube.model_fields[k].json_schema_extra["prompt"] = kwargs[k]
