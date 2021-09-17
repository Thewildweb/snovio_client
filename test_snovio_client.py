import os

import pytest
from dotenv import load_dotenv

from snovio_client import SnovioClient, DomainResponse, Email

load_dotenv()


class MissingEnvironmentVariable(Exception):
    pass


def test_get_token():
    api_user = os.environ.get("API_USER")
    api_secret = os.environ.get("API_SECRET")

    if not api_user or not api_secret:
        raise MissingEnvironmentVariable(
            "For this test the API_USER and API_SECRET env variables are needed"
        )

    client = SnovioClient(api_user, api_secret)
    token = client.token

    assert token
    assert isinstance(token, str)


def test_domain_search():
    api_user = os.environ.get("API_USER")
    api_secret = os.environ.get("API_SECRET")

    if not api_user or not api_secret:
        raise MissingEnvironmentVariable(
            "For this test the API_USER and API_SECRET env variables are needed"
        )

    client = SnovioClient(api_user, api_secret)
    domain = client.domain_search(domain="elinerosina.com", limit=1, type="personal")

    assert isinstance(domain, DomainResponse)
    assert len(domain.emails) == 1
    assert isinstance(domain.emails[0], Email)
