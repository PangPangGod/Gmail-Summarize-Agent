from googleapiclient.discovery import build
from agent import GmailLangChainAgent, create_credentials
from parsers import get_message_from_id, validate_email_url
from bs4 import BeautifulSoup
from datetime import date
from config import AGENTQUERY

from chain import url_handling_chain

#### RUN
#### Agent Part (Get most recent "Medium Daily Digest Email ID" from GmailAPI)
gmail_langchain_agent = GmailLangChainAgent()
search_result = gmail_langchain_agent.run(AGENTQUERY)
search_result_parsed_output = search_result["output"].split(":")[-1].lstrip(" ") # parse result

#### Get specific id and raw html snippet from GMAIL API, parse html
creds = create_credentials()
service = build('gmail', 'v1', credentials=creds)

#### Get mail content from id and parsing with BS4
user_id = 'me'
message_id = search_result_parsed_output
html_content = get_message_from_id(service, user_id, message_id)

soup = BeautifulSoup(html_content, 'html.parser')
links = soup.find_all('a')

url_dict = {}
for link in links:
    url = link.get('href').split("?")[0] #parsed url
    text = link.get_text(strip=True) #description of url
    if validate_email_url(url):
        url_dict[url] = text

if url_dict:
    running_result = url_handling_chain(url_dict) ## result will be parsed as dictionary.

### print as markdown syntex(save as .bat compatibility)
today = date.today()
result_format = f"___\n\n ## Here is your Today's Daily LLM Digest! : {today}\n\n"
for idx, content in enumerate(running_result.url_text_pairs, 1):
    result_format += f"{idx}. [{content.description}]({content.url})\n\n"

print(result_format)