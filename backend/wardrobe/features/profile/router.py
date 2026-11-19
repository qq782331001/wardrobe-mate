"""本地演示偏好接口。"""

from fastapi import APIRouter

from wardrobe.features.profile import service
from wardrobe.features.profile.models import ProfilePreferences


router = APIRouter(prefix="/profile", tags=["本地偏好"])


@router.get("")
async def get_preferences() -> ProfilePreferences:
    """查看演示偏好，此接口不表示登录状态。"""
    return service.get_preferences()


@router.put("")
async def replace_preferences(payload: ProfilePreferences) -> ProfilePreferences:
    """完整替换单份本地偏好。"""
    return service.replace_preferences(payload)
