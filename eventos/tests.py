from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from eventos.models import Local, Evento
from faker import Faker
from random import randint

# pylint: disable=no-member

# Inicializa o Faker com a localidade 'pt_BR'
fake = Faker('pt_BR')


class UsuarioFactory:
    """Classe Factory para criar dados falsos de usuários."""
    
    @staticmethod
    def gerar_usuario():
        """Gera um usuário com dados aleatórios, incluindo um CPF válido."""
        cpf = fake.cpf()
        return {
            "username": fake.user_name(),
            "cpf": cpf,
            "email": fake.email(),
            "password": "Senha@123",  # A senha pode ser fixa ou gerada aleatoriamente
            "first_name": fake.first_name(),
            "last_name": fake.last_name()
        }


class UsuarioAPITests(TestCase):
    """Essa classe de testes foca nos testes dos usuários"""
    
    def setUp(self):
        # Configura um cliente de API para enviar requisições
        self.client = APIClient()
        self.url_usuarios = "http://127.0.0.1:8000/api/usuarios/"
        self.user_data = UsuarioFactory.gerar_usuario()  # Gera dados falsos de um usuário

    def test_criar_usuario_sucesso(self):
        """
            Este teste tenta criar um usuário, enviando um post para a url,
            checando o status 201_created e se os dados batem.
        """
        response = self.client.post(self.url_usuarios, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["first_name"], self.user_data["first_name"])
        self.assertEqual(response.data["last_name"], self.user_data["last_name"])

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
        usuario_criado = self.client.post(self.url_usuarios, self.user_data, format='json')
        user_id = usuario_criado.data.get("id")
        response = self.client.get(f"{self.url_usuarios}{user_id}/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["first_name"], self.user_data["first_name"])
        self.assertEqual(response.data["last_name"], self.user_data["last_name"])

    def test_atualizacao_parcial_usuario(self):
        """
            Este teste cria o usuário, pega o ID dele e faz
            a alteração parcial do usuário criado em questão.
            Além disso checa se o dado alterado bate.
        """
        usuario_criado = self.client.post(self.url_usuarios, self.user_data, format='json')
        user_id = usuario_criado.data.get("id")
        dado_novo = {"email": fake.email()}  # Dado novo
        response = self.client.patch(f"{self.url_usuarios}{user_id}/", dado_novo, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], dado_novo["email"])

    def test_atualizacao_total_usuario(self):
        """
            Este teste cria o usuário, pega o ID dele e faz
            a alteração total do usuário criado em questão.
            Além disso checa se os dados alterados batem.
        """
        usuario_criado = self.client.post(self.url_usuarios, self.user_data, format='json')
        user_id = usuario_criado.data.get("id")
        dados_novos = UsuarioFactory.gerar_usuario()  # Gera novos dados
        response = self.client.put(f"{self.url_usuarios}{user_id}/", dados_novos, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], dados_novos["username"])
        self.assertEqual(response.data["email"], dados_novos["email"])
        self.assertEqual(response.data["first_name"], dados_novos["first_name"])
        self.assertEqual(response.data["last_name"], dados_novos["last_name"])

    def test_deletar_usuario(self):
        """
            Esse teste cria um usuário, depois deleta ele e verifica se foi,
            no caso mostra o status 204
        """
        usuario_criado = self.client.post(self.url_usuarios, self.user_data, format='json')
        user_id = usuario_criado.data.get("id")
        response = self.client.delete(f"{self.url_usuarios}{user_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response_pos_lixim = self.client.get(f"{self.url_usuarios}{user_id}/")
        self.assertEqual(response_pos_lixim.status_code, status.HTTP_404_NOT_FOUND)
