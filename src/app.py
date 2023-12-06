from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app=Flask(__name__)
CORS(app)

con=MySQL(app)

#Metodo para registrar usuarios
@app.route('/user_registration',methods=['POST'])
def registrar_usuario():
    try:
        datos = request.get_json()
        user=leer_usuarios_db(datos.get('email'), datos.get('password'))
        print("parametro1:", datos.get('email'))
        print("parametro2:", datos.get('password'))
        
        if user != None:
            return jsonify({'mensaje':'El correo ya esta registrado', 'exito':False})
        else: 
            cursor=con.connection.cursor()
            sql="""INSERT INTO usuarios(email,password)
            VALUES('{0}','{1}')""".format(datos.get('email'),datos.get('password'))
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Usuario registrado', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})

#Metodo para detectar usuarios
def leer_usuarios_db(email_user, password):
    try:
        cursor = con.connection.cursor()
        sql = 'select * from usuarios where email = "{0}" and password = "{1}"'.format(email_user, password)
        cursor.execute(sql)
        datos = cursor.fetchone()

        if datos != None:
            usuario = {'id_user':datos[0],'nickname':datos[1],'email':datos[2],'password':datos[3],'number_phone':datos[4]}
            return usuario
        else: 
            return None
    

    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':True})

#Metodo para obtener el usuario para su validacion
@app.route('/user',methods=['GET'])
def leer_alumno():
    try:
        email_user = request.args.get('email')
        password = request.args.get('password')
        user=leer_usuarios_db(email_user, password)

        if user != None:
            return jsonify({'mensaje':'Usuario encontrado', 'exito':True})
        else:
            return jsonify({'mensaje':'Usuario no encontrado', 'exito':False})  
              
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})
    
#Metodo para obtener las figuras
@app.route('/figuras',methods=['GET'])
def obtener_figuras():
    try:
        cursor = con.connection.cursor()
        sql = 'select * from figuritas'
        cursor.execute(sql)
        datos=cursor.fetchall()
        figuras=[]
        for fila in datos:
            figura={'id':fila[0],'titulo':fila[1],'cantidad':fila[2],'estilo':fila[3],'descripcion':fila[4],'marca':fila[5], 'photo':fila[6]}
            figuras.append(figura)
            print(figura)
        return jsonify({'figuras':figuras, 'mensaje':'lista de Figuras', 'exito':True})
              
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})

#Metodo para registrar una figura
@app.route('/figure_registration',methods=['POST'])
def registrar_figura():
    try:
        datosFigura = request.get_json()
        cursor=con.connection.cursor()
        sql="""INSERT INTO figuritas(title,cantidad,style,description,brand,photo)
        VALUES('{0}','{1}','{2}','{3}','{4}','{5}')""".format(datosFigura.get('titulo'),datosFigura.get('cantidad'),datosFigura.get('estilo'),datosFigura.get('descripcion'),datosFigura.get('marca'),datosFigura.get('photo'))
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'Figura registrada', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})
    
#Metodo para borrar una Figura
@app.route('/figure_delete',methods=['POST'])
def eliminar_figura():
    try:
        datosFigura = request.get_json()
        cursor=con.connection.cursor()
        sql="""DELETE FROM figuritas WHERE id = {0}""".format(datosFigura.get('id'))
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'Figura eliminada', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})
    
#Metodo para modificar una Figura
@app.route('/figure_edit',methods=['POST'])
def modificar_figura():
    try:
        datosFigura = request.get_json()
        cursor=con.connection.cursor()
        sql="""UPDATE figuritas SET title='{0}', cantidad='{1}', style='{2}', description='{3}', brand='{4}', photo='{5}' WHERE id = {6}
        """.format(datosFigura.get('titulo'),datosFigura.get('cantidad'),datosFigura.get('estilo'),datosFigura.get('descripcion'),datosFigura.get('marca'),datosFigura.get('photo'),datosFigura.get('id'),)
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'Figura eliminada', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"

carrito = []

# Método para agregar figura al carrito
@app.route('/agregar_figura_al_carrito', methods=['POST'])
def agregar_figura_al_carrito():
    try:
        datosFigura = request.get_json()

        # Verifica si la figura ya está en el carrito
        figura_existente = next((item for item in carrito if item['id'] == datosFigura['id']), None)

        if figura_existente:
            # Si la figura ya está en el carrito, incrementa la cantidad
            figura_existente['cantidad'] += 1
        else:
            # Si la figura no está en el carrito, agrégala con cantidad 1
            carrito.append({'id': datosFigura['id'], 'titulo': datosFigura['titulo'], 'cantidad': 1})

        return jsonify({'mensaje': 'Figura agregada al carrito', 'exito': True, 'carrito': carrito})

    except Exception as ex:
        return jsonify({'mensaje': 'Error al agregar la figura al carrito {}'.format(ex), 'exito': False})

# Método para obtener el carrito
@app.route('/obtener_carrito', methods=['GET'])
def obtener_carrito():
    try:
        return jsonify({'carrito': carrito, 'mensaje': 'Carrito obtenido', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al obtener el carrito {}'.format(ex), 'exito': False})


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()

