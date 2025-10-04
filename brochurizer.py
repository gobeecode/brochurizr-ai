import os
import ollama
import openai

from helpers.credential_helper import CredentialHelper
from helpers.time_helper import TimeHelper
from webpage import Webpage
import json

class Brochurizer:
    def __init__(self, platform: str, model: str, webpage: Webpage):
        self.platform = platform
        self.model = model
        self.webpage = webpage


    def get_brochure_link_messages(self):
        system_prompt = ("You are provided with a list of links in a webpage."
                         "You can decide which of those links are relevant to be included in the company's brochure. "
                         "You should respond in JSON format as in the below example. "
                         "The response should strictly be a JSON and it should start and end with a curly brace. "
                         "Do not add anything else before and after the curly braces. "
                         "Replace the example domain name with the actual domain name."
                         "Make sure that the type and url properties are included.")
        system_prompt += """
        {
            "links": [
                {"type": "about_page", "url": "https://example.com/about"},
                {"type": "careers_page", "url": "https://example.com/careers"}
            ]
        }
        """
        user_prompt = (f"You are looking at the webpage {self.webpage.title} with the url {self.webpage.url}"
                       "Decide on the relevant links for the brochure. Respond with full https url. "
                       "Do not include terms of conditions, service and privacy policy links."
                       f"Below is the list of links. {self.webpage.links}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return messages

    def get_brochure_links(self):
        messages = self.get_brochure_link_messages()
        if self.platform == 'openai':
            CredentialHelper.validate_openai_api_key()
            response = openai.chat.completions.create(
                model=self.model,  # For example: gpt-4o-mini
                messages=messages
            )
            return f"\n\n{response.choices[0].message.content}"
        else:
            response = ollama.chat(model=self.model, messages=messages)
            return f"\n\n{response['message']['content']}"

    def get_create_brochure_messages(self, contents: str):
        system_prompt = ("You are an assistant that analyzes the contents of several webpages of a company and"
                         "creates a short brochure with all the relevant links. You should strictly respond in markdown format.")
        user_prompt = (f"You are looking at the webpage {self.webpage.title}.\n\n"
                       f"Create a short brochure with all the relevant details using the contents below."
                       f"{contents[:20000]}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return messages

    def create_brochure(self):
        with TimeHelper.measure('create_brochure'):
            contents = self.webpage.text
            print(f"Brochure creation started for {self.webpage.title}")
            print(f"Please wait when {self.model} creates the brochure. This might take a while...")
            print("Fetching relevant links...")
            brochure_links = self.get_brochure_links()
            try:
                brochure_links_json = json.loads(brochure_links)
                print(f"Parsed links as JSON. \n {brochure_links_json}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Parse links as JSON failed: {e}") from e
            for link in brochure_links_json.get('links', []):
                print(f"Fetching {link['type']} contents...")
                webpage = Webpage(link.get('url'))
                contents += f"\n\n{link.get('type')}"
                contents += f"\n{webpage.text}"
            messages = self.get_create_brochure_messages(contents)
            if self.platform == 'openai':
                CredentialHelper.validate_openai_api_key()
                response = openai.chat.completions.create(
                    model=self.model,  # For example: gpt-4o-mini
                    messages=messages
                )
                print(f"\n{response.choices[0].message.content}")
            else:
                print("Creating brochure...")
                response = ollama.chat(model=self.model, messages=messages)
                print(f"\n{response['message']['content']}")
        elapsed = TimeHelper.get_elapsed('create_brochure')
        print(f"✅ Brochure created using {self.model} in {elapsed:.4f} seconds.")


