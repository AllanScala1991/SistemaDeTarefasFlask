from flask import render_template, Flask, request
import sqlite3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#VARIAVEIS GLOBAIS
exibir_all = True

    



#INICIA O INDEX DO SISTEMA
@app.route('/')
def index_page():
    all_registers = []
    with sqlite3.connect('static/database/database.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM tarefas")
        ids = cursor.fetchall()
        for tarefa in ids:
            cursor.execute("SELECT * FROM tarefas WHERE id=?",(tarefa))
            all_registers.append(cursor.fetchone())
        cursor.execute("SELECT id FROM tarefas WHERE condicao=?",('ABERTO',))
        abertos = cursor.fetchall()
        total_aberto = 0
        for i in abertos:
            total_aberto +=1
        return render_template('index.html', registers = all_registers, exibir = exibir_all,itens_aberto = total_aberto)

#SALVA O CADASTRO
@app.route('/salvar_cadastro', methods=['POST'])
def Save_Register():
    #PEGANDO AS INFORMACOES DO FORM
    nome = request.form['nome']
    status = "ABERTO"
    dt_inicio = request.form['inicio']
    dt_final = request.form['final']
    descricao = request.form['descricao']
    all_registers = []
    #ACESSANDO O BANCO DE DADOS
    with sqlite3.connect('static/database/database.db') as connection:
        
        #GRAVANDO AS INFORMÇÕES
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tarefas (nome, descricao, dt_inicio, dt_final, condicao) VALUES (?,?,?,?,?)",(nome,descricao,dt_inicio,dt_final,status,))
        connection.commit()
        #SELECIONANDO TODOS OS REGISTROS PARA MANDAR PARA PAGINA
        cursor.execute("SELECT id FROM tarefas")
        ids = cursor.fetchall()
        for tarefa in ids:
            cursor.execute("SELECT * FROM tarefas WHERE id=?",(tarefa))
            all_registers.append(cursor.fetchone())
            
        cursor.execute("SELECT id FROM tarefas WHERE condicao=?",('ABERTO',))
        abertos = cursor.fetchall()
        total_aberto = 0
        for i in abertos:
            total_aberto +=1
        return render_template('index.html', registers = all_registers, exibir = exibir_all,itens_aberto = total_aberto)
@app.route('/search', methods=['POST'])
def Search():
    search = request.form['search']
    try:
        with sqlite3.connect('static/database/database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM tarefas WHERE nome=?',(search,))
            search_select = cursor.fetchall()
            
            cursor.execute("SELECT id FROM tarefas WHERE condicao=?",('ABERTO',))
            abertos = cursor.fetchall()
            total_aberto = 0
            for i in abertos:
                total_aberto +=1
            
            if search_select != []:
                return render_template('index.html',registers = search_select, exibir = True,itens_aberto = total_aberto)
            else:
                return render_template('index.html',registers = search_select, error_search = True,itens_aberto = total_aberto)

    except:
        return render_template('index.html',registers = search_select, error_search = True,itens_aberto = total_aberto)

@app.route('/delete/<delete_item>')
def Delete(delete_item):
    with sqlite3.connect('static/database/database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tarefas WHERE id=?',(delete_item,))
        connection.commit()
        
        all_registers = []
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM tarefas")
        ids = cursor.fetchall()
        for tarefa in ids:
            cursor.execute("SELECT * FROM tarefas WHERE id=?",(tarefa))
            all_registers.append(cursor.fetchone())
        
        cursor.execute("SELECT id FROM tarefas WHERE condicao=?",('ABERTO',))
        abertos = cursor.fetchall()
        total_aberto = 0
        for i in abertos:
            total_aberto +=1
            
        return render_template('index.html', registers = all_registers, exibir = exibir_all,itens_aberto = total_aberto)

@app.route('/condicao/<finalizar_item>')
def Finalizar(finalizar_item):
    with sqlite3.connect('static/database/database.db') as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE tarefas SET condicao=? WHERE id=?",("CONCLUIDO",(finalizar_item)))
        connection.commit()
        
        all_registers = []
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM tarefas")
        ids = cursor.fetchall()
        for tarefa in ids:
            cursor.execute("SELECT * FROM tarefas WHERE id=?",(tarefa))
            all_registers.append(cursor.fetchone())
        
        cursor.execute("SELECT id FROM tarefas WHERE condicao=?",('ABERTO',))
        abertos = cursor.fetchall()
        total_aberto = 0
        for i in abertos:
            total_aberto +=1    
            
        return render_template('index.html', registers = all_registers, exibir = exibir_all,itens_aberto = total_aberto)

@app.route('/filtro/<filtrar>')
def Filtro_Aberto(filtrar):
    try:
        with sqlite3.connect('static/database/database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM tarefas WHERE condicao=?',(filtrar,))
            search_select = cursor.fetchall()
            
            cursor.execute("SELECT id FROM tarefas WHERE condicao=?",('ABERTO',))
            abertos = cursor.fetchall()
            total_aberto = 0
            for i in abertos:
                total_aberto +=1
            
            if search_select != []:
                return render_template('index.html',registers = search_select, exibir = True,itens_aberto = total_aberto)
            else:
                return render_template('index.html',registers = search_select, error_search = True,itens_aberto = total_aberto)

    except:
        return render_template('index.html',registers = search_select, error_search = True,itens_aberto = total_aberto)
        
    
    
    
    
        
        
            

#INICIA O FLASK
if __name__ == '__main__':
    app.run(port=5000)