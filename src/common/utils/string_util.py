import re


class StringUtil:

    @staticmethod
    def to_camel_case(string: str) -> str:
        parts = string.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    @staticmethod
    def to_snake_case(string: str) -> str:
        result = re.sub(r'(?<!^)([A-Z])', r'_\1', string).lower()
        return result
  