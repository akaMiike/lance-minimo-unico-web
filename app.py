from flask import Flask
from flask import render_template, jsonify, request, flash, redirect, url_for
import random, datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'lances12345'

lances = dict({})

tempo_restante_rodada = 10
tempo_restante_retornar_inicio = 10

premios = {
    "/static/carrinho.png" : "Carrinho da hotwheels 0 KM",
    "/static/nota10.png" : "Notas 10 em todas as disciplinas pelo resto do curso"
}

premio_rodada = []

@app.route("/timer/resultado")
def timer_resultado():
    global tempo_restante_retornar_inicio, tempo_restante_rodada, premio_rodada, lances
    
    tempo_restante_result = str(datetime.timedelta(seconds = (tempo_restante_retornar_inicio)))
    
    if(tempo_restante_retornar_inicio == 0):
        tempo_restante_rodada = 10
        tempo_restante_retornar_inicio = 10
        premio_rodada = []
        lances = {}
    
    else:
        tempo_restante_retornar_inicio = tempo_restante_retornar_inicio - 1

    return jsonify({"result": tempo_restante_result})

@app.route("/timer/rodada")
def timer_rodada():
    global tempo_restante_rodada, premio_rodada
    
    tempo_restante_result = str(datetime.timedelta(seconds = (tempo_restante_rodada)))
    tempo_restante_rodada = tempo_restante_rodada - 1

    return jsonify({"result": tempo_restante_result})

@app.route("/")
def home():
    return render_template('regras.html')

@app.route("/lances")
def tela_lances():
    global premio_rodada
    
    if(len(premio_rodada) == 0):
        premio_atual, descricao = random.choice(list(premios.items()))
        
        premio_rodada.append(premio_atual)
        premio_rodada.append(descricao)
    else:
        premio_atual = premio_rodada[0]
        descricao = premio_rodada[1]
    
    return render_template('tela-lances.html', premio=premio_atual, descricao=descricao)

@app.route("/lances", methods =['POST'])
def fazer_lance():
    global premio_rodada
    
    nome = request.form['Nome']
    valor_lance = request.form['Lance']
    
    try:
        valor_lance = float(valor_lance)
    except ValueError:
        return ('',404)
    
    if(valor_lance not in lances):
        lances[valor_lance] = [nome]
    else:
        lances[valor_lance].append(nome)
    
    flash("Lance submetido com sucesso!")
    return redirect(url_for('tela_lances'))
    
@app.route("/lances/resultado")
def obter_resultado():
    global lances, premio_rodada, tempo_restante_rodada
    
    if(tempo_restante_rodada > 0):
        return redirect(url_for('tela_lances'))
    
    lance_minimo_unico = -1
    nome_ganhador = ""
    
    for key,value in lances.items():
        if(len(value) == 1 and (lance_minimo_unico == -1 or key < lance_minimo_unico)):
            lance_minimo_unico = key
            nome_ganhador = value[0]
                
    return render_template('tela-resultado.html', nome = nome_ganhador, lance = lance_minimo_unico, premio=premio_rodada[0])


@app.route("/lances/maior-lance")
def obter_maior_lance_unico():
    global lances
    lance_maximo_unico = -1
    
    for key,value in lances.items():
        if(len(value) == 1 and (lance_maximo_unico == -1 or key > lance_maximo_unico)):
            lance_maximo_unico = key

    return jsonify({"result": lance_maximo_unico})