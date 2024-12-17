""" Neste módulo temos a implementação dos viewsets criadas na api"""
# pylint: disable=no-member, too-many-ancestors, too-many-return-statements
# Importações do Django REST framework
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.exceptions import NotAuthenticated
from django.core.exceptions import ObjectDoesNotExist

# Importações locais
from .models import Local, Evento, Custo
from .serializers import LocalSerializer, EventoSerializer, CustoSerializer


class LocalViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de Locais

        Fornece operações CRUD para locais, com acesso restrito ao usuário
        proprietário.
    """
    serializer_class = LocalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas locais do usuário autenticado"""
        try:
            return Local.objects.filter(usuario=self.request.user)
        except PermissionError as e:
            return Response({'Erro de Permissão':
                            str(e)}, status=status.HTTP_403_FORBIDDEN)
        except PermissionDenied as e:
            return Response({'Você não tem permissão': str(e)},
                            status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response({'Você não está autenticado ainda': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response({'Objeto não encontrado': str(e)},
                            status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"Valor inválido": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({"Faltando chave ou dado inválido": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Associa o usuário autenticado ao local durante a criação"""
        try:
            if not serializer.is_valid():
                raise ValidationError("Dados incompletos ou inválidos.")
            serializer.save(usuario=self.request.user)
        except ValidationError as ve:
            return Response({'Não foi possível validar este usuário': str(ve)},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({'Você não tem permissão para isto':
                            str(pe)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"Erro": "Dados de Local inválidos!"},
                            status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response({"Preenchimento incompleto."},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as pe:
            return Response({'Você não tem a permissão para executar':
                            str(pe)}, status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response({'Você não está autenticado ainda': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response({'Local não encontrado': str(e)},
                            status=status.HTTP_404_NOT_FOUND)


class EventoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de Eventos

    Fornece operações CRUD para eventos, com acesso restrito ao usuário
    proprietário.
    """
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas eventos do usuário autenticado"""
        try:  # erro normal
            return Evento.objects.filter(usuario=self.request.user)
        except PermissionError as e:
            return Response({'Você não tem permissão para executar isso':
                             str(e)}, status=status.HTTP_403_FORBIDDEN)
        except PermissionDenied as e:
            return Response({'Você não tem permissão para executar isto':
                             str(e)}, status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response({'Usuário não está autenticado': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response({'Evento não-encontrado': str(e)},
                            status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"Valor inválido": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({"Faltando chave ou dado inválido": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Associa o usuário autenticado ao evento durante a criação"""
        try:
            if not serializer.is_valid():
                raise ValidationError("Dados incompletos ou inválidos.")
            serializer.save(usuario=self.request.user)
        except ValidationError as ve:
            return Response({'Não foi possível validar este usuário': str(ve)},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({'Você não tem permissão para executar':
                            str(pe)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"Erro": "Dados inválidos!"},
                            status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response({"Erro": "Algum dado faltando ou incorreto."},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as pe:
            return Response({'Você não tem permissão': str(pe)},
                            status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response({'Usuário não está autenticado': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response({'Evento não encontrado': str(e)},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'], url_path="custos")
    def calcular_custos(self, request):  # ignorar
        """Endpoint personalizado para calcular custos totais do evento

        Retorna uma lista de custos e o valor total acumulado.
        """
        try:
            evento = self.get_object()
            if not evento:
                return Response(
                    {'error': 'Evento não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            custos = Custo.objects.filter(evento=evento)  # pode ignorar
            if not custos.exists():
                return Response(
                    {'message': 'Nenhum custo associado a este evento.'},
                    status=status.HTTP_200_OK
                )
            total = sum(custo.valor for custo in custos)
            custo_serializer = CustoSerializer(custos, many=True,
                                               context={'request': request})

            return Response(
                {'custos': custo_serializer.data, 'total': total},
                status=status.HTTP_200_OK
            )
        except Evento.DoesNotExist:  # pode ignorar
            return Response(
                {'error': 'Evento não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionError as pe:
            return Response({'Você não tem permissão para executar':
                            str(pe)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as ve:
            return Response({'Não foi possível validar este evento': str(ve)},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as pe:
            return Response({'Você não tem permissão para calcular': str(pe)},
                            status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response({'Você não está autenticado': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as ve:
            return Response({'Dados inválidos!': str(ve)},
                            status=status.HTTP_409_CONFLICT)
        except KeyError as ke:
            return Response({"Algum dado faltando ou errado.": str(ke)},
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({'Evento não encontrado': str(e)},
                            status=status.HTTP_404_NOT_FOUND)


class CustoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de Custos

    Fornece operações CRUD para custos, com acesso restrito aos custos
    dos eventos do usuário autenticado.
    """
    serializer_class = CustoSerializer
    queryset = Custo.objects.all()  # pode ignorar
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas custos dos eventos do usuário autenticado"""
        try:  # pode ignorar esse
            return Custo.objects.filter(evento__usuario=self.request.user)
        except PermissionError as e:
            return Response({'Você não tem permissão para executar esta ação':
                            str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"Erro": "Dados inválidos!"},
                            status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response({"Erro": "Algum dado faltando ou errado."},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'Você não tem permissão para executar esta ação':
                            str(e)}, status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response({'Você não está autenticado': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response({'Custo ou evento não encontrado': str(e)},
                            status=status.HTTP_404_NOT_FOUND)
