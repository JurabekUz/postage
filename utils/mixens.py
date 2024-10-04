from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT


class ArchiveMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        return Response(status=HTTP_204_NO_CONTENT)


class AutoOrgSetMixin:

    def perform_create(self, serializer):
        serializer.validated_data['organization_id'] = self.request.user.org_id
        serializer.save()


class SelectMixin:

    @action(detail=False, methods=['GET'], url_path='select')
    def select(self, request):
        queryset = self.get_queryset().values('id', 'name')
        return Response(queryset)


class OrgFilterMixin:

    def get_queryset(self):
        return self.queryset.filter(organization_id=self.request.user.org_id)