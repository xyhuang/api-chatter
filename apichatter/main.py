import sys

from . import openai_client
from . import openapi_helper


def main():
    args = sys.argv
    if len(args) !=2:
        print("wrong arguments")
        sys.exit()
    openapi_spec_file = args[1]

    api_helper = openapi_helper.OpenAPIHelper()
    api_helper.load(openapi_spec_file)

    oai_client = openai_client.OpenAIClient()
    task_descriptions = api_helper.get_task_descriptions()
    while True:
        instruction = input("> ")
        task_id = oai_client.match_task(task_descriptions, instruction)
        if task_id is None:
            print("Sorry, I could not find the relevant API, please try a different description.")
            continue
        api_description = api_helper.get_spec_from_task(task_id)
        answer = oai_client.generate_api(api_description, instruction)
        print(answer)
        print("")

if __name__ == "__main__":
    main()
