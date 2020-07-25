import base64

from django.core.exceptions import ObjectDoesNotExist

from RBAC.models import Identity
from RBAC.services.RoleService import RoleService


class IdentityService:

    @staticmethod
    def create_identity(identity_data):
        if identity_data:
            # Added a bonus sample of base64 decoding of the password,
            # of course no base64 encode would ever be used by me to encode user password :)
            # It is possible for example to use the 'bcrypt' package to hash passwords
            identity = Identity.objects.create(
                name=identity_data['name'],
                password=base64.b64decode(identity_data['password'])
            )
            for role in identity_data['Roles']:
                IdentityService.add_role(identity, role['name'])
                print("Identity after adding role: {}".format(identity))
            return identity
        raise NameError

    @staticmethod
    def get_identity(iden_name):
        if iden_name:
            try:
                return Identity.objects.get(name=iden_name)
            except ObjectDoesNotExist as error:
                print("Error: username <{}> does not exist, details: \n{}"
                      .format(iden_name, error))
                raise error
        raise NameError

    @staticmethod
    def validate_credentials(identity, password):
        if str(identity.password) == str(base64.b64decode(password)):
            return 200
        print("Error: password is incorrect")
        return 401

    @classmethod
    def add_role(cls, identity, role_name):
        role = RoleService.get_role(role_name)
        identity.roles.add(role)
        identity.save()
