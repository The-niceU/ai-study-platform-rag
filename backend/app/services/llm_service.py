from openai import OpenAI

from app.core.config import settings

print("API KEY:", settings.OPENAI_API_KEY[:10] if settings.OPENAI_API_KEY else "EMPTY")
print("BASE URL:", settings.OPENAI_BASE_URL)
print("MODEL:", settings.OPENAI_MODEL)
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)


def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个课程资料问答助手。你必须优先依据提供的资料片段回答问题，不要编造。如果资料不足，请明确说明资料不足。回答尽量清晰、简洁。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()