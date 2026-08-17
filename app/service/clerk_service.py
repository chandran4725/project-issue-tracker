import logging
from app.auth.clerk import clerk
from app.util.config import settings

logger = logging.getLogger(__name__)


def invite_employee(
    email: str
):
    try:
        req_payload = {"email_address": email}
        if settings.CLERK_SIGN_UP_URL:
            req_payload["redirect_url"] = settings.CLERK_SIGN_UP_URL

        invitation = clerk.invitations.create(
            request=req_payload
        )
        return invitation
    except Exception as err:
        logger.warning(f"Clerk invitation failed for {email}: {err}")
        return None