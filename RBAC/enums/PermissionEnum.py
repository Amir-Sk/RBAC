from enum import Enum


class PermissionEnum(Enum):
    READ = 'READ'
    WRITE = 'WRITE'
    DELETE = 'DELETE'

    @staticmethod
    def get_available_permissions():
        return [permission_enum.value for permission_enum in PermissionEnum]
