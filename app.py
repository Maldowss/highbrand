#Importante respetar la sangría a la hora de escribir código(nota personal)
import os
from flask import Flask
#El siguiente import nos ayudará a importar la plantilla .html
#Request es el encargado de la recepción de la información y redirect nos va a servir para redireccionar y poder mostrar la iformación
#send_from_directory nos permitira el despliegue de las imagene que esten almacenadas en nuestro directio img
#Session como su nombre indica nos permite almacenar los datos durante una sesión
from flask import render_template, request, redirect, send_from_directory, session
#Nos permite la conexion con el controller del archivo clothes_controller.py
import clothes_controller
#para respetar el archivo imagen y sus propiedades
from datetime import datetime



app=Flask(__name__)
app.secret_key="develoteca"

#Esto nos permite el acceso a las diferentes rutas .html
@app.route('/')
def home():
    return render_template('web/index.html')

@app.route('/img/<image>')
def images(image):
    return send_from_directory(os.path.join('templates/web/img'), image)

@app.route('/clothes')
def clothes():
    clothes = clothes_controller.query_clothes()
    # print(clothes)
    users = []
    for clothe in clothes:
        users.append(clothes_controller.query_user(clothe[6])) 

    # print(users)
    combined_data = list(zip(clothes, users))

    return render_template('web/clothes.html', combined_data=combined_data)

@app.route('/clothes/buscar', methods=['POST'])
def search_clothes():
    search = request.form['txtSearch']
    clothes = clothes_controller.search_clothes(search)
    users = []
    for clothe in clothes:
        users.append(clothes_controller.query_user(clothe[6])) 

    # print(users)
    combined_data = list(zip(clothes, users))
    message = "Sin resultados" if len(clothes) == 0 else str(len(clothes))+' resultados encontrados:'
    return render_template('web/clothes.html', combined_data=combined_data, message=message)

@app.route('/info')
def info():
    return render_template('web/info.html')

@app.route('/admin/')
def admin_index():
    if not session.get('login'):
        return redirect("/admin/login")
    
    return render_template('admin/index.html')

# @app.route('/admin/edit', methods=['POST'])
# def admin_edit():
#     if not session.get('login'):
#         return redirect("/admin/login")
    
#     info_clothe = []
#     info_clothe.append(request.form['txtID'])
#     info_clothe.append(request.form['txtName'])
#     info_clothe.append(request.form['txtBrand'])
#     info_clothe.append(request.form['txtPrice'])
#     info_clothe.append(request.form['txtImage'])
#     info_clothe.append(request.form['txtUrl'])
    
#     return render_template("admin/edit.html", info=info_clothe)

@app.route('/admin/edit', methods=['POST'])
def admin_edit():
    if not session.get('login'):
        return redirect("/admin/login")
    
    info_clothe = []
    info_clothe.append(request.form.get('txtID', ''))
    info_clothe.append(request.form.get('txtName'))
    info_clothe.append(request.form.get('txtBrand'))
    info_clothe.append(request.form.get('txtPrice'))
    info_clothe.append(request.form.get('txtImage'))
    info_clothe.append(request.form.get('txtUrl'))
    print(info_clothe)
    return render_template("admin/edit.html", info=info_clothe)


@app.route('/admin/edit/actualizar', methods=['POST'])
def admin_edit_update():
    if not session.get('login'):
        return redirect("/admin/login")
    
    _oldName=request.form['txtNameOld']
    _oldBrand=request.form['txtBrandOld']
    _oldPrice=request.form['txtPriceOld']
    _oldImage=request.form['txtImageOld']
    _oldUrl=request.form['txtUrlOld']
    
    _id=request.form['txtID']
    _name=request.form['txtName'] if request.form['txtName'] else _oldName
    _brand=request.form['txtBrand'] if request.form['txtBrand'] else _oldBrand
    _price=request.form['txtPrice'] if request.form['txtPrice'] else _oldPrice
    _url=request.form['txtURL'] if request.form['txtURL'] else _oldUrl

    if not request.files['txtImage']:
        newName=_oldImage
    else:
        time= datetime.now()
        actualHour=time.strftime('%Y%H%S')
        if request.files['txtImage'].filename!="":
            newName=actualHour+"_"+request.files['txtImage'].filename
            request.files['txtImage'].save("templates/web/img/"+newName)

    clothes_controller.update_clothe(_id, _name, _brand, _price, newName, _url)

    return redirect('/admin/clothes')

