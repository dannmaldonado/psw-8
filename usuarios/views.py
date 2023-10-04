from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validação: As senhas devem ser iguais
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não são iguais')
            return redirect('/usuarios/cadastro')

        # Validação: A senha deve ter pelo menos 6 caracteres
        if len(senha) < 6:
            messages.error(request, 'Sua senha deve ter 6 ou mais caracteres')
            return redirect('/usuarios/cadastro')

        # Validação: Verifica se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso')
            return redirect('/usuarios/cadastro')

        # Validação: Verifica se o email já está cadastrado
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado')
            return redirect('/usuarios/cadastro')

        try:
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS,
                                 'Usuário salvo com sucesso')
        except:
            messages.add_message(request, constants.ERROR,
                                 'Erro interno do sistema, contate um administrator')
            return redirect('/usuarios/cadastro')
