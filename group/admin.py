from django.contrib import admin
from models import *


class GroupBranchAdmin(admin.ModelAdmin):
    pass
admin.site.register(GroupBranch, GroupBranchAdmin)


# class UserGroupAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(UserGroup, UserGroupAdmin)