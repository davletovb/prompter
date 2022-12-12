import openai
import os

api_key = os.environ.get('OPENAI_API_KEY')


class QueryAPI:
    def __init__(self):

        openai.api_key = api_key

    def generate_text(self, prompt):
        # Use the OpenAI API (text-davinci-003) to generate text based on the given prompt
        gpt_prompt = f"""Turn the following into a blog post: {prompt} """
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=gpt_prompt,
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        except openai.error.APIError as e:
            print(f"Error: {e}")
            return None

        return response.choices[0].text
