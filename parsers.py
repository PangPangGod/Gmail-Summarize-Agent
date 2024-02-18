import base64
import email
from urllib.parse import urlparse

def get_message_from_id(service, user_id, message_id):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='raw').execute()
        # print('Message snippet: %s' % message['snippet'])

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

def validate_email_url(url)->bool:
    """Return True if it meets the criteria(url, username)."""
    parsed_url = urlparse(url)
    if parsed_url.scheme == "https" and parsed_url.netloc == "medium.com":
            # 경로에서 @username 확인
            path_parts = parsed_url.path.split('/')
            if len(path_parts) >= 3 and path_parts[1].startswith('@'):
                return True
    return False