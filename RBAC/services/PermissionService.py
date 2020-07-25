import json

from django.core.exceptions import ObjectDoesNotExist

from RBAC.enums.PermissionEnum import PermissionEnum
from RBAC.models import Permission # , Endpoint


class PermissionService:

    ep_conf_path = "./RBAC/configurations/endpoints_by_permissions.json"

    @staticmethod
    def create_permission(perm_name):
        if PermissionService.is_perm_name_valid(perm_name):
            return Permission.objects.create(name=perm_name)
        raise NameError

    @staticmethod
    def get_permission(perm_name):
        if PermissionService.is_perm_name_valid(perm_name):
            try:
                return Permission.objects.get(name=perm_name)
            except ObjectDoesNotExist as error:
                print("Error: permission <{}> does not exist, details: \n{}"
                      .format(perm_name, error))
                raise error
        print("ERROR with perm name: {}".format(perm_name))
        raise NameError

    @classmethod
    def is_perm_name_valid(cls, perm_name):
        if perm_name and perm_name in PermissionEnum.get_available_permissions():
            return True
        return False

    @staticmethod
    def endpoints_for_identity(identity):
        endpoints = list()
        for role in identity.roles.all():
            for permission in role.permissions.all():
                try:
                    with open(PermissionService.ep_conf_path) as file:
                        ep_conf_data = json.load(file)
                        endpoints.append(ep_conf_data[permission.name])
                except FileNotFoundError as error:
                    print("ERROR: FileNotFoundError\n{}".format(error))
                    raise error
                except PermissionError as error:
                    print("ERROR: PermissionError\n{}".format(error))
                    raise error
                except Exception as error:
                    raise error
        return endpoints

