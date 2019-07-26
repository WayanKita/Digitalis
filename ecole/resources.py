from import_export import resources
from .models import Eleve


class EleveResource(resources.ModelResource):
    class Meta:
        model = Eleve