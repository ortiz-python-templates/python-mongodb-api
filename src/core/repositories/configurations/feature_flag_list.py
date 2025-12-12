from typing import Any, Dict, List


class FeatureFlagList:

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return [
                {
                    "flag_name": "flag.identity.create-user",
                    "description": "Allows creating new users",
                    "is_enabled": True,
                },
                {
                    "flag_name": "flag.identity.update-user",
                    "description": "Allows editing existing users",
                    "is_enabled": True,
                },
                {
                    "flag_name": "flag.identity.delete-user",
                    "description": "Allows deleting users",
                    "is_enabled": False,
                },
                {
                    "flag_name": "flag.company.update-config",
                    "description": "Allows updating company configuration settings",
                    "is_enabled": True,
                },
                {
                    "flag_name": "flag.system.maintenance-mode",
                    "description": "Enable or disable maintenance mode globally",
                    "is_enabled": False,
                }
        ]
        