from __future__ import annotations

import json
from collections.abc import MutableMapping
from typing import Any

import requests
from requests import RequestException
from requests import Response as RequestsResponse

from audio_tribe.libs.exceptions import ThirdPartyAPIConnectionError


class Response:
    """Data class for response third party request response."""

    response_data: Any
    status_code: int
    headers: MutableMapping[str, str] | None

    def __init__(
        self,
        response_data: Any,
        status_code: int,
        headers: MutableMapping[str, str] | None = None,
        response_object: RequestsResponse | None = None,
    ):
        """Set data."""
        self.response_data = response_data
        self.status_code = status_code
        self.headers = headers
        self.response_object = response_object


class RequestClient:
    """Requests wrapper library used to handle HTTP requests to third party libraries."""

    _conn_timeout = 15
    _read_timeout = 45

    def __init__(
        self,
        third_party: str,
        conn_timeout: int | None = None,
        read_timeout: int | None = None,
    ):
        """Third party name and timeout if set."""
        self.third_party = third_party
        self._conn_timeout = conn_timeout if conn_timeout else self._conn_timeout
        self._read_timeout = read_timeout if read_timeout else self._read_timeout

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: MutableMapping[str, str] | None,
        params: MutableMapping[str, str] | None = None,
        post_data: dict[str, Any] | None = None,
        sensitive_request_data: dict[str, Any] | None = None,
        verify: bool = True,
        body_data: str | None = "",
    ) -> Response:
        """
        Perform request to third party endpoints.

        :param params:
        :param method:
        :param url:
        :param headers:
        :param post_data:
        :param sensitive_request_data: This should contain data like SECKEY which we don't want recorded anywhere.
        :return: Response object with request code and response data.
        """
        if post_data is None:  # pragma: no cover
            post_data = {}

        # Add sensitive here to not log it.
        if sensitive_request_data:  # pragma: no cover
            post_data.update(sensitive_request_data)

        try:
            response = requests.request(  # nosemgrep  # awaiting https://gitlab.int.seedstars.com/shared/common/-/issues/6
                method,
                url,
                headers=headers,
                data=json.dumps(post_data) if not body_data else body_data,
                timeout=(self._conn_timeout, self._read_timeout),
                params=params,
                verify=verify,
            )
            status_code = response.status_code
            try:
                response_data = response.json()
                headers = response.headers
            except json.JSONDecodeError:  # pragma: no cover
                response_data = {}

            return Response(
                response_data=response_data,
                headers=headers,
                status_code=status_code,
                response_object=response,
            )
        except RequestException as request_error:
            raise ThirdPartyAPIConnectionError(
                response_code=request_error.response.status_code
                if request_error.response
                else 0,
                response_data={"message": str(request_error)},
            ) from request_error
