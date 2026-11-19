"""保存当前进程的单份演示偏好。"""

from wardrobe.features.profile.models import ProfilePreferences


# ponytail: 仅有一份本地偏好，重启清空；多用户使用前需持久化并按账号隔离。
preferences = ProfilePreferences()
