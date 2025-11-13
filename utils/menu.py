from controller import cliente_controller, betoneira_controller, alugueis_controller
from pesquisa import pesquisa
from utils import inputs_tratados
import time
from conexion import database

def pausar_e_limpar():
    input("\nPressione Enter para continuar...")

def exibir_tela_inicializacao():
    print("\n" + "="*43)
    print("   GERENCIADOR DE ALUGUEL DE BETONEIRAS")
    print("="*43)
    
    print("\nDesenvolvido por:")
    print("- Wagner Dos Santos")
    print("- Gabriel Rodrigo")
    print("- Micael Ribeiro")
    
    print("\n" + "-"*43)
    print("✅ Conectado ao MongoDB com sucesso!")
    print("-" * 43)
    pausar_e_limpar()

def gerenciar_betoneiras():
    while True:
        escolha_crud = input('''
========================================
      Gerenciamento de Betoneiras
========================================
[1] Adicionar Betoneira
[2] Listar Todas as Betoneiras
[3] Atualizar Dados (Modelo, Valor)
[4] Gerenciar Manutenção
[5] Remover Betoneira
[6] Voltar ao Menu Principal
----------------------------------------
Escolha uma opção: ''')
        
        match escolha_crud:
            case '1': adicionar_betoneira()
            case '2': pesquisa.listar_todas_betoneiras()
            case '3': atualizar_dados_betoneira()
            case '4': gerenciar_manutencao_betoneira()
            case '5': remover_betoneira()
            case '6': break
            case _: print("\n>> Opção inválida! Tente novamente.")
        
        if escolha_crud != '6':
            pausar_e_limpar()

def adicionar_betoneira():
    print("\n-- Adicionando Nova Betoneira --")
    modelo = inputs_tratados.modelo("Digite o modelo da betoneira: ")
    valor = inputs_tratados.valor("Digite o valor da diária (ex: 99.90): ")
    
    resultado = betoneira_controller.cadastrar_betoneira(modelo, valor)
    print(f"\n>> {resultado}")

def atualizar_dados_betoneira():
    print("\n-- Atualizando Dados da Betoneira --")
    pesquisa.listar_todas_betoneiras()
    try:
        id_bet = input("\nDigite o ID da betoneira para atualizar os dados: ")
        print("\n(Deixe em branco para não alterar)")
        
        novo_modelo = inputs_tratados.modelo("Novo modelo: ")
        
        novo_valor_str = input("Novo valor da diária: ")
        novo_valor = float(novo_valor_str) if novo_valor_str else None

        resultado = betoneira_controller.atualizar_dados_betoneira(id_bet, novo_modelo, novo_valor)
        print(f"\n>> {resultado}")

    except ValueError:
        print("\n>> Erro: ID ou valor inválido. Devem ser números.")
    except Exception as e:
        print(f"\n>> Erro inesperado: {e}")

def gerenciar_manutencao_betoneira():
    print("\n-- Gerenciar Manutenção da Betoneira --")
    pesquisa.listar_todas_betoneiras()
    try:
        id_bet = input("\nDigite o ID da betoneira para gerenciar a manutenção: ")
        
        opcao = input("Deseja [1] Colocar em manutenção ou [2] Retirar da manutenção? ")

        novo_status = ""
        if opcao == '1':
            novo_status = 'manutencao'
        elif opcao == '2':
            novo_status = 'disponivel'
        else:
            print("\n>> Opção inválida.")
            return

        resultado = betoneira_controller.atualizar_status_manutencao(id_bet, novo_status)
        print(f"\n>> {resultado}")

    except ValueError:
        print("\n>> Erro: ID inválido. Deve ser um número.")

def remover_betoneira():
    print("\n-- Removendo Betoneira --")
    pesquisa.listar_todas_betoneiras()
    try:
        id_bet = input("\nDigite o ID da betoneira que deseja remover: ")
        
        confirmacao = input(f"Tem certeza que deseja remover a betoneira ID {id_bet}? (s/n): ").lower()
        if confirmacao == 's':
            resultado = betoneira_controller.deletar_betoneira(id_bet)
            print(f"\n>> {resultado}")
        else:
            print("\n>> Operação cancelada.")
    except ValueError:
        print("\n>> Erro: ID inválido. Deve ser um número.")

def gerenciar_clientes():
    while True:
        escolha_crud = input('''
========================================
      Gerenciamento de Clientes
========================================
[1] Adicionar Cliente
[2] Listar Todos os Clientes
[3] Atualizar Dados
[4] Remover Cliente
[5] Voltar ao Menu Principal
----------------------------------------
Escolha uma opção: ''')
        
        match escolha_crud:
            case '1': adicionar_cliente()
            case '2': pesquisa.listar_todos_clientes()
            case '3': atualizar_cliente()
            case '4': remover_cliente()
            case '5': break
            case _: print("\n>> Opção inválida! Tente novamente.")
        
        if escolha_crud != '5':
            pausar_e_limpar()

