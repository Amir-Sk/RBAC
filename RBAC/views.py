import yaml
from django.http import HttpResponse, JsonResponse

from RBAC.services.IdentityService import IdentityService
from RBAC.services.PermissionService import PermissionService
from RBAC.services.RoleService import RoleService


def index(request):
    return HttpResponse("Welcome to the RBAC index.html")


class ViewService:

    @staticmethod
    def authenticate_identity(request):
        status = 200
        json_payload = {}
        try:
            data = request.POST
            identity = IdentityService.get_identity(data['name'])
            status = IdentityService.validate_credentials(identity, data['password'])
            if status == 200:
                endpoints = PermissionService.endpoints_for_identity(identity)
                json_payload = {"endpoints": endpoints}
                # payload = json.dumps(json_payload)
        except Exception as error:
            print("Some higher level exception handling + logging, details:\n{}"
                  .format(error))
        return JsonResponse(json_payload, status=status)


class ConfigurationView:

    error_text = "ERROR:\nEncountered exception - " \
                 "Handling should be done here before" \
                 "returning to controller, details:\n{}"

    # Usually config file would be defined in a higher
    # level according to Env properties(Production/Staging etc.) and would
    # include file paths etc.
    def __init__(self, config_file_path='./RBAC/configurations/config.yaml'):
        self.config_file_path = config_file_path

    @staticmethod
    def parse_file():
        conf_view = ConfigurationView()
        try:
            with open(conf_view.config_file_path) as file:
                config_data = yaml.safe_load(file)
                conf_view.register_permissions(config_data['Permissions'])
                # conf_view.register_endpoints_to_permission()  # config_data['Endpoints'])
                conf_view.register_roles(config_data['Roles'])
                conf_view.register_identities(config_data['Identities'])
                print(config_data)
        except FileNotFoundError as err:
            print("ERROR: FileNotFoundError\n{}".format(err))
        except PermissionError as err:
            print("ERROR: PermissionError\n{}".format(err))
        except Exception as err:
            print(ConfigurationView.error_text.format(err))

    @classmethod
    def register_permissions(cls, data):
        for perm in data:
            try:
                permission = PermissionService.create_permission(perm['name'])
                print("register_roles, permission created: \n{}".format(permission))
            except Exception as err:
                print(ConfigurationView.error_text.format(err))

    # def register_endpoints_to_permission(self, data):
    #     for perm in data:
    #         try:
    #             PermissionService.add_endpoint_to_permission(perm)
    #         except Exception as err:
    #             print(ConfigurationView.error_text.format(err))

    def register_roles(self, data):
        for role in data:
            try:
                role = RoleService.create_role(role)
                print("register_roles, role created: \n{}".format(role))
            except Exception as err:
                print(ConfigurationView.error_text.format(err))

    def register_identities(self, data):
        for identity_data in data:
            try:
                identity = IdentityService.create_identity(identity_data)
                print("register_identities, identity_data created: \n{}".format(identity))
            except Exception as err:
                print(ConfigurationView.error_text.format(err))

# ConfigurationView.parse_file()
