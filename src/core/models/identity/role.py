class Role:
    # Internal - Full control
    SUPER_ADMIN = 'super-admin'      # Full system access
    ADMIN = 'admin'                  # Manages modules and users
    
    # Internal - Operational
    FINANCE = 'finance'              # Manages billing, payments, salaries
    DIRECTOR = 'director'            # Oversees operations and strategic reports
    EMPLOYEE = 'employee'            # Staff member with limited permissions

    # External - Business
    CUSTOMER = 'customer'            # Organization's customer
    SUPPLIER = 'supplier'            # Supplier or business partner
    
    # Technical / Integration
    INTEGRATOR = 'integrator'        # System or partner integrating via API

    
    @staticmethod
    def get_description(role: str) -> str:
        descriptions = {
            Role.SUPER_ADMIN: "Super Administrador",
            Role.ADMIN: "Administrador",
            Role.FINANCE: "Financeiro",
            Role.DIRECTOR: "Diretor",
            Role.EMPLOYEE: "Colaborador",
            Role.CUSTOMER: "Cliente",
            Role.SUPPLIER: "Fornecedor",
            Role.INTEGRATOR: "Integrador de Sistema",
        }
        return descriptions.get(role, "Unknown")
