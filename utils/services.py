from django.db.models import Max


def generate_code(model, diff, org):
    code = model.objects.filter(
        organization=org
    ).aggregate(Max('code', default=0))['code__max'] + diff
    return code
