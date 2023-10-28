import re
import textwrap

def menu():
    menu = """\n
     ======= MENU =======

         [d]\tDepositar
         [s]\tSacar
         [e]\tExtrato
         [nu]\tNovo Usuário
         [nc]\tNova Conta
         [lc]\tListar Contas
         [lu]\tListar Usuários
         [f]\tFim/Sair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n### Operação Falhou! - O Valor informado é inválido. ###")
    return saldo, extrato

def sacar(saldo, limite, numeroSaques, limiteSaques, extrato):
    valor = float(input("Informe o valor de saque: "))
    excedeuSaldo = valor > saldo
    excedeuLimite = valor > limite
    excedeuSaques = numeroSaques >= limiteSaques

    if excedeuSaldo:
        print("\n### Operação Falhou! - Você não possui saldo suficiente. ###")
    elif excedeuLimite:
        print("\n### Operação Falhou! - Você não possui limite de saque. ###")
    elif excedeuSaques:
        print("\n### Operação Falhou! - Número de saques diários excedido. ###")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numeroSaques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n### Operação Falhou! - O valor informado é inválido. ###")
    return saldo, extrato

def exibirExtrato(saldo, extrato):
    print("\n======= Extrato =======")
    print("Nenhuma movimentação foi feita." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("===========================")

def criarUsuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    # Validação do CPF com expressão regular
    if not re.match(r'^\d{11}$', cpf):
        print("\n### CPF inválido! Deve conter 11 dígitos. ###")
        return

    if filtrarUsuario(cpf, usuarios):
        print("\n### Já existe usuário com esse CPF! ###")
    else:
        nome = input("Informe o nome completo: ")
        dataNascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")

        # Validação da data de nascimento com expressão regular
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', dataNascimento):
            print("\n### Data de nascimento inválida! Deve estar no formato dd-mm-aaaa. ###")
            return

        endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")
        usuarios.append({"nome": nome, "dataNascimento": dataNascimento, "cpf": cpf, "endereco": endereco})
        print("=== Usuário criado com sucesso ===")

def filtrarUsuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criarConta(agencia, numeroConta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrarUsuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta Criada com Sucesso! ===")
        return {"agencia": agencia, "numeroConta": numeroConta, "usuario": usuario}
    
    print("\n### Usuário não encontrado, cadastre o usuário primeiro. ###")

def listarContas(contas):
    for conta in contas:
        print("\n======= Dados da Conta =======")
        print(f"Agência:\t{conta['agencia']}")
        print(f"C/C:\t\t{conta['numeroConta']}")
        print(f"Titular:\t{conta['usuario']['nome']}")
        print("==============================")

def listarUsuarios(usuarios):
    for usuario in usuarios:
        print("\n======= Dados do Usuário =======")
        print(f"Usuário:\t{usuario['nome']} \tCPF:\t{usuario['cpf']}")
        print("==============================")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numeroSaques = 0
    usuarios = []
    contas = []
    numeroConta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "s":
            saldo, extrato = sacar(saldo, limite, numeroSaques, LIMITE_SAQUES, extrato)

        elif opcao == "e":
            exibirExtrato(saldo, extrato)

        elif opcao == "nu":
            criarUsuario(usuarios)

        elif opcao == "nc":
            conta = criarConta(AGENCIA, numeroConta, usuarios)
            if conta:
                contas.append(conta)
                numeroConta += 1

        elif opcao == "lc":
            listarContas(contas)

        elif opcao == "lu":
            listarUsuarios(usuarios)

        elif opcao == "f":
            break

        else:
            print("Operação falhou! A opção informada é inválida.")

main()
