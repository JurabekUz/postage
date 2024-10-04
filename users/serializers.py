from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserFullNameSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_user_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'last_name']

    def get_user_full_name(self, obj):
        return obj.get_full_name()


class MeSerializer(serializers.ModelSerializer):
    branch__name = serializers.CharField(source='branch.name', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'branch__name']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        del data["refresh"]
        data["access"] = str(refresh.access_token)
        data["full_name"] = self.user.get_full_name()
        data['is_staff'] = self.user.is_staff

        # remove update last login feature
        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return data
