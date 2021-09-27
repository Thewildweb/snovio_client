from typing import Optional
import json

import requests
from pydantic import BaseModel, Field


class Email(BaseModel):
    email: str
    first_name: str = Field(None, alias="firstName")
    last_name: str = Field(None, alias="lastName")
    position: str
    source_page: str = Field(None, alias="sourcePage")
    company_name: str = Field(None, alias="companyName")
    type: str
    status: str


class DomainResponse(BaseModel):
    success: bool
    domain: str
    webmail: bool
    result: int
    last_id: int = Field(None, alias="lastId")
    limit: int
    company_name: str = Field(None, alias="companyName")
    emails: list[Email]


class SnovioClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: Optional[str] = None

    @property
    def token(self):
        if self._token:
            return self._token

        self._token = self.get_token()
        return self._token

    def get_token(self) -> str:
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        res = requests.post("https://api.snov.io/v1/oauth/access_token", data=params)
        resText = res.text.encode("ascii", "ignore")

        return json.loads(resText)["access_token"]

    def domain_search(
        self,
        domain: str,
        type: Optional[str] = "all",
        limit: Optional[int] = 10,
        lastId: Optional[int] = 0,
        positions: Optional[list[str]] = None,
    ) -> DomainResponse:
        params = locals()
        params["access_token"] = self.token
        params["positions[]"] = params["positions"]
        del params["positions"]
        resp = requests.get(
            "https://api.snov.io/v2/domain-emails-with-info", params=params
        )
        return DomainResponse.parse_obj(json.loads(resp.text))