@app.route('/admin/login')
def admin_login():
    if not session.get('login'):
        return render_template("/admin/login.html")
    

    return redirect('/admin/clothes')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _user=request.form['txtUser']
    _password=request.form['txtPassword']

    if clothes_controller.login_authentication(_user, _password) == True:
        session['login'] = True
        session['user'] = _user
        _id_user= clothes_controller.query_id_user(_user)
        session['id_user'] = _id_user[0]
        return redirect('/admin/clothes')
    
    return render_template('admin/login.html', message="Denied acces")

@app.route('/admin/register')
def admin_register():

    return render_template('admin/register.html')

@app.route('/admin/register', methods=['POST'])
def admin_register_post():
    _newUser=request.form['txtUser']
    _newPass1=request.form['txtPasswordX']
    _newPass2=request.form['txtPasswordY']
    if clothes_controller.check_user_existence(_newUser) == True:
        message='User already in use'
    elif _newPass1 != _newPass2:
        message='Passwords must be the same'
    else:
        clothes_controller.register_user(_newUser, _newPass2)
        if not session.get('login'):
            session['login'] = True
            session['user'] = _newUser
            _id_user= clothes_controller.query_id_user(_newUser)
            session['id_user'] = _id_user[0]
            return redirect('/admin/clothes')
        else:
            return redirect('/clothes')

    return render_template('admin/register.html', message=message)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/admin/login')

@app.route('/admin/daccount')
def admin_daccount():
    if not session.get('login'):
        return redirect("/admin/login")
    
    return render_template('/admin/deleteAccount.html')
    
@app.route('/admin/daccount/eliminar')
def admin_daccount_delete():
    if not session.get('login'):
        return redirect("/admin/login")
    
    
    clothes_controller.delete_user(session['id_user'])
    session.clear()
    return redirect('/')
    

@app.route('/admin/clothes')
def admin_clothes():
    if not session.get('login'):
        return redirect("/admin/login")
    
    clothes = clothes_controller.query_clothes_admin(session['id_user'])
    return render_template('admin/clothes.html', clothes=clothes)

@app.route('/admin/clothes/control',)
def admin_clothes_post():
    if not session.get('login'):
        return redirect("/admin/login")
    
    clothes = clothes_controller.query_clothes_admin(session['id_user'])
    return render_template('admin/clothes.html', clothes=clothes, message='No dejes un campo sin rellenar')

@app.route('/admin/clothes/guardar', methods=['POST'])
def admin_clothe_save():
    if not session.get('login'):
        return redirect("/admin/login")

    _name=request.form['txtName']
    _brand=request.form['txtBrand']
    _price=request.form['txtPrice']
    _image=request.files['txtImage']
    _url=request.form['txtURL']

    if not all((request.form['txtName'], request.form['txtBrand'], request.form['txtPrice'], request.files['txtImage'], request.form['txtURL'])):
        return redirect('/admin/clothes/control')



    time= datetime.now()
    actualHour=time.strftime('%Y%H%S')

    if _image.filename!="":
        newName=actualHour+"_"+_image.filename
        _image.save("templates/web/img/"+newName)
    clothes_controller.insert_clothe(_name, _brand, _price, newName, _url, session['id_user'])
    return redirect('/admin/clothes')

@app.route('/admin/clothes/borrar', methods=['POST'])
def admin_clothe_delete():
    if not session.get('login'):
        return redirect("/admin/login")

    _id=request.form['txtID']
    clothes_controller.delete_clothe(_id)
    return redirect('/admin/clothes')

#Con esto sabremos si la aplicación está lista, de ser asi activa el modo debug
#de esta manera, si actualizamos index, también actualice
if __name__ == '__main__':
    app.run(debug = True)