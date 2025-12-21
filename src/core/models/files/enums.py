from enum import StrEnum


class FileOwnerEntity(StrEnum):
    USERS = "users"
    BASIC_CONFIGURATIONS = "basic_configurations"
    COMPANY_CONFIGURATIONS = "companyconfigurations"
    COMPANIES = "companies"

    
class FileVisibility(StrEnum):
    PRIVATE = "private"
    PUBLIC = "public"
    INTERNAL = "internal"
