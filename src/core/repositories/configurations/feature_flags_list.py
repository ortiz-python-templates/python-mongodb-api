from typing import Any, Dict, List
from src.core.repositories.configurations.feature_flags import *

class FeatureFlagList:

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return configuration_flags + company_flags + identity_flags
        