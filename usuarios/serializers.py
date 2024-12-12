from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'cpf', 'email', 'password'
        ]

    def create(self, validated_data):
        # Extrai a senha dos dados validados
        password = validated_data.pop('password')

        # Cria instância do usuário com os dados restantes
        user = Usuario(**validated_data)
        user.set_password(password)  # Criptografa a senha
        user.save()
        return user