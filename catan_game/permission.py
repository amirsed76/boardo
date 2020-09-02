from rest_framework.permissions import BasePermission

from . import models


# class IsCompany(BasePermission):
#
#     def has_permission(self, request, view):
#         companies = models.Company.objects.filter(user = request.user)
#         if len(companies)==0:
#             return False
#         else:
#             return True
#
#     # def has_object_permission(self, request, view, obj):
#
