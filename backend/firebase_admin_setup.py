import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)

def send_push(token: str, notification: dict):
    message = messaging.Message(
        token=token,
        notification=messaging.Notification(
            title=notification["title"],
            body=notification["body"],
            image=notification.get("image_url")
        ),
        webpush=messaging.WebpushConfig(
            fcm_options=messaging.WebpushFCMOptions(
                link=notification.get("action_url")
            )
        ),
        data=notification.get("data") or {}
    )

    response = messaging.send(message)
    return response
