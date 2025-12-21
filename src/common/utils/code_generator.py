import random
from datetime import datetime, timezone


class CodeGenerator:

    @staticmethod
    def generate(prefix: str, sequence: int) -> str:
        """Generates a unique code in the format PREFIX-YYYY-####"""
        year = datetime.now(timezone.utc).year
        return f"{prefix}-{year}-{sequence:04d}"

    @staticmethod
    def generate_random(prefix: str) -> str:
        """Generates a unique code in the format PREFIX-YYYY-RAND####"""
        year = datetime.now(timezone.utc).year
        rand = random.randint(1000, 9999)
        return f"{prefix}-{year}-RAND{rand}"

    @staticmethod
    def generate_with_timestamp(prefix: str) -> str:
        """Generates a unique code in the format PREFIX-YYYYMMDDHHMMSS"""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return f"{prefix}-{ts}"
