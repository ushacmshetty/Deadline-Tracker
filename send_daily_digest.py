
from email_service import send_deadline_digest


if __name__ == "__main__":
    success, message = send_deadline_digest()

    print(message)

    if not success:
        raise SystemExit(1)
