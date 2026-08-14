from app.auth.clerk import clerk
from app.util.config import settings


def invite_employee(
    email: str
):
    invitation = clerk.invitations.create(
        request={
        "email_address": email,
        "redirect_url": settings.CLERK_SIGN_UP_URL,
        }
    )

    return invitation