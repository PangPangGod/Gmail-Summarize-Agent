from gmailagent import GmailLangChainAgent, create_credentials

import base64
import email
from googleapiclient.discovery import build

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from datetime import date

def get_message_from_id(service, user_id, message_id):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='raw').execute()
        print('Message snippet: %s' % message['snippet'])

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_str)

        # 메일 본문 찾기
        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode()
                    break
        else:
            html_content = mime_msg.get_payload(decode=True).decode()

        return html_content
    except Exception as error:
        print('An error occurred: %s' % error)

def validate_email_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme == "https" and parsed_url.netloc == "medium.com":
            # 경로에서 @username 확인
            path_parts = parsed_url.path.split('/')
            if len(path_parts) >= 3 and path_parts[1].startswith('@'):
                return True
    return False

class URL_TABLE(BaseModel):
    url:str = Field(description="url")
    description:str = Field(description="description that describe url")

class URLTextList(BaseModel):
    url_text_pairs: List[URL_TABLE]

#### RUN
#### Agent Part (Get most recent "Medium Daily Digest Email ID" from GmailAPI)
gmail_langchain_agent = GmailLangChainAgent()
prompt = {"input": "`search_gmail` with `{'query': 'from':'Medium Daily Digest', 'max_results': 1}`.  Get Most recent matching mail with id ONLY. return must be like 'the matching mail id is:'"}
search_result = gmail_langchain_agent.run(prompt)
search_result_parsed_output = search_result["output"].split(":")[-1].lstrip(" ") # parse result

#### Get specific id and raw html snippet from GMAIL API, parse html
creds = create_credentials()
service = build('gmail', 'v1', credentials=creds)

# 메일 내용 가져오기 및 파싱 예제
user_id = 'me'
message_id = search_result_parsed_output
html_content = get_message_from_id(service, user_id, message_id)

soup = BeautifulSoup(html_content, 'html.parser')
links = soup.find_all('a')

url_dict = {}

for link in links:
    text = link.get_text(strip=True)
    url = link.get('href').split("?")[0]

    if validate_email_url(url):
        url_dict[url] = text

parser = PydanticOutputParser(pydantic_object=URLTextList)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
# parse result with PydanticOutputParser
chain = llm | parser
result = chain.invoke(f"""get dict {url_dict}. Show value and url if it is related to LLM or Python or Programming.
    Output should be dictionary like this .
    <Example output>                       
                     {{
    "url_text_pairs": [
        {{
            "url": "https://example.com/1",
            "description": "Example description 1"
        }},
        {{
            "url": "https://example.com/2",
            "description": "Example description 2"
        }}
    ]}}""")

today = date.today()

prompt_format = f"Here is your Today Daily LLM Digest!: {today}\n\n"
for idx, content in enumerate(result.url_text_pairs, 1):
    prompt_format += f"{idx}. \"{content.description}\" \n\t-url: {content.url}\n"
print(prompt_format)