from flask import Flask
from flask import render_template

app = Flask(__name__)

lances = dict({})

@app.route("/")
def home():
    return render_template('base.html')

@app.route("/lance/<string:valor>", methods =['POST'])
def fazer_lance(valor):
    
    try:
        valor = float(valor)
    except ValueError:
        return ('',404)
    
    if(valor not in lances):
        lances[valor] = 1
    else:
        lances[valor] += 1
        
    return ('',201)
    
@app.route("/menor-lance")
def obter_menor_lance_unico():
    global lances
    lance_minimo_unico = -1
    
    for key,value in lances.items():
        if(value == 1 and (lance_minimo_unico == -1 or key < lance_minimo_unico)):
            lance_minimo_unico = key
                
    if(lance_minimo_unico != -1):
        return f'<h1>O menor lance único foi: {lance_minimo_unico}</h1>'
    else:
        return '<h1>Não houve nenhum lance mínimo único ainda.</h1>'
