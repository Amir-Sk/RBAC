from enum import Enum


class RolesEnum(Enum):
    DESIGNER = 'Designer'
    INTEGRATOR = 'Integrator'

    @staticmethod
    def get_available_roles():
        return [role_enum.value for role_enum in RolesEnum]
