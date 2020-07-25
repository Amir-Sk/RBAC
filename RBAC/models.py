from django.db import models


class Permission(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return '<Permission: name: {}>'.format(self.name)


class Role(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, null=False)
    permissions = models.ManyToManyField(Permission, default=[])

    def __str__(self):
        return '<Role: {}\n Permissions: {}\n >'.format(self.name, self.permissions.all())


class Identity(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=30, null=False)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return '<Identity: Assigned Roles: {} , Password: {}>'\
            .format(self.roles.all(), self.password)
