import graphene
from .models import *

class OfficeType(graphene.ObjectType):
    title = graphene.String()
    extension = graphene.String()
    phone = graphene.String()

    def resolve_title(self, info, **kwargs):
        try:
            return self.title
        except:
            return self["title"]

    def resolve_extension(self, info, **kwargs):
        try:
            return self.extension
        except:
            return self["extension"]

    def resolve_phone(self, info, **kwargs):
        try:
            return self.phone
        except:
            return self["phone"]