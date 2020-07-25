from django.core.exceptions import ObjectDoesNotExist

from RBAC.enums.RolesEnum import RolesEnum
from RBAC.models import Role
from RBAC.services.PermissionService import PermissionService


class RoleService:

    @staticmethod
    def create_role(role_data):
        if role_data:
            role = Role.objects.create(name=role_data['name'])
            for perm in role_data['permissions']:
                RoleService.add_permission(role, perm['name'])
            return role
        raise NameError

    @staticmethod
    def get_role(role_name):
        if RoleService.is_role_name_valid(role_name):
            try:
                return Role.objects.get(name=role_name)
            except ObjectDoesNotExist as error:
                print("Error: username <{}> does not exist, details: \n{}"
                      .format(role_name, error))
                raise error
        print("ERROR with perm name: {}".format(role_name))
        raise NameError
    
    @classmethod
    def add_permission(cls, role, perm_name):
        permission = PermissionService.get_permission(perm_name)
        role.permissions.add(permission)
        role.save()

    @classmethod
    def is_role_name_valid(cls, role_name):
        if role_name and role_name in RolesEnum.get_available_roles():
            return True
        return False

    # Can be used later on if needed (YAGNI instructs other way ofcourse,
    # but permissions addition with no removal in RBAC is a bit offbeat and unexpected)
    #
    # @staticmethod
    # def remove_permission(role, perm_name):
    #     for perm in role.permissions.all():
    #         if perm.name == perm_name:
    #             role.permissions.remove(perm)
    #             role.save()