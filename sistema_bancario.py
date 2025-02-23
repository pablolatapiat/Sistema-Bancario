import os, time, locale

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')  
LIM_SAQUE_DIARIO = 3
LIM_SAQUE_OPERACAO = 500

saldo = 0
num_saques = 0
extrato = ""

def depositar(saldo, extrato, /):
    while True:
        try:
            deposito = input("\n[c] Cancelar operação\nValor: ").strip()
            if deposito == 'c':
                print("Operação Cancelada!\n")
                break
            deposito = float(deposito)
            assert deposito > 0
            saldo += deposito
            extrato += f"+ {locale.currency(deposito)}\n"
            break
        except ValueError:
            print("Valor informado é inválido! Informe um valor numérico e tente novamente...")
            time.sleep(0.5)
        except AssertionError:
            print("Valor informado é inválido! Informe um valor maior que zero e tente novamente...")
            time.sleep(0.5)
    return saldo, extrato

def sacar(*, saldo, num_saques, extrato):
    while True:
        if num_saques != LIM_SAQUE_DIARIO:
            try:
                saque = input("\n[c] Cancelar operação\nValor: ").strip()
                if saque == 'c':
                    print("Operação Cancelada!\n")
                    break
                saque = float(saque)
                assert saque > 0
                assert saque <= 500
                if saldo >= saque:
                    num_saques += 1
                    saldo -= saque
                    extrato += f"- {locale.currency(saque)}\n"
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
    return saldo, num_saques, extrato

def mostrar_extrato(saldo, /, extrato):
    print(extrato) if extrato else print("Não foram realizadas movimentações.")
    print(f"Saldo: {locale.currency(saldo)}\n")


while True:
    menu_operacoes = f"""
=-=-=-= MENU =-=-=-=
|  [D] Depósito    |
|  [S] Saque [{num_saques}/3] |
|  [E] Extrato     |
|  [Q] Sair        |
--------------------
Digite uma opção: """

    menu_contas = f"""
=-=-=-=-= BEM-VINDO =-=-=-=-=
|  [C] Cadastrar Usuário
|  [E] Entrar em uma conta
|  [L] Listar 
|  [Q] Sair
"""
    
    os.system('cls' if os.name == 'nt' else 'clear')
    opc = input(menu_operacoes)

    if opc in 'dD':
        saldo, extrato = depositar(saldo, extrato)
        input("Pressione ENTER para continuar... ")

    elif opc == 'sS':
        saldo, num_saques, extrato = sacar(saldo=saldo, num_saques=num_saques, extrato=extrato)
        input("Pressione ENTER para continuar... ")

    elif opc == 'eE':
        mostrar_extrato(saldo, extrato=extrato)
        input("Pressione ENTER para continuar... ")

    elif opc == 'qQ':
        print("Volte sempre !!!")
        break

    else:
        print("Opção inválida, tente novamente...")
        time.sleep(1)
