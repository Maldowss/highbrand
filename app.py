#Importante respetar la sangría a la hora de escribir código(nota personal)
import os
from flask import Flask
#El siguiente import nos ayudará a importar la plantilla .html
#Request es el encargado de la recepción de la información y redirect nos va a servir para redireccionar y poder mostrar la iformación
#send_from_directory nos permitira el despliegue de las imagene que esten almacenadas en nuestro directio img
from flask import render_template, request, redirect, send_from_directory
#Nos permite la conexion con el controller del archivo clothes_controller.py
import clothes_controller
#para respetar el archivo imagen y sus propiedades
from datetime import datetime



app=Flask(__name__)


#Esto nos permite el acceso a las diferentes rutas .html
@app.route('/')
def home():
    return render_template('web/index.html')

@app.route('/img/<image>')
def images(image):
    print(image)
    return send_from_directory(os.path.join('templates/web/img'), image)

@app.route('/clothes')
def clothes():
    return render_template('web/clothes.html') 

@app.route('/info')
def info():
    return render_template('web/info.html')

@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/clothes')
def admin_clothes():
    clothes = clothes_controller.query_clothes()
    return render_template('admin/clothes.html', clothes=clothes)

@app.route('/admin/clothes/guardar', methods=['POST'])
def admin_clothe_save():
    _name=request.form['txtName']
    _brand=request.form['txtBrand']
    _price=request.form['txtPrice']
    _image=request.files['txtImage']
    _url=request.form['txtURL']

    time= datetime.now()
    actualHour=time.strftime('%Y%H%S')

    if _image.filename!="":
        newName=actualHour+"_"+_image.filename
        _image.save("templates/web/img/"+newName)
    clothes_controller.insert_clothe(_name, _brand, _price, newName, _url)
    return redirect('/admin/clothes')

@app.route('/admin/clothes/borrar', methods=['POST'])
def admin_clothe_delete():
    _id=request.form['txtID']
    clothes_controller.delete_clothe(_id)
    return redirect('/admin/clothes')

#Con esto sabremos si la aplicación está lista, de ser asi activa el modo debug
#de esta manera, si actualizamos index, también actualice
if __name__ == '__main__':
    app.run(debug = True)