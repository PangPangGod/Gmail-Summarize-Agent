SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
AGENTQUERY={"input": "`search_gmail` with `{'query': 'from':'Medium Daily Digest', 'max_results': 1}`.  Get Most recent matching mail with id ONLY. return must be like 'the matching mail id is:'"}
OUTPUTHANDLINGQUERY= """get dict {url_dict}. Show value and url if it is related to LLM or Python or Programming.
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
        ]}}"""