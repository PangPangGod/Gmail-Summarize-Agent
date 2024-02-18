import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from langchain import hub
from langchain_community.agent_toolkits import GmailToolkit
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor

from config import SCOPES

def create_credentials(scopes=SCOPES, token_file='token.json', credentials_file='credentials.json'):
    """Create or load Google API credentials."""
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    else:
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds

class GmailLangChainAgent:
    """A Gmail agent integrated with LangChain for processing and executing Gmail-related tasks."""

    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0, streaming=True, max_tokens=2048):
        self.creds = create_credentials()
        self.toolkit = self._set_default_toolkit()
        self.model = self._initialize_model(model, temperature, streaming, max_tokens)
        self.agent = self._create_agent()
        self.agent_executor = self._build_executor()

    def _set_default_toolkit(self):
        """Set the default LangChain GmailToolkit."""
        from langchain_community.tools.gmail.utils import build_resource_service
        return GmailToolkit(api_resource=build_resource_service(credentials=self.creds))

    def _initialize_model(self, model, temperature, streaming, max_tokens):
        """Initialize the ChatOpenAI model."""
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model, temperature=temperature, streaming=streaming, max_tokens=max_tokens)

    def _create_agent(self):
        """Create a LangChain agent with the provided model and tools."""
        from langchain import hub
        from langchain.agents import create_openai_functions_agent

        instructions = "You are an assistant. Return output only."
        template_from_hub = hub.pull("langchain-ai/openai-functions-template")
        agent_prompt = template_from_hub.partial(instructions=instructions)
        return create_openai_functions_agent(self.model, self.toolkit.get_tools(), agent_prompt)

    def _build_executor(self):
        """Build the LangChain agent executor."""
        from langchain.agents import AgentExecutor
        return AgentExecutor(agent=self.agent, tools=self.toolkit.get_tools())

    def run(self, prompt):
        """Execute the agent with the given prompt."""
        return self.agent_executor.invoke(prompt)

# # Usage example
# if __name__ == "__main__":
#     gmail_langchain_agent = GmailLangChainAgent()
#     prompt = {"input": "`search_gmail` with `{'query': 'from':'Medium Daily Digest', 'max_results': 1}`.  Get Most recent matching mail with id ONLY. return must be like 'the matching mail id is:'"}
#     search_result = gmail_langchain_agent.run(prompt)
#     print(search_result)