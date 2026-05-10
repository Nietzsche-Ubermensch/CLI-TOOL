from dataclasses import dataclass


@dataclass(slots=True)
class SandboxPolicy:
    enabled: bool = False
    platform: str = "auto"
    allow_network: bool = True
