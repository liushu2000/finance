from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# from pricing.models import Policy_Collection


class GroupBranchManager(models.Manager):

    @property
    def groups(self):
        return self.get_query_set().filter(parent__isnull=True)

    @property
    def branches(self):
        return self.get_query_set().filter(parent__isnull=False)

    @property
    def branchesingroup(self):
        return self.get_query_set().filter(parent=self)


class GroupBranch(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', blank=True, null=True,)
    type = models.CharField(blank=True, null=True, max_length=20)
    phone = models.CharField(_('Phone'), blank=True, null=True, max_length=20)
    address = models.CharField(_('Address'), blank=True, null=True, max_length=150)
    #policy_collection = models.ForeignKey(Policy_Collection, blank=True, null=True,)
    objects = GroupBranchManager()

    def __unicode__(self):
        return self.name

    def get_branches(self):
        return self.objects.filter(parent=self)

# class Entity(models.Model):
#     name = models.CharField(max_length=20)
#     parent = models.ForeignKey('self', blank=True, null=True,)
#     type = models.CharField(blank=True, null=True, max_length=20)
#     phone = models.CharField(_('Phone'), blank=True, null=True, max_length=20)
#     address = models.CharField(_('Address'), blank=True, null=True, max_length=150)
#
#     def __unicode__(self):
#         return self.name