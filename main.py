import random
def saque(*, saldo, extrato, limite, numero_saque, limite_saque):

    if numero_saque >= limite_saque:
        print('\nLimite de saques diários atingindos. Seu limite será restaurado amanhã')
        return saldo, extrato, numero_saque
    
    try:
        valor = float(input("Informe o valor do saque R$: "))
        
        if valor <=0:
            print("Nenhum valor foi informado para saque")
        elif valor > saldo:
            print("Seu saldo é insuficiente para essa transação")
        elif valor > limite:
            print(f"Seu limite de saque é de {limite:.2f}\n")
        else:
            saldo -= valor
            extrato += f"Saque -R${valor}\n"
            numero_saque += 1
            print(f"\nSaque de {valor:.2f} realizado com sucesso!")
    
    except ValueError:
        print("\nValor inválido")

    return saldo, extrato, numero_saque

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: +R${valor:.2f}\n'
        print(f'Depósito de R${valor} realizado com sucesso!')
    else:
        print("\nOperação falhou!")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo: R${saldo:.2f}")
    

def criar_usuario(lista_clientes):
    print("\nBem-vindo(a) ao BiaBANK. Por favor, preencha os dados do novo cliente.")
    cpf = input("CPF: ")
    # Verifica se já existe
    for cliente in lista_clientes:
        if cliente["cpf"] == cpf:
            print("CPF já cadastrado. Não é possível duplicar clientes.")
            return
    nome = input('Nome completo: ').title()
    endereço = input("Endereço (logradouro - bairro - cidade/estado): ")
    
    cliente ={
            "nome": nome,
            "cpf": cpf,
            "endereço": endereço
        }
    lista_clientes.append(cliente)   
    print("Cliente cadastrado com sucesso!")
    
def criar_conta_corrente(agencia, numero_conta, lista_clientes, lista_contas):
    if not lista_clientes:
        print("\nNenhum cliente cadastrado. Crie um cliente antes de abrir uma conta.")
        return None
    
    cpf = input("Informe o CPF do cliente para vincular a uma nova conta: ")
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente["cpf"] == cpf:
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "cliente": cliente_encontrado,
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0
        }
        lista_contas.append(conta)
        print(f"\nConta Nº {numero_conta} criada com sucesso para o(a) cliente {cliente_encontrado['nome']}!")
        return conta
    else:
        print("\nCliente não encontrado. Verifique o CPF digitado.")
        return None

def main():
    AGENCIA = "0001"
    
    lista_clientes = []
    lista_contas = []

    while True:
        menu = """
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        opcao = input(menu)

        if opcao == "d":
            if lista_contas:
                conta_ativa = lista_contas[0] 
                try:
                    valor = float(input("Informe o valor do depósito: "))
                    conta_ativa["saldo"], conta_ativa["extrato"] = depositar(conta_ativa["saldo"], valor, conta_ativa["extrato"])
                except ValueError:
                    print("Valor de depósito inválido.")
            else:
                print("Nenhuma conta foi criada ainda.")

        elif opcao == "s":
            if lista_contas:
                conta_ativa = lista_contas[0]
                conta_ativa["saldo"], conta_ativa["extrato"], conta_ativa["numero_saques"] = saque(
                    saldo=conta_ativa["saldo"],
                    extrato=conta_ativa["extrato"],
                    limite=conta_ativa["limite"],
                    numero_saque=conta_ativa["numero_saques"],
                    limite_saque=conta_ativa["limite_saques"]
                )
            else:
                print("Nenhuma conta foi criada ainda.")

        elif opcao == "e":
            if lista_contas:
                conta_ativa = lista_contas[0]
                exibir_extrato(conta_ativa["saldo"], extrato=conta_ativa["extrato"])
            else:
                print("Nenhuma conta foi criada ainda.")

        elif opcao == "nu":
            criar_usuario(lista_clientes)

        elif opcao == "nc":
            numero_conta = len(lista_contas) + 1
            criar_conta_corrente(AGENCIA, numero_conta, lista_clientes, lista_contas)

        elif opcao == "lc":
            if not lista_contas:
                print("\nNenhuma conta cadastrada.")
            else:
                print("\n================ LISTA DE CONTAS ================")
                for conta in lista_contas:
                    linha = f"""
                        Agência:\t{conta['agencia']}
                        C/C:\t\t{conta['numero_conta']}
                        Titular:\t{conta['cliente']['nome']}
                    """
                    print(linha)
                print("================================================")


        elif opcao == "q":
            print("Obrigado por utilizar o BiaBANK. Volte sempre!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()