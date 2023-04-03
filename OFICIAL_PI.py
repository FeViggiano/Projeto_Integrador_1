#!/usr/bin/env python
# coding: utf-8

# In[3]:


import PySimpleGUI as sg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys

def limpar():
    window['-ID-'].update('')
    window['-Cliente-'].update('')
    window['-PET-'].update('')
    window['-CEL-'].update('')


def atualiza():
    if len(lista) == 0:
        limpar()
    else:
        window['-ID-'].update( lista[indice][0] )
        window['-Cliente-'].update( lista[indice][1] )
        window['-PET-'].update( lista[indice][2] )
        window['-CEL-'].update( lista[indice][3] )


def todos():
    global indice
    global lista
    query = QSqlQuery()
    query.prepare("SELECT ID, Cliente, PET, celular FROM cadastro")
    query.exec() # execute a query

    # Índices com Clientes para melhorar a legibilidade
    ID, Cliente, PET, celular = range(4)  # 0, 1, 2 e 3
    cont = 0
    lista.clear()
    while query.next():
        lista.append( [query.value(ID), query.value(Cliente), query.value(PET), query.value(celular)] )
        cont += 1
    query.finish()
    sg.popup('Quantidade de registros: ' + str(cont))
    indice = 0
    atualiza()


# Inicialização BD
arquivo = 'cadastro.sqlite'
con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName(arquivo)
if not con.open():
  print("Erro na base de dados: %s" % con.lastError().databaseText())
  sys.exit()
else:
  createTableQuery = QSqlQuery()
  createTableQuery.exec('CREATE TABLE IF NOT EXISTS cadastro (            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,            Cliente VARCHAR(40) NOT NULL,            PET VARCHAR(40) NOT NULL,            celular VARCHAR(20) NOT NULL)')
  createTableQuery.finish()

lista=[]
indice = 0

layout = [
    [
        sg.Text("ID:", size=(8, 1)),
        sg.InputText(size=(40, 1), key="-ID-", focus=True)
    ],
    [
        sg.Text("Cliente:", size=(8, 1)),
        sg.InputText(size=(40, 1), key="-Cliente-")
    ],
    [
        sg.Text("PET:", size=(8, 1)),
        sg.InputText(size=(40, 1), key="-PET-")
    ],
    [
        sg.Text("Celular:", size=(8, 1)),
        sg.InputText(size=(40, 1), key="-CEL-")
    ],
    [
        sg.Button('Limpar', size=(9, 1), key="-LIMPAR-"),
        sg.Button('Inserir', size=(9, 1), key="-INSERIR-"),
        sg.Button('Atualizar', size=(9, 1), key="-ATUALIZAR-"),
        sg.Button('Remover', size=(9, 1), key="-REMOVER-")
    ],
    [
        sg.Button('<<', size=(9, 1), key="-<<-"),
        sg.Button('Procurar', size=(9, 1), key="-PROCURAR-"),
        sg.Button('Todos', size=(9, 1), key="-TODOS-"),
        sg.Button('>>', size=(9, 1), key="->>-")
    ]
]

window = sg.Window("Cadastro CLIENTE - Villa dos Pets", layout, use_default_focus=False)

# Run the Event Loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == "-LIMPAR-":
        limpar()
    elif event == "-INSERIR-":
        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare('INSERT INTO cadastro (Cliente, PET, celular) VALUES (?, ?, ?)')
        insertDataQuery.addBindValue(values['-Cliente-']) # dado relativo ao primeiro espaço reservado
        insertDataQuery.addBindValue(values['-PET-']) # dado relativo ao segundo espaço reservado
        insertDataQuery.addBindValue(values['-CEL-']) # dado relativo ao terceiro espaço reservado
        insertDataQuery.exec() # execute a query
        insertDataQuery.finish() # inative a query
        limpar()
    elif event == "-ATUALIZAR-":
        queryUpdate = QSqlQuery()
        queryUpdate.prepare("UPDATE cadastro SET Cliente = ?, PET = ?, celular = ? WHERE ID = ?")
        queryUpdate.addBindValue(values['-Cliente-'])
        queryUpdate.addBindValue(values['-PET-'])
        queryUpdate.addBindValue(values['-CEL-'])
        queryUpdate.addBindValue(values['-ID-'])
        queryUpdate.exec() # execute a query
        queryUpdate.finish()
        lista[indice] = [values['-ID-'], values['-Cliente-'], values['-PET-'], values['-CEL-']]        
    elif event == "-REMOVER-":
        queryDelete = QSqlQuery()
        queryDelete.prepare("DELETE FROM cadastro WHERE ID = ?")
        queryDelete.addBindValue( values['-ID-'] )
        queryDelete.exec() # execute a query
        queryDelete.finish()
        lista.pop(indice)
        indice -= 1
        atualiza()
    elif event == "-PROCURAR-":
        query = QSqlQuery()
        query.prepare("SELECT ID, Cliente, PET, celular FROM cadastro WHERE Cliente LIKE ? ORDER BY ID")
        query.addBindValue('%'+values['-Cliente-']+'%') # dado relativo ao espaço reservado
        query.exec() # execute a query

        # Índices com Clientes para melhorar a legibilidade
        ID, Cliente, PET, celular = range(4)  # 0, 1, 2 e 3
        cont = 0
        lista.clear()
        while query.next():
            lista.append( [query.value(ID), query.value(Cliente), query.value(PET), query.value(celular)] )
            cont += 1
        query.finish()  
        sg.popup('Quantidade de registros: ' + str(cont))
        indice = 0
        atualiza()
    elif event == "-TODOS-":
        todos()
    elif event == "->>-":
        indice += 1
        if indice >= len(lista): indice = len(lista)-1
        atualiza()
    elif event == "-<<-":
        indice -= 1
        if indice <= 0: indice = 0
        atualiza()

window.close()
con.close()
QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())


# In[ ]:





# In[ ]:




