import os, time, locale

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')  
LIM_SAQUE_DIARIO = 3
LIM_SAQUE_OPERACAO = 500

saldo = 0
num_saques = 0
extrato = ""

def depositar():
    global saldo, extrato
    while True:
        try:
            deposito = float(input("Valor: ").strip())
            assert deposito > 0
            saldo += deposito
            extrato += f"+ {locale.currency(deposito)}\n"
            break
        except ValueError:
            print("Valor informado é inválido! Informe um valor numérico e tente novamente...")
            time.sleep(1)
        except AssertionError:
            print("Valor informado é inválido! Informe um valor maior que zero e tente novamente...")
            time.sleep(1)

def sacar():
    global saldo, num_saques, extrato
    while True:
        if num_saques != LIM_SAQUE_DIARIO:
            try:
                saque = float(input("Valor: ").strip())
                assert saque > 0
                assert saque <= 500
                if saldo >= saque:
                    num_saques += 1
                    saldo -= saque
                    extrato += f"- {locale.currency(saque)}\n"
                    break
                else:
                    print("Saldo insuficiente para realizar o saque!")
            except ValueError:
                print("Valor informado é inválido! Informe um valor numérico e tente novamente...")
                time.sleep(1)
            except AssertionError:
                print("Valor informado é inválido! Informe um valor maior que zero e tente novamente...") if saque <= 0 else print(f"Limite máximo por saque é de {locale.currency(LIM_SAQUE_OPERACAO)}! Informe um valor menor que o {locale.currency(LIM_SAQUE_OPERACAO)}...")
                time.sleep(1)
        else:
            print(f"Limite de saques diários atingido. (MAX: {LIM_SAQUE_DIARIO} por dia)")
            break

def mostrar_extrato(extrato):
    print(extrato) if extrato else print("Não foram realizadas movimentações.")
    print(f"Saldo: {locale.currency(saldo)}")


while True:
    menu = f"""
=-=-=-= MENU =-=-=-=
|  [d] Depósito    |
|  [s] Saque [{num_saques}/3] |
|  [e] Extrato     |
|  [q] Sair        |
--------------------
Digite uma opção: """
    
    os.system('cls' if os.name == 'nt' else 'clear')
    opc = input(menu)

    if opc == 'd':
        depositar()
        input("Pressione ENTER para continuar... ")

    elif opc == 's':
        sacar()
        input("Pressione ENTER para continuar... ")

    elif opc == 'e':
        mostrar_extrato(extrato)
        input("Pressione ENTER para continuar... ")

    elif opc == 'q':
        print("Volte sempre !!!")
        break

    else:
        print("Opção inválida, tente novamente...")
        time.sleep(1)
