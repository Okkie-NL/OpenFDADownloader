from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from time import sleep
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests

from .config import Settings


@dataclass(slots=True)
class HttpResponse:
    status_code: int
    body: str
    next_url: str | None
    headers: dict[str, str]


@dataclass(slots=True)
class DownloadPage:
    number: int
    response: HttpResponse
    data: dict

    @property
    def raw_json(self) -> str:
        return self.response.body

    @property
    def meta(self) -> dict:
        return self.data.get("meta", {})

    @property
    def results(self) -> list:
        return self.data.get("results", [])

    @property
    def record_count(self) -> int:
        return len(self.results)


class OpenFDAApiClient:
    def __init__(self, settings: Settings) -> None:

        self.settings = settings

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "OpenFDADataPipeline/1.0",
            }
        )

    def build_initial_url(self) -> str:

        params = {
            "search": self.settings.search,
            "limit": self.settings.page_size,
            "sort": self.settings.sort,
        }

        if self.settings.api_key:
            params["api_key"] = self.settings.api_key

        request = requests.Request(
            "GET",
            f"https://api.fda.gov/{self.settings.endpoint}.json",
            params=params,
        )

        prepared = self.session.prepare_request(request)

        if prepared.url is None:
            raise RuntimeError(
                "Failed to build request URL."
            )

        return prepared.url

    def get(self, url: str) -> HttpResponse:

        url = self._with_api_key(url)

        delay = self.settings.retry_delay

        for attempt in range(
            self.settings.retry_count + 1
        ):

            try:

                response = self.session.get(
                    url,
                    timeout=self.settings.timeout,
                )

                if response.status_code == 200:

                    return HttpResponse(
                        status_code=response.status_code,
                        body=response.text,
                        next_url=self._extract_next_url(
                            response
                        ),
                        headers=dict(response.headers),
                    )

                if response.status_code in (
                    429,
                    503,
                ):

                    if (
                        attempt
                        == self.settings.retry_count
                    ):
                        break

                    retry_after = response.headers.get(
                        "Retry-After"
                    )

                    if (
                        retry_after
                        and retry_after.isdigit()
                    ):
                        sleep(int(retry_after))
                    else:
                        sleep(delay)
                        delay *= 2

                    continue

                response.raise_for_status()

            except requests.Timeout:

                if (
                    attempt
                    == self.settings.retry_count
                ):
                    raise

                sleep(delay)
                delay *= 2

            except requests.ConnectionError:

                if (
                    attempt
                    == self.settings.retry_count
                ):
                    raise

                sleep(delay)
                delay *= 2

        raise RuntimeError(
            f"Request failed after "
            f"{self.settings.retry_count} retries."
        )

    def pages(self) -> Iterator[DownloadPage]:

        page_number = 1
        next_url = self.build_initial_url()

        while next_url:

            response = self.get(next_url)

            data = json.loads(response.body)

            yield DownloadPage(
                number=page_number,
                response=response,
                data=data,
            )

            next_url = response.next_url
            page_number += 1

    @staticmethod
    def _extract_next_url(
        response: requests.Response,
    ) -> str | None:

        link = response.headers.get("Link")

        if not link:
            return None

        start = link.find("<")
        end = link.find(">")

        if start == -1 or end == -1:
            return None

        return link[start + 1 : end]

    def _with_api_key(
        self,
        url: str,
    ) -> str:

        if not self.settings.api_key:
            return url

        parsed = urlparse(url)
        query = dict(parse_qsl(parsed.query))

        query.setdefault(
            "api_key",
            self.settings.api_key,
        )

        return urlunparse(
            parsed._replace(
                query=urlencode(query)
            )
        )