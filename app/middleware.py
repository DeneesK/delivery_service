from typing import Callable
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SessionIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not request.session.get("session_id"):
            request.session["session_id"] = str(uuid4())
        response = await call_next(request)
        return response
