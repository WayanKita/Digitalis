import datetime

from import_export import resources
from .models import Eleve


class EleveResource(resources.ModelResource):
    def after_import_instance(self, instance, new, **kwargs):
        if new:
            instance.user = kwargs['user']
            instance.date_ajout = datetime.datetime.now()
            instance.assure = False


    class Meta:
        model = Eleve
        import_id_fields = ('nom', 'prenom', 'date_de_naissance')
        exclude = ('id', 'assure', 'date_ajout', 'user')