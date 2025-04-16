import os, time, locale

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')  
LIM_SAQUE_DIARIO = 3
LIM_SAQUE_OPERACAO = 500

usuarios = list()
usuario_logado = dict()

contador_contas = 1 # Contador de contas

def depositar(operacao=0):
    global usuario_logado
    while True:
        try:
            deposito = input("\n[c] Cancelar operação\nValor: ").strip()
            if deposito in 'cC':
                print("Operação Cancelada!\n")
                break
            deposito = float(deposito)
            assert deposito > 0
            usuario_logado['contas'][operacao]['saldo'] += deposito
            usuario_logado['contas'][operacao]['extrato'] += f"\t+ {locale.currency(deposito)}\n"
            break
        except ValueError:
            print("Valor informado é inválido! Informe um valor numérico e tente novamente...")
            time.sleep(0.5)
        except AssertionError:
            print("Valor informado é inválido! Informe um valor maior que zero e tente novamente...")
            time.sleep(0.5)

def sacar(operacao=0):
    while True:
        if usuario_logado['contas'][operacao]['num_saques'] != LIM_SAQUE_DIARIO:
            try:
                saque = input("\n[c] Cancelar operação\nValor: ").strip()
                if saque in 'cC':
                    print("Operação Cancelada!\n")
                    break
                saque = float(saque)
                assert saque > 0
                assert saque <= 500
                if usuario_logado['contas'][operacao]['saldo'] >= saque:
                    usuario_logado['contas'][operacao]['num_saques'] += 1
                    usuario_logado['contas'][operacao]['saldo'] -= saque
                    usuario_logado['contas'][operacao]['extrato'] += f"\t- {locale.currency(saque)}\n"
                    break
                else:
                    print("Saldo insuficiente para realizar o saque!")
                    time.sleep(0.5)
            except ValueError:
                print("Valor informado é inválido! Informe um valor numérico e tente novamente...")
                time.sleep(0.5)
            except AssertionError:
                print("Valor informado é inválido! Informe um valor maior que zero e tente novamente...") if saque <= 0 else print(f"Limite máximo por saque é de {locale.currency(LIM_SAQUE_OPERACAO)}! Informe um valor menor que o {locale.currency(LIM_SAQUE_OPERACAO)}...")
                time.sleep(0.5)
        else:
            print(f"Limite de saques diários atingido. (MAX: {LIM_SAQUE_DIARIO} por dia)")
            break

def mostrar_extrato(operacao=0):
    print(usuario_logado['contas'][operacao]['extrato']) if usuario_logado['contas'][operacao]['extrato'] else print("Não foram realizadas movimentações.")
    print(f"Saldo: {locale.currency(usuario_logado['contas'][operacao]['saldo'])}\n")

def criar_conta_corrente(usuario):
    global contador_contas
    usuario['contas'].insert(0, {
        'agencia': "0001",
        'numero': contador_contas,
        'num_saques': 0,
        'saldo': 0,
        'extrato': ""
    })
    print(f"\nConta criada com sucesso!\nAgência: {usuario['contas'][0]['agencia']}\nNúmero: {usuario['contas'][0]['numero']}")
    contador_contas += 1
    return usuario

def cadastrar_usuario():
    while True:
        try:
            usuario = {
                'nome': input("Digite um nome: "),
                'data_nasc': input("Digite o nascimento (XX/XX/XXXX): "),
                'cpf': int(input("Digite um cpf (apenas números): ")) ,
                'endereco': input("Digite um endereço (<Logradouro>, <N°> - <Bairro> - <Cidade>/<UF>): "),
                'contas': []
            }
            assert usuario['cpf'] != ''

            if not usuarios:
                return usuario
            else:
                for u in usuarios:
                    if u['cpf'] == usuario['cpf']:
                        print("CPF já cadastrado, tente novamente...\n")
                        break
                    else:
                        return usuario
        except AssertionError:
            print("Campo CPF é obrigatório, porfavor preencha-o e tente novamente...\n")
        except ValueError:
            print("Valor informado inválido! Digite apenas números para o CPF...\n")

def login(nome, cpf):
    global usuario_logado
    for usuario in usuarios:
        if usuario['nome'] == nome and usuario['cpf'] == cpf:
            usuario_logado = usuario
            return usuario

def listar_contas(usuarios):
    for usuario in usuarios:
        print("-="*29)
        print(f"{usuario['nome']} - {usuario['cpf']} - {usuario['data_nasc']}")
        for conta in usuario['contas']:
            print(f"Conta:\tAg: {conta['agencia']} - Ctt: {conta['numero']}")
        print("-="*29, end="\n\n")

def movimentacoes(operacao=0):
    while True:
        num_saques = usuario_logado['contas'][operacao]['num_saques']
        menu_movimentacoes = f"=-=-=-=-= MENU =-=-=-=-=\n|  [D] Depósito         |\n|  [S] Saque [{num_saques}/3]      |\n|  [E] Extrato          |\n|  [Q] Sair             |\n-------------------------\nDigite uma opção: "
        os.system('cls' if os.name == 'nt' else 'clear')
        opc = input(menu_movimentacoes)

        if opc in 'dD':
            depositar()
            input("Pressione ENTER para continuar... ")
        elif opc in 'sS':
            sacar()
            input("Pressione ENTER para continuar... ")
        elif opc in 'eE':
            mostrar_extrato()
            input("Pressione ENTER para continuar... ")
        elif opc in 'qQ':
            print("Volte sempre !!!")
            break
        else:
            print("Opção inválida, tente novamente...")
            time.sleep(1)

while True:
    menu_inicial = f"\033[0;33m=-=-=-=-= \033[mBEM-VINDO \033[0;33m=-=-=-=-=\n|  [\033[mC\033[0;33m] Cadastrar Usuário    |\n|  [\033[mE\033[0;33m] Entrar em uma conta  |\n|  [\033[mL\033[0;33m] Listar Contas        |\n|  [\033[mQ\033[0;33m] Sair                 |\n-----------------------------\n\033[mDigite uma opção: "

    os.system('cls' if os.name == 'nt' else 'clear')
    opc = input(menu_inicial)
    print()

    if opc and opc in 'cC':
        usuario = cadastrar_usuario()
        usuarios.append(criar_conta_corrente(usuario))
        input("Pressione ENTER para continuar... ")

    elif opc and opc in 'eE':
        usuario = login(input("Nome: "), input("CPF: "))
        if usuario != None:
            movimentacoes()
        else:
            print("\nNome de usuário ou CPF inválido!")
        input("Pressione ENTER para continuar... ")

    elif opc and opc in 'lL':
        listar_contas(usuarios)
        input("Pressione ENTER para continuar... ")

    elif opc and opc in 'qQ':
        print("Volte sempre !!!")
        break

    else:
        print("Opção inválida, tente novamente...")
        time.sleep(1)
