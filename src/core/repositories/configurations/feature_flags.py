
# IDENTITY
identity_flags = [
    {
        "flag_name": "flag.identity.create-user",
        "description": "Allows creating new users",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.update-user",
        "description": "Allows editing existing users",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.delete-user",
        "description": "Allows permanently deleting users",
        "is_enabled": False
    },
    {
        "flag_name": "flag.identity.get-all-users",
        "description": "Allows retrieving the list of all users (including active and inactive)",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.get-active-users",
        "description": "Allows retrieving the list of only active users",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.get-inactive-users",
        "description": "Allows retrieving the list of only inactive users",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.search-users",
        "description": "Allows searching for users based on query parameters",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.get-user-by-id",
        "description": "Allows retrieving a single user's details using their ID",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.get-user-by-email",
        "description": "Allows retrieving a single user's details using their email address",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.activate-user",
        "description": "Allows changing a user's status to active",
        "is_enabled": True
    },
    {
        "flag_name": "flag.identity.deactivate-user",
        "description": "Allows changing a user's status to inactive",
        "is_enabled": True
    }
]

# Configurations
configuration_flags = [
    {
        "flag_name": "flag.configuration.update-basic-configurations",
        "description": "Allows updating the system's basic configuration settings",
        "is_enabled": True
    },
    {
        "flag_name": "flag.configuration.get-basic-configurations",
        "description": "Allows viewing the system's basic configuration settings",
        "is_enabled": True
    },
    {
        "flag_name": "flag.configuration.update-company-configurations",
        "description": "Allows updating the company-specific configuration settings",
        "is_enabled": True
    },
    {
        "flag_name": "flag.configuration.get-company-configurations",
        "description": "Allows viewing the company-specific configuration settings",
        "is_enabled": True
    }
]

company_flags = [
    # --- BRANCHES Flags ---
    {
        "flag_name": "flag.company.create-branch",
        "description": "Allows creating new company branches",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.get-branches",
        "description": "Allows viewing the list of all company branches",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.update-branch",
        "description": "Allows editing existing company branch details",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.delete-branch",
        "description": "Allows deleting company branches",
        "is_enabled": False
    },

    #--- OFFICES Flags ---
    {
        "flag_name": "flag.company.create-office",
        "description": "Allows creating new offices within branches",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.get-offices",
        "description": "Allows viewing the list of all offices",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.update-office",
        "description": "Allows editing existing office details",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.delete-office",
        "description": "Allows deleting offices",
        "is_enabled": False
    },

    # --- ROOMS Flags ---
    {
        "flag_name": "flag.company.create-room",
        "description": "Allows creating new rooms within offices",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.get-rooms",
        "description": "Allows viewing the list of all rooms",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.update-room",
        "description": "Allows editing existing room details",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.delete-room",
        "description": "Allows deleting rooms",
        "is_enabled": False
    },

    # --- DEPARTMENTS Flags ---
    {
        "flag_name": "flag.company.create-department",
        "description": "Allows creating new company departments",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.get-departments",
        "description": "Allows viewing the list of all departments",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.update-department",
        "description": "Allows editing existing department details",
        "is_enabled": True
    },
    {
        "flag_name": "flag.company.delete-department",
        "description": "Allows deleting departments",
        "is_enabled": False
    }
]