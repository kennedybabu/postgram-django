from rest_framework import serializers 

from core.user.models import User
from core.user.serializers import UserSerializer 


class RegisterSerializer(UserSerializer):
    """
    Reg serializer for requests and user creation
    """

    # Making sure the password is at least 8 char long, 
    # and no longer than 128 and cant by the user

    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User

        #list of all the fields that can be included in a req or a response
        #, 'avatar'
        fields = ['id', 'bio', 'email', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        #use the `create_user` method to create a new user
        return User.objects.create_user(**validated_data)

