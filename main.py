from abc import ABC, abstractmethod
from datetime import datetime

# ----------------------------
# Cliente e Pessoa Física
# ----------------------------
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __repr__(self):
        return f"<PessoaFisica: {self.nome}, CPF: {self.cpf}>"


# ----------------------------
# Conta e Conta Corrente
# ----------------------------
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        elif valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        self._saldo -= valor
        transacao = Saque(valor)
        self.historico.adicionar_transacao(transacao)
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor de depósito deve ser positivo. @@@")
            return False
        
        self._saldo += valor
        transacao = Deposito(valor)
        self.historico.adicionar_transacao(transacao)
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        # Filtra as transações para contar apenas os saques de hoje
        hoje = datetime.now().date()
        saques_hoje = [
            t for t in self.historico.transacoes 
            if t['tipo'] == Saque.__name__ and t['data'].date() == hoje
        ]
        numero_saques = len(saques_hoje)

        if valor > self.limite:
            print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f}. @@@")
            return False
        elif numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")
            return False
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# ----------------------------
# Histórico de Transações
# ----------------------------
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(),
            }
        )


# ----------------------------
# Transações abstratas e concretas
# ----------------------------
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    # O método registrar foi removido para simplificar o fluxo
    # @abstractmethod
    # def registrar(self, conta):
    #     pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

# ===================================================================
# FUNÇÕES DE INTERAÇÃO DO SISTEMA
# ===================================================================

def menu():
    menu_text = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(menu_text).lower()


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        conta.depositar(valor)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        conta.sacar(valor)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            tipo = transacao['tipo']
            valor = transacao['valor']
            data = transacao['data'].strftime("%d-%m-%Y %H:%M:%S")
            print(f"{data} - {tipo}:\n\tR$ {valor:.2f}")

    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    print("\n================ LISTA DE CONTAS ================")
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print("*" * 20)
            print(str(conta))
    print("==================================================")


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("\nSaindo do sistema... Obrigado por usar nossos serviços!")
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# --- Ponto de entrada do programa ---
if __name__ == "__main__":
    main()