def adicionar_cliente():
    print("\n-- Adicionando Novo Cliente --")
    nome = inputs_tratados.nome("Digite o nome do cliente: ")
    telefone = inputs_tratados.telefone("Digite o telefone (11 dígitos, ex: 27999998888): ")
    cpf = inputs_tratados.cpf("Digite o CPF: ")

    resultado = cliente_controller.cadastrar_cliente(nome, telefone, cpf)
    print(f"\n>> {resultado}")

def atualizar_cliente():
    print("\n-- Atualizando Cliente --")
    pesquisa.listar_todos_clientes()
    try:
        id_cli = input("\nDigite o ID do cliente que deseja atualizar: ")
        print("\n(Deixe em branco para não alterar)")
        novo_nome = inputs_tratados.nome("Novo nome: ")
        novo_telefone = inputs_tratados.telefone("Novo telefone: ")

        resultado = cliente_controller.atualizar_cliente(id_cli, novo_nome, novo_telefone)
        print(f"\n>> {resultado}")
    except ValueError:
        print("\n>> Erro: ID inválido. Deve ser um número.")

def remover_cliente():
    print("\n-- Removendo Cliente --")
    pesquisa.listar_todos_clientes()
    try:
        id_cli = input("\nDigite o ID do cliente que deseja remover: ")
        
        confirmacao = input(f"Tem certeza que deseja remover o cliente ID {id_cli}? (s/n): ").lower()
        if confirmacao == 's':
            resultado = cliente_controller.deletar_cliente(id_cli)
            print(f"\n>> {resultado}")
        else:
            print("\n>> Operação cancelada.")
    except ValueError:
        print("\n>> Erro: ID inválido. Deve ser um número.")

def registrar_novo_aluguel():
    print("\n-- Registrar Novo Aluguel --")
    pesquisa.listar_todos_clientes()
    try:
        id_cli = input("\nDigite o ID do Cliente: ")
        
        print("\n-- Betoneiras Disponíveis --")
        pesquisa.listar_betoneiras_disponiveis()
        id_bet = input("\nDigite o ID da Betoneira: ")
        
        data_inicio = inputs_tratados.data("Data de Início do Aluguel (DD/MM/AAAA): ")
        data_prevista = inputs_tratados.data("Data Prevista de Devolução (DD/MM/AAAA): ")

        resultado = alugueis_controller.registrar_aluguel(id_cli, id_bet, data_inicio, data_prevista)
        print(f"\n>> {resultado}")

    except ValueError:
        print("\n>> Erro: ID inválido. Deve ser um número.")

def registrar_devolucao():
    print("\n-- Registrar Devolução --")
    pesquisa.listar_alugueis_ativos()
    try:
        id_aluguel = input("\nDigite o ID do aluguel a ser finalizado: ")
        data_devolucao = inputs_tratados.data("Data de Devolução Efetiva (DD/MM/AAAA): ")

        resultado = alugueis_controller.finalizar_aluguel(id_aluguel, data_devolucao)
        print(f"\n>> {resultado}")
    except ValueError:
        print("\n>> Erro: ID inválido. Deve ser um número.")

def menu_pesquisas():
    while True:
        escolha = input('''
========================================
        Consultas e Pesquisas
========================================
[1] Listar Aluguéis Ativos
[2] Listar Betoneiras Disponíveis
[3] Histórico de Aluguéis (Todos)
[4] Voltar ao Menu Principal
----------------------------------------
Escolha uma opção: ''')
        match escolha:
            case '1': pesquisa.listar_alugueis_ativos()
            case '2': pesquisa.listar_betoneiras_disponiveis()
            case '3': pesquisa.historico_alugueis()
            case '4': break
            case _: print("\n>> Opção inválida.")
        
        if escolha != '4':
            pausar_e_limpar()

def menu():
    exibir_tela_inicializacao()

    while True:
        print("\n" + "="*43)
        print("             MENU PRINCIPAL")
        print("="*43)
        print("\n--- OPERAÇÕES ---")
        print("[1] Registrar Novo Aluguel")
        print("[2] Registrar Devolução")
        print("\n--- CADASTROS ---")
        print("[3] Gerenciar Clientes")
        print("[4] Gerenciar Betoneiras")
        print("\n--- PESQUISAS ---")
        print("[5] Consultas e Pesquisas")
        print("\n--- SISTEMA ---")
        print("[6] Sair")
        print("-"*43)
        
        escolha = input("Digite o número da opção desejada: ")
        
        match escolha:
            case '1': registrar_novo_aluguel(); pausar_e_limpar()
            case '2': registrar_devolucao(); pausar_e_limpar()
            case '3': gerenciar_clientes()
            case '4': gerenciar_betoneiras()
            case '5': menu_pesquisas()
            case '6':
                print("\nSaindo do sistema. Até logo!")
                break
            case _:
                print(f"\n>> ERRO: Opção '{escolha}' inválida. Tente novamente.")
                time.sleep(2)

