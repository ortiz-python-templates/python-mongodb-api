from typing import List
from src.common.utils.custom_exceptions import NotFoundException
from src.core.models.identity.role import Role


class RoleService:

    def __init__(self):
        pass

    def get_all_roles(self) -> list[dict[str, str]]:
        return [
            {"code": Role.SUPER_ADMIN, "description": Role.get_description(Role.SUPER_ADMIN)},
            {"code": Role.ADMIN, "description": Role.get_description(Role.ADMIN)},
            {"code": Role.EMPLOYEE, "description": Role.get_description(Role.EMPLOYEE)},
            {"code": Role.CUSTOMER, "description": Role.get_description(Role.CUSTOMER)},
            {"code": Role.SUPPLIER, "description": Role.get_description(Role.SUPPLIER)},
        ]


    def get_role_by_code(self, code: str) -> dict[str, str]:
        if code in self.get_roles_list():
            return {
                "code": code,
                "description": Role.get_description(code)
            }
        raise NotFoundException(f"Role '{code}' does not exist.")


    def get_roles_list(self) -> List[str]:
        return [
            Role.SUPER_ADMIN,
            Role.ADMIN,
            Role.EMPLOYEE,
            Role.CUSTOMER,
            Role.SUPPLIER,
            Role.INTEGRATOR
        ]