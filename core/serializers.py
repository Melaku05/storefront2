from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta): # inherit everything from base class(djoser) and the override specfic field
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        