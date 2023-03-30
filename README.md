# api-chatter

Api-Chatter is an HTTP request generator powered by ChatGPT. Given a user instruction in natural language, it generates an HTTP request based on a pre-defined OpenAPI specification.

## Installation

```
pip3 install requirements.txt
```

## Prerequisites

- Get an OpenAI account and create an API key
- Have an OpenAPI specification file in json or yaml format

## Usage

- set the following environment variables
  ```
  OPENAI_ORGANIZATION=<your_openai_organization_id>
  OPENAI_API_KEY=<your_openai_api_key>
  ```
- run the following command to start
  ```
  python3 -m apichatter.main <openapi_specification_file_path>
  ```
- once you see the prompt `> `, type in your instructions in natural language
- if a relevant API is found, the generated HTTP request will be returned, usually after a few seconds

