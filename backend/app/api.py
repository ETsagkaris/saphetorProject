from fastapi.routing import APIRoute
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ValidationError
from typing import Callable
import bcrypt

from app import errors, settings


async def do_or_error(
    to_be_called, **kwargs
):
    try:
        return await to_be_called(**kwargs)
    except errors.JsonException as exc:
        status_code = exc.code
        content = {
            "message": exc.message,
            "detail": exc.details,
            "data": exc.data,
        }
    except (RequestValidationError, ValidationError) as exc:
        status_code = 422
        content = {
            "message": str(exc),
            "detail": "",
            "data": {},
        }

    return JSONResponse(status_code=status_code, content=content)


class Wrapper(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            return await do_or_error(
                to_be_called=original_route_handler,
                request=request,
            )
        return custom_route_handler


def check_accept(accept):
    if accept and accept not in ("application/json", "application/xml"):
        raise errors.JsonException(
            message=errors.ACCEPT_HEADER_NOT_ACCEPTABLE, code=406)


def generate_etag(new_etag):
    return bcrypt.hashpw(str.encode(new_etag), bcrypt.gensalt()).decode()


def compare_etags(cur_etag, etag):
    return bcrypt.checkpw(str.encode(cur_etag), str.encode(etag))


def check_etag(response, query_params, accept, etag):
    cur_etag = f'{"variants"}/{query_params.json()}/{accept}'
    if etag and compare_etags(cur_etag, etag):
        raise errors.JsonException(
            message=errors.API_CALL_NOT_MODIFIED, code=304)
    response.headers["etag"] = generate_etag(cur_etag)


def check_authorization(authorization):
    if authorization != settings.secret:
        raise errors.JsonException(
            message=errors.PERMISSION_DENIED, code=403)
