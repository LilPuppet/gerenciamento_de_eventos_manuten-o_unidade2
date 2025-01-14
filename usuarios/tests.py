"""Testes do Sistema"""
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from eventos.models import Local, Evento
# pylint: disable=no-member


class UsuarioAPITests(TestCase):
    """Essa classe de testes foca nos testes dos usuários"""
    def setUp(self):
        # Configura um cliente de API para enviar requisições
        self.client = APIClient()
        self.url_usuarios = "http://127.0.0.1:8000/api/usuarios/"
        self.user_data = {
            "username": "joaosilva",
            "cpf": "123.456.789-10",
            "email": "joao.silva@exemplo.com",
            "password": "Senha@123",
            "first_name": "João",
            "last_name": "Silva"
        }

    def test_criar_usuario_sucesso(self):
        """
            Este teste tenta criar um usuário, enviando um post para a url,
            checando o status 201_created e se os dados batem.
        """
        response = self.client.post(self.url_usuarios, self.user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["first_name"],
                         self.user_data["first_name"])
        self.assertEqual(response.data["last_name"],
                         self.user_data["last_name"])

    def test_listar_usuarios(self):
        """
            Esse teste tenta listar os usuários, ele cria um usuário
            e tenta listar o usuário criado com o metodo GET
        """
        self.client.post(self.url_usuarios, self.user_data, format='json')
        response = self.client.get(self.url_usuarios, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Ao menos um?

    def test_buscar_usuario_por_id(self):
        """
            Este teste cria o usuário, pega o ID dele e faz
            a busca do usuário criado em questão.
            Além disso checa se os dados batem.
        """
        usuario_criado = self.client.post(self.url_usuarios,
                                          self.user_data, format='json')
        user_id = usuario_criado.data.get("id")
        response = self.client.get(f"{self.url_usuarios}{user_id}/",
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["first_name"],
                         self.user_data["first_name"])
        self.assertEqual(response.data["last_name"],
                         self.user_data["last_name"])

    def test_atualizacao_parcial_usuario(self):
        """
            Este teste cria o usuário, pega o ID dele e faz
            a alteração parcial do usuário criado em questão.
            Além disso checa se os dado alterado bate.
        """
        usuario_criado = self.client.post(self.url_usuarios,
                                          self.user_data, format='json')
        user_id = usuario_criado.data.get("id")
        dado_novo = {"email": "joao.novo@exemplo.com"}  # Dado novo
        response = self.client.patch(f"{self.url_usuarios}{user_id}/",
                                     dado_novo, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], dado_novo["email"])

    def test_atualizacao_total_usuario(self):
        """
            Este teste cria o usuário, pega o ID dele e faz
            a alteração total do usuário criado em questão.
            Além disso checa se os dados alterados batem.
        """
        usuario_criado = self.client.post(self.url_usuarios,
                                          self.user_data, format='json')
        user_id = usuario_criado.data.get("id")
        dados_novos = {
            "username": "mariosilva",
            "cpf": "987.654.321-00",
            "email": "mario.silva@exemplo.com",
            "password": "NovaSenha@123",
            "first_name": "Mario",
            "last_name": "Silva"
        }
        response = self.client.put(f"{self.url_usuarios}{user_id}/",
                                   dados_novos, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], dados_novos["username"])
        self.assertEqual(response.data["email"], dados_novos["email"])
        self.assertEqual(response.data["first_name"],
                         dados_novos["first_name"])
        self.assertEqual(response.data["last_name"],
                         dados_novos["last_name"])

    def test_deletar_usuario(self):
        """
            Esse teste cria um usuário, depois deleta ele e verifica foi,
            no caso mostra o status 204
        """
        usuario_criado = self.client.post(self.url_usuarios, self.user_data,
                                          format='json')
        user_id = usuario_criado.data.get("id")
        response = self.client.delete(f"{self.url_usuarios}{user_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response_pos_lixim = self.client.get(f"{self.url_usuarios}{user_id}/")
        self.assertEqual(response_pos_lixim.status_code,
                         status.HTTP_404_NOT_FOUND)


# -----------------------------------------------------------------------------------


class LocalAPITests(APITestCase):
    """Testes para Locais com autenticação do usuário"""

    def setUp(self):
        self.client = APIClient()
        usuario = get_user_model()
        self.user = usuario.objects.create_user(
            username="usuario_teste",
            password="Senha@123",
            cpf="123.456.789-00",
            email="usuario_teste@example.com"
        )
        self.client.force_authenticate(user=self.user)
        self.url_locais = "http://127.0.0.1:8000/api/locais/"
        self.local_data = {
            "nome": "Centro de Convenções",
            "logradouro": "Rua Principal",
            "numero": 123,
            "bairro": "Centro",
            "cidade": "Cidade X",
            "estado": "Estado Y",
            "cep": "12345-678",
            "capacidade": 500,
        }
        response = self.client.post(self.url_locais, self.local_data,
                                    format='json')
        self.local_id = response.data["id"]

    def test_criar_local_sucesso(self):
        """Teste para criação de local autenticado"""
        response = self.client.post(self.url_locais, self.local_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], self.local_data["nome"])

    def test_listar_locais_autenticado(self):
        """Teste para listar locais do usuário autenticado"""
        response = self.client.get(self.url_locais, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_criar_local_sem_autenticacao(self):
        """Teste de falha ao criar local sem autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url_locais, self.local_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_atualizar_local_put(self):
        """Teste para atualizar um local usando PUT"""
        updated_data = self.local_data.copy()
        updated_data["nome"] = "Centro Atualizado"
        url = f"{self.url_locais}{self.local_id}/"
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], updated_data["nome"])

    def test_atualizar_local_patch(self):
        """Teste para atualizar parcialmente um local usando PATCH"""
        url = f"{self.url_locais}{self.local_id}/"
        response = self.client.patch(url, {"nome":
                                           "Centro Parcialmente Atualizado"},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"],
                         "Centro Parcialmente Atualizado")

    def test_deletar_local(self):
        """Teste para deletar um local"""
        url = f"{self.url_locais}{self.local_id}/"
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verifica se o local foi realmente excluído
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EventoAPITests(APITestCase):
    """Testes para Eventos com autenticação do usuário"""

    def setUp(self):
        self.client = APIClient()
        usuario = get_user_model()
        self.user = usuario.objects.create_user(
            username="usuario_teste",
            password="Senha@123",
            cpf="123.456.789-00",
            email="usuario_teste@example.com"
        )
        self.client.force_authenticate(user=self.user)
        self.local = Local.objects.create(
            nome="Centro de Convenções",
            logradouro="Rua Principal", numero=123,
            bairro="Centro", cidade="Cidade X", estado="Estado Y",
            cep="12345-678", capacidade=500, usuario=self.user
        )
        self.url_eventos = "http://127.0.0.1:8000/api/eventos/"
        self.evento_data = {
            "titulo": "Evento de Teste",
            "descricao": "Descrição do evento",
            "orcamento": "1000.00",
            "status": "PLANEJADO",
            "dataInicio": "2024-12-25T10:00:00Z",
            "dataFim": "2024-12-25T18:00:00Z",
            "local": self.local.id,
        }
        response = self.client.post(self.url_eventos, self.evento_data,
                                    format='json')
        self.evento_id = response.data["id"]

    def test_atualizar_evento_put(self):
        """Teste para atualizar um evento usando PUT"""
        updated_data = self.evento_data.copy()
        updated_data["titulo"] = "Evento Atualizado"
        url = f"{self.url_eventos}{self.evento_id}/"
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titulo"], updated_data["titulo"])

    def test_atualizar_evento_patch(self):
        """Teste para atualizar parcialmente um evento usando PATCH"""
        url = f"{self.url_eventos}{self.evento_id}/"
        response = self.client.patch(url, {"titulo":
                                           "Evento Parcialmente Atualizado"},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titulo"],
                         "Evento Parcialmente Atualizado")

    def test_deletar_evento(self):
        """Teste para deletar um evento"""
        url = f"{self.url_eventos}{self.evento_id}/"
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verifica se o evento foi realmente excluído
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustoAPITests(APITestCase):
    """Testes para Custos com autenticação do usuário"""

    def setUp(self):
        self.client = APIClient()
        usuario = get_user_model()
        self.user = usuario.objects.create_user(
            username="usuario_teste",
            password="Senha@123",
            cpf="123.456.789-00",
            email="usuario_teste@example.com"
        )
        self.client.force_authenticate(user=self.user)
        self.local = Local.objects.create(
            nome="Centro de Convenções",
            logradouro="Rua Principal", numero=123,
            bairro="Centro", cidade="Cidade X", estado="Estado Y",
            cep="12345-678", capacidade=500, usuario=self.user
        )
        self.evento = Evento.objects.create(
            titulo="Evento de Teste", descricao="Descrição do evento",
            orcamento=1000.00,
            status="PLANEJADO", dataInicio="2024-12-25T10:00:00Z",
            dataFim="2024-12-25T18:00:00Z",
            local=self.local, usuario=self.user
        )
        self.url_custos = "http://127.0.0.1:8000/api/custos/"
        self.custo_data = {
            "descricao": "Aluguel de equipamentos",
            "valor": "500.00",
            "evento": self.evento.id,
        }
        response = self.client.post(self.url_custos, self.custo_data,
                                    format='json')
        self.custo_id = response.data["id"]

    def test_atualizar_custo_put(self):
        """Teste para atualizar um custo usando PUT"""
        updated_data = self.custo_data.copy()
        updated_data["descricao"] = "Equipamentos Atualizados"
        url = f"{self.url_custos}{self.custo_id}/"
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["descricao"], updated_data["descricao"])

    def test_atualizar_custo_patch(self):
        """Teste para atualizar parcialmente um custo usando PATCH"""
        url = f"{self.url_custos}{self.custo_id}/"
        response = self.client.patch(url, {"descricao": "Custo Parcial"},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["descricao"], "Custo Parcial")

    def test_deletar_custo(self):
        """Teste para deletar um custo"""
        url = f"{self.url_custos}{self.custo_id}/"
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verifica se o custo foi realmente excluído
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)