"""本地偏好的读取与完整替换。"""

from wardrobe.features.profile import state
from wardrobe.features.profile.models import ProfilePreferences


def get_preferences() -> ProfilePreferences:
    """读取当前进程的演示偏好，不影响推荐规则。"""
    return state.preferences


def replace_preferences(payload: ProfilePreferences) -> ProfilePreferences:
    """完整替换演示偏好，目前不联动任何推荐服务。"""
    state.preferences = payload.model_copy(deep=True)
    return state.preferences
