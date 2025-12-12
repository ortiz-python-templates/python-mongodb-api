from datetime import datetime
from fastapi import Request
from src.core.services.configurations.flags import FlagList
from src.core.repositories.configurations.feature_flag_query_repository import FeatureFlagQueryRepository
from src.core.schemas.pagination_response import PaginationResponse
from src.core.filters.pagination_filter import PaginationFilter
from src.common.utils.custom_exceptions import BadRequestException, NotFoundException
from src.core.schemas.configurations.feature_flag_responses import FeatureFlagDetail
from src.common.utils.messages.configurations_messages import CompanyConfigMsg
from src.core.schemas.common_results import UpdatedResult
from src.core.schemas.configurations.feature_flag_requests import ManageFeatureFlagRequest
from src.core.repositories.configurations.feature_flag_command_repository import FeatureFlagCommandRepository


class FeatureFlagService:

    def __init__(self, db):
        self.command_repository = FeatureFlagCommandRepository(db)
        self.query_repository = FeatureFlagQueryRepository(db)


    async def create_all_feature_flags(self):
        flags = FlagList.get_all()
        results = []

        for flag in flags:
            filter_q = {"flag_name": flag["flag_name"]}

            update_q = {
                "$set": {
                    "description": flag.get("description"),
                    "is_enabled": flag.get("is_enabled", False),
                }
            }

            result = await self.command_repository.update_raw(
                filter=filter_q,
                update=update_q,
                upsert=True,
            )

            results.append({
                "flag_name": flag["flag_name"],
                "matched": result.matched_count,
                "modified": result.modified_count,
                "upserted_id": getattr(result, "upserted_id", None)
            })

        return {
            "total": len(flags),
            "updated_or_inserted": results
        }


    async def manage_feature_flag(self, request: Request, body: ManageFeatureFlagRequest):
        feature_flag = await self.command_repository.get_by_name_aux(body.flag_name)
        if feature_flag is None:
            raise NotFoundException(f"Flag with name '{body.flag_name}' not found")
        # current user
        current_user = request.state.user
        # update
        feature_flag.is_enabled = body.is_enabled
        feature_flag.updated_at = datetime.now()
        feature_flag.updated_by = current_user.id
        await self.command_repository.update(feature_flag.id, feature_flag)
        
        return UpdatedResult(
            id=feature_flag.unique_id,
            message=CompanyConfigMsg.Success.UPDATED
        )
    
    
    async def get_all_feature_flags(self, request: Request, pagination_filter: PaginationFilter) -> PaginationResponse[FeatureFlagDetail]:
        if pagination_filter.page_size <= 0 or pagination_filter.page_index < 0:
            raise BadRequestException("Invalid pagination parameters. Check page_size and page_index.")
        feature_flags = await self.query_repository.get_all(pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=feature_flags,
            total_items=await self.query_repository.count(),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def get_feature_flag_by_id(self, request: Request, id: str) -> FeatureFlagDetail:
        feature_flag = await self.query_repository.get_by_id(id)
        if feature_flag is None:
            raise NotFoundException(f"Feature flag with ID '{id}' was not found.")
        return feature_flag