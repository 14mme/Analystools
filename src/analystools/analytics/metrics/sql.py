import re


_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def validate_identifier(name: str) -> str:
    if not _IDENTIFIER_PATTERN.fullmatch(name):
        raise ValueError(
            f"Invalid SQL identifier: {name}"
        )

    return name

def quote_identifier(name: str) -> str:
    validate_identifier(name)
    return f'"{name}"'

def quote_identifier_list(names: list[str]) -> list[str]:
    return [quote_identifier(name) for name in names]