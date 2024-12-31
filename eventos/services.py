"""Serviços para a criação adequada dos eventos"""
# pylint: disable=no-member
from rest_framework.exceptions import ValidationError
from .models import Local, Evento, Custo


def get_user_locals(user):
    """Pegando os locais de um usuário"""
    try:
        return Local.objects.filter(usuario=user)
    except Exception as e:
        raise e


def create_local(data, user):
    """Criando o local atrelado ao usuário"""
    if not data.is_valid():
        raise ValidationError("Dados incompletos ou invalidos.")
    data.save(usuario=user)


def get_user_eventos(user):
    """Pegando os eventos do usuário"""
    try:
        return Evento.objects.filter(usuario=user)
    except Exception as e:
        raise e


def create_evento(data, user):
    """Criando o evento atrelado ao usuário e ao local"""
    if not data.is_valid():
        raise ValidationError("Dados incompletos ou invalidos.")
    data.save(usuario=user)


def calcular_custos(evento):
    """Calculo dos custos"""
    try:
        custos = Custo.objects.filter(evento=evento)
        if not custos.exists():
            return {"message": "Nenhum custo associado a este evento.",
                    "custos": [], "total": 0}

        total = sum(custo.valor for custo in custos)
        return {"custos": custos, "total": total}
    except Exception as e:
        raise e


def get_user_custos(user):
    """Pegando os custos de um evento de um usuário"""
    try:
        return Custo.objects.filter(evento__usuario=user)
    except Exception as e:
        raise e
