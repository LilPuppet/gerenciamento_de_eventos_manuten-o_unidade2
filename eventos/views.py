""" Neste módulo temos a implementação dos viewsets criadas na api"""
# Importações do Django REST framework
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

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
        try:  # esse erro é normal e deve ser ignorado
            return Local.objects.filter(usuario=self.request.user)  
        except PermissionError as e:
            return Response({'Você não tem permissão para executar esta ação':
                            str(e)}, status=status.HTTP_403_FORBIDDEN)
            # Temos que por excessões mais específicas

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
            return Response({'Você não tem permissão para executar esta ação':
                            str(pe)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"Erro": "Dados inválidos!"},
                            status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response({"Erro": "Algum dado faltando ou errado."},
                            status=status.HTTP_400_BAD_REQUEST)
            # Temos que por excessões mais específicas


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
            return Response({'Você não tem permissão para executar esta ação':
                             str(e)}, status=status.HTTP_403_FORBIDDEN)
            # Temos que por excessões mais específicas

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
            return Response({'Você não tem permissão para executar esta ação':
                            str(pe)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"Erro": "Dados inválidos!"},
                            status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response({"Erro": "Algum dado faltando ou errado."},
                            status=status.HTTP_400_BAD_REQUEST)
            # Temos que por excessões mais específicas

    @action(detail=True, methods=['GET'], url_path="custos")
    def calcular_custos(self, request, pk=None):  # ignorar
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
            return Response({'Você não tem permissão para executar esta ação':
                            str(pe)}, status=status.HTTP_403_FORBIDDEN)
            # Temos que por excessões mais específicas


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
            # Temos que por excessões mais específicas
