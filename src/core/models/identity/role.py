from enum import StrEnum


class Role(StrEnum):
    # Internal - Full control
    SUPER_ADMIN = 'super-admin'
    ADMIN = 'admin'
    
    # Internal - Operational
    EMPLOYEE = 'employee'

    # External - Business
    CUSTOMER = 'customer'
    SUPPLIER = 'supplier'
    
    # Technical / Integration
    INTEGRATOR = 'integrator'

    @staticmethod
    def get_description(role: str) -> str:
        descriptions = {
            Role.SUPER_ADMIN: "Super Administrator",
            Role.ADMIN: "Administrator",
            Role.EMPLOYEE: "Employee",
            Role.CUSTOMER: "Customer",
            Role.SUPPLIER: "Supplier",
            Role.INTEGRATOR: "System Integrator",
        }
        return descriptions.get(role, "Unknown")
