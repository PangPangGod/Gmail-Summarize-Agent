#### Agent Part (Get most recent "Medium Daily Digest Email ID" from GmailAPI)
from gmailagent import GmailAgent
agent = GmailAgent()
result = agent.search_emails("'from':'Medium Daily Digest'")
parsed_result = result["output"].split(":")[-1].lstrip(" ") # parse result

####
import base64
import email
service = build('gmail', 'v1', credentials=creds)

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

# 메일 내용 가져오기 및 파싱 예제
user_id = 'me'  # 현재 로그인한 사용자
message_id = parsed_result  # 가져오고자 하는 메시지의 ID
html_content = get_message(service, user_id, message_id)
