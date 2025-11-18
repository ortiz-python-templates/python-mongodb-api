import re


class RegexValidator:
    """
    🔹 Common Regex Validators for production use.
    """

    # 🔹 Personal fiscal number — Angola (9 digits + 2 letters + 3 digits)
    PERSONAL_FISCAL_NUMBER = r"^\d{9}[A-Z]{2}\d{3}$"

    # 🔹 Company fiscal number — only digits (10 to 14 digits)
    COMPANY_FISCAL_NUMBER = r"^\d{10,14}$"

    # 🔹 Angolan phone number — starts with 9 and has 9 digits; accepts +244 or 00244
    PHONE_NUMBER = r"^(?:\+244|00244)?9\d{8}$"

    # 🔹 Angola IBAN — starts with AO + 2 digits + 21 numbers (25 characters total)
    IBAN = r"^AO\d{2}\d{21}$"

    # 🔹 Social security number (INSS) — normally 9 digits
    SOCIAL_SECURITY_NUMBER = r"^\d{9}$"

    @staticmethod
    def validate_field(value: str, pattern: str, field_name: str) -> str:
        """
        Validate a field using a regex pattern.
        
        Args:
            value (str): The value to validate.
            pattern (str): Regex pattern.
            field_name (str): Name of the field for error messages.
        
        Returns:
            str: Original value if valid.
        
        Raises:
            ValueError: If the value does not match the pattern.
        """
        if not re.match(pattern, value):
            raise ValueError(f"{field_name} is invalid. Accepted format required.")
        return value

    # Example values for testing
    class Example:
        PERSONAL_FISCAL_NUMBER = "123456789AB123"
        COMPANY_FISCAL_NUMBER = "5001234567"
        PHONE_NUMBER_1 = "+244923456789"
        PHONE_NUMBER_2 = "923456789"
        PHONE_NUMBER_3 = "00244923456789"
        IBAN = "AO06004400000000012345678"
        SOCIAL_SECURITY_NUMBER = "005069955"
