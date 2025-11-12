from dataclasses import dataclass

@dataclass
class Credential:
    site: str
    username: str
    password: str
