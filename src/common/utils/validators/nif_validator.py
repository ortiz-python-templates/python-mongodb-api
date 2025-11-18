import re
from src.common.utils.validators.regex_validator import RegexValidator


class FiscalNumberValidator:
    @staticmethod
    def validate(fiscal_number: str | None, client_type: object | None):
        """
        Validates a fiscal number for both individual and company clients.
        
        Args:
            fiscal_number (str | None): The fiscal number to validate.
            client_type (object | None): Type of client (e.g., 'Individual', 'Company').
        
        Raises:
            ValueError: If the fiscal number does not match the expected pattern.
        """
        if not fiscal_number or not client_type:
            return  # Nothing to validate if missing

        type_value = str(client_type).upper()

        if "INDIVIDUAL" in type_value:
            if not re.match(RegexValidator.PERSONAL_FISCAL_NUMBER, fiscal_number):
                raise ValueError(
                    "Invalid fiscal number for individual client. Example: 123456789AB123"
                )
        else:
            if not re.match(RegexValidator.COMPANY_FISCAL_NUMBER, fiscal_number):
                raise ValueError(
                    "Invalid fiscal number for company client. Must be 10 to 14 digits."
                )
