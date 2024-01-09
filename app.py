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
    if not session.get('login'):
        return render_template("web/index.html", sesion="Log in")
    else:
        return render_template('web/index.html', sesion="Mi perfil")

@app.route('/img/<image>')
def images(image):
    return send_from_directory(os.path.join('templates/web/img'), image)

@app.route('/clothes')
def clothes():
    if not session.get('login'):
        sesion="Log in"
    else:
        return redirect('/clothes/userview')
        

    clothes = clothes_controller.query_clothes()
    
    users = []
    favorites = []
    for clothe in clothes:
        users.append(clothes_controller.query_user(clothe[6])) 
        favorites.append(None)
    # print(users)
    combined_data = list(zip(clothes, users, favorites))
    message = "Sin resultados" if len(clothes) == 0 else str(len(clothes))+' resultados encontrados:'

    return render_template('web/clothes.html', combined_data=combined_data, sesion=sesion, message=message, id=None)

@app.route('/clothes/userview')
def user_view_clothes():
    sesion="Mi perfil"

    clothes = clothes_controller.query_clothes()
    
    users = []
    favorites = []
    for clothe in clothes:
        users.append(clothes_controller.query_user(clothe[6])) 
        favorites.append(clothes_controller.check_favorites(session['id_user'], clothe[0]))

    print(favorites)
    combined_data = list(zip(clothes, users, favorites))
    message = "Sin resultados" if len(clothes) == 0 else str(len(clothes))+' resultados encontrados:'
    return render_template('web/clothes.html', combined_data=combined_data, sesion=sesion, message=message, id=session['id_user'])

@app.route('/clothes/buscar', methods=['POST'])
def search_clothes():
    search = request.form['txtSearch']
    users = []
    favorites = []
    clothes = clothes_controller.search_clothes(search)
    if not session.get('login'):
        sesion="Log in"
        id=None
        for clothe in clothes:
            users.append(clothes_controller.query_user(clothe[6])) 
            favorites.append(None)
    else:
        sesion="Mi perfil"
        id=session['id_user']
        for clothe in clothes:
            users.append(clothes_controller.query_user(clothe[6])) 
            favorites.append(clothes_controller.check_favorites(session['id_user'], clothe[0]))

    combined_data = list(zip(clothes, users, favorites))
    message = "Sin resultados" if len(clothes) == 0 else str(len(clothes))+' resultados encontrados:'
    return render_template('web/clothes.html', combined_data=combined_data, message=message, sesion=sesion, id=id)

@app.route('/logforfav')
def log_for_fav():
    return render_template("admin/login.html", message="inicia sesion para favoritos")

@app.route('/addFavorite', methods=['POST'])
def admin_add_favorite():

    _user_id=request.form['id_user']
    _clothe_id=request.form['id_clothe']
    _name=request.form['name']
    _brand=request.form['brand']
    _price=request.form['price']
    _image=request.form['image']
    _url=request.form['url']
    
    print(_user_id)
    clothes_controller.add_favorite(_user_id, _clothe_id, _name, _brand, _price, _image, _url)
    return "Success"

@app.route('/deleteFavorite', methods=['POST'])
def  admin_delete_favorite():
    _user_id=request.form['id_user']
    _clothe_id=request.form['id_clothe']

    clothes_controller.delete_favorite(_user_id, _clothe_id)

    return "success"

@app.route('/admin/info/deleteFavoriteUser', methods=['POST'])
def delete_favorite_userInfo():
    _user_id=request.form['id_user']
    _clothe_id=request.form['id_clothe']
    print(session['id_user'])
    clothes_controller.delete_favorite(_user_id, _clothe_id)

    return "success"

@app.route('/info')
def info():

    if not session.get('login'):
        sesion="Log in"
    else:
        sesion="Mi perfil"
    comments=clothes_controller.query_comments()

    if len(comments) > 4:
        last_four_comments = comments[-4:]
    else:
        last_four_comments=comments


    return render_template('web/info.html', comments=last_four_comments, sesion=sesion)

@app.route('/info/comentar', methods=['POST'])
def comment():
    if not session.get('login'):
        return render_template("admin/login.html", message="Debes iniciar sesión para comentar")
    
    text=request.form['txtComment']
    
    clothes_controller.insert_comment(session['user'], text, session['id_user'])
    
    return redirect('/info')


@app.route('/admin/')
def admin_index():
    if not session.get('login'):
        return redirect("/admin/login")
    
    return render_template('admin/index.html')

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

    if newName == _oldImage:
        condition = False
    else:
        condition = True

    clothes_controller.update_clothe(_id, _name, _brand, _price, newName, _url, condition)

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

@app.route('/admin/info')
def admmin_info():
    if not session.get('login'):
        return redirect("/admin/login")
    
    clothes = clothes_controller.query_clothes_favorites(session['id_user'])
    
    users = []
    for clothe in clothes:
        users.append(clothes_controller.query_user(clothe[1])) 

    # print(users)
    combined_data = list(zip(clothes, users))
    
    user_info=clothes_controller.query_info_user(session['id_user'])
   
    return render_template('/admin/userInfo.html', info=user_info, combined_data=combined_data)

@app.route('/admin/info/user_info', methods=['POST'])
def update_user_info():
    if not session.get('login'):
        return redirect("/admin/login")
    
    _oldName=request.form['nameOld']
    _oldLast_name=request.form['last_nameOld']
    _oldEmail=request.form['emailOld']
    _oldTlf=request.form['tlfOld']
    
    _name=request.form['name'] if request.form['name'] else _oldName
    _last_name=request.form['last_name'] if request.form['last_name'] else _oldLast_name
    _email=request.form['email'] if request.form['email'] else _oldEmail
    _tlf=request.form['tlf'] if request.form['tlf'] else _oldTlf

    clothes_controller.update_user_info(_name, _last_name, _email, _tlf, session['id_user'])
    
    return redirect('/admin/info')

#Con esto sabremos si la aplicación está lista, de ser asi activa el modo debug
#de esta manera, si actualizamos index, también actualice
if __name__ == '__main__':
    app.run(debug = True)