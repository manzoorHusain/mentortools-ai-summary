# Author: Manzoor Hussain


from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def test_summary() -> None:
    description = "Learn Python from scratch in this beginner-friendly course. You'll cover variables, functions," \
                  " loops, and build basic projects."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Summarize this course: {description}"}
        ],
        max_tokens=150,
        temperature=0.7
    )

    summary = response.choices[0].message.content
    print("\n✅ AI Summary:\n")
    print(summary)


# 🔽 Call the test when run directly
if __name__ == "__main__":
    test_summary()
