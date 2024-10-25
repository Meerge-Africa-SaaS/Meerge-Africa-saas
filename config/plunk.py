import requests  # type: ignore[import]
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, sanitize_address


class PlunkEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)

    def send_messages(self, email_messages: list[EmailMessage]) -> int:
        for message in email_messages:
            # from_email = sanitize_address(message.from_email, message.encoding)
            message.message
            recipients = [
                sanitize_address(addr, message.encoding)
                for addr in message.recipients()
            ]
            subject = message.subject
            body = getattr(message, "html", message.body)
            headers = message.extra_headers
            payload = {
                "to": recipients,
                "subject": subject,
                "body": body,
                "subscribed": False,
                "name": "Meerge Africa",
                # TODO: add from field
                # "from": from_email,
                # TODO: add reply field
                # "reply": from_email,
                "headers": headers,
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.PLUNK_API_KEY}",
            }
            response = requests.post(
                settings.PLUNK_API_URL, json=payload, headers=headers
            )
            response.raise_for_status()
        return len(email_messages)
