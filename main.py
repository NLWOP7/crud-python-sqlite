import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS cadastro_clientes
               (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               titular TEXT NOT NULL,
               saldo FLOAT NOT NULL,
               cpf TEXT NOT NULL UNIQUE)""")

def adicionar_cliente(titular, saldo, cpf):
    cursor.execute("""INSERT INTO cadastro_clientes
                   (titular, saldo, cpf) VALUES
                   (?, ?, ?)""",(titular, saldo, cpf))
    conexao.commit()

def lista_clientes():
    cursor.execute("""SELECT * FROM cadastro_clientes""")
    clientes = cursor.fetchall()
    for cliente in clientes:
        id, titular, saldo, cpf = cliente
        print(f"""id: {id}
Titular: {titular}
Saldo: {saldo}
CPF: {cpf}""")
        print("\n")

def atualizar_saldo(valor, id):
    cursor.execute("""UPDATE cadastro_clientes
                   SET saldo = saldo + ?
                   WHERE id = ?""",(valor, id))
    conexao.commit()

def deletar_cliente(id):
    cursor.execute("DELETE FROM cadastro_clientes WHERE id = ?", (id,))
    conexao.commit()

def lista_ids_clientes():
    cursor.execute("SELECT id FROM cadastro_clientes")
    resultados = cursor.fetchall()
    return [ c[0] for c in resultados ]

def mostrar_saldo(id):
    cursor.execute("SELECT saldo FROM cadastro_clientes WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None
    
while True:
    print("""1 - Adicionar cliente
2 - Atualizar saldo
3 - Deletar cliente
4 - Lista de clientes
5 - Sair""")
    escolha = input("Escolha uma opçao: ")
    
    if escolha == "1":
        titular = input("Nome do cliente: ").capitalize().strip()
        saldo = float(input("Saldo da conta do cliente: "))
        cpf = input("Qual cpf do cliente: ").strip()
        try:
            adicionar_cliente(titular, saldo, cpf)
            print('Cliente adicionado com sucesso')
        except sqlite3.IntegrityError:
            print("Erro: CPF ja cadastrado!")

    elif escolha == "2":
        saldo_atualizado = float(input('Valor que deseja adicionar: '))
        id_saldo_atualizado = int(input('Id da pessoas que deseja atualizar o saldo: '))
        if id_saldo_atualizado in lista_ids_clientes():
            atualizar_saldo(saldo_atualizado, id_saldo_atualizado)
            saldo_novo = mostrar_saldo(id_saldo_atualizado)
            print(f'Saldo atualizado com sucesso {saldo_novo}')
        else:
            print('Cliente nao encontrado')

    elif escolha == "3":
        delete_cliente = int(input("ID do cliente que deseja deletar: "))
        if delete_cliente in lista_ids_clientes():
            deletar_cliente(delete_cliente)
            print('Cliente deletado com sucesso')
        else:
            print('Cliente nao encontrado')

    elif escolha == "4":
        print("\n")
        lista_clientes()

    elif escolha == "5":
        print('Programa finalizado')
        break
    else:
        print('Opcao invalida! ')
