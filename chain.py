from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from config import OUTPUTHANDLINGQUERY

# def Pydantic parser
class URL_TABLE(BaseModel):
    url:str = Field(description="url")
    description:str = Field(description="description that describe url")

class URLTextList(BaseModel):
    url_text_pairs: List[URL_TABLE]

def url_handling_chain(url_dict):  
    prompt_template = OUTPUTHANDLINGQUERY.format(url_dict=url_dict)
    # parse result with PydanticOutputParser
    parser = PydanticOutputParser(pydantic_object=URLTextList)
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    # set chain
    chain = llm | parser
    result = chain.invoke(prompt_template)

    return result