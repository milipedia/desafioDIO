
def menu_bancario():
    print("Olá, bem-vindo ao BiaBANK!")
    print("D > Depósito")
    print("S > Saque")
    print("E > Extrato")
    print("F > Sair")
    
    deposito = 0.0
    LIMITE_SAQUES = 3
    saques_realizados = 0    

    while True:
        opcao = input("Escolha uma opção: ").upper().strip()

        if opcao == "D":
            try:
                valor = float(input("Informe o valor do depósito: "))
                if  valor <= 0:
                    print("Nenhum valor foi informado para depósito.")
                else:
                    deposito += (valor)
                    print(f"Depósito de R${valor} realizado com sucesso!")
            except ValueError:
                print("Valor inválido. Por favor, informe um número válido.")

        elif opcao == "S":
            if saques_realizados >= LIMITE_SAQUES:
                print("Limite de saques diários atingido. Tente novamente amanhã.")
                continue

            try:
                valor = float(input("Informe o valor do saque: "))
                if  valor <= 0:
                    print("Nenhum valor foi informado para saque.")
                elif valor > deposito:
                    print("Saldo insuficiente para saque.")
                elif valor > 500:
                    print("Seu limite para esse tipo de transação é de R$500.")
                else:
                    deposito -= valor
                    saques_realizados += 1
                    print(f"Saque de R${valor} realizado com sucesso!")
            except ValueError:
                print("Valor inválido. Por favor, informe um número válido.")

            if saques_realizados > LIMITE_SAQUES:
                print("Limite de saques diários atingido. Tente novamente amanhã.")

        elif opcao == "E":
            print(f"""---- Extrato ---
                  Depósitos realizados: R${deposito:.2f}
                  Saques realizados: {saques_realizados}
                  Saldo atual: R${deposito:.2f} 
        """)

        elif opcao == "F":
            print("Obrigado por usar o BiaBANK! Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
menu_bancario()