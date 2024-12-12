# Importações necessárias do Django REST framework
from rest_framework import serializers
from .models import Local, Evento, Custo

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = "__all__"
        read_only_fields = ['usuario']

class EventoSerializer(serializers.ModelSerializer):
    local = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.none()
    )
    
    class Meta:
        model = Evento
        fields = "__all__"
        read_only_fields = ['usuario']

    def __init__(self, *args, **kwargs):
        """Inicializa o serializer com filtro de locais por usuário"""
        super().__init__(*args, **kwargs)
        # Limita os locais ao usuário autenticado para segurança
        user = self.context['request'].user
        self.fields['local'].queryset = Local.objects.filter(usuario=user)

    def validate(self, data):
        """Valida se a data de término é posterior à data de início"""
        if data['dataFim'] < data['dataInicio']:
            raise serializers.ValidationError("A data de término não pode ser antes da data de início.")
        return data

class CustoSerializer(serializers.ModelSerializer):
    evento = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.none()
    )

    class Meta:
        model = Custo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """Inicializa o serializer com filtro de eventos por usuário"""
        super().__init__(*args, **kwargs)
        # Limita os eventos ao usuário autenticado para segurança
        user = self.context['request'].user
        self.fields['evento'].queryset = Evento.objects.filter(usuario=user)