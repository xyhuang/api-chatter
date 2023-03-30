import json
import os
import re

import openai


task_matching_sys_message = """
Return the key in the item list below whose value best matches user's instruction.
Desired format:
{\"task_id\": <key>}

Item list:

"""

api_generation_sys_message = """
Construct api requests from openapi spec and user instruction. In the request body, only print fields that are relevant to the instruction.
Desired format:
{
  "url": <url_of_the_request>,
  "method": <method_of_the_request>,
  "headers": [<comma_separated_list_of_headers>],
  "body": <request_body>
}

OpenAPI Spec:

"""

class OpenAIClient(object):

    def __init__(self):
        openai.organization = os.getenv("OPENAI_ORGANIZATION")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"

    def match_task(self, task_descriptions, instruction):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": task_matching_sys_message + json.dumps(task_descriptions)},
                {"role": "user", "content": instruction}
            ],
            temperature=0,
            max_tokens=256
        )
        response_message = completion.choices[0].message["content"]
        regex_match = re.search(r"({\"task_id\":.*?})", response_message)
        if regex_match is None:
            return None
        response_message = json.loads(regex_match.group(1))
        return response_message["task_id"]

    def generate_api(self, api_description, instruction):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": api_generation_sys_message + json.dumps(api_description)},
                {"role": "user", "content": instruction}
            ],
            temperature=0,
            max_tokens=512
        )
        response_message = completion.choices[0].message["content"]
        return response_message
