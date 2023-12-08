from bd import conexion
import os

def query_clothes():
    conexion_db= conexion()
    clothes = []
    with conexion_db.cursor() as cursor:
        cursor.execute('SELECT * FROM clothes')
        clothes = cursor.fetchall()
    conexion_db.close()
    return clothes

def insert_clothe(name, brand, price, image, url):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("INSERT INTO clothes(nombre, marca, precio, imagen, url) VALUES (%s, %s, %s, %s, %s)",
                       (name, brand, price, image, url))
    conexion_db.commit()
    conexion_db.close()

def delete_clothe(id):
    delete_image_directory(id)
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("DELETE FROM clothes WHERE id = %s", (id,))
    conexion_db.commit()
    conexion_db.close()

def delete_image_directory(id):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT imagen from clothes WHERE id = %s", (id))
        clothe=cursor.fetchall()

        if os.path.exists("templates/web/img/"+str(clothe[0][0])):
            os.unlink("templates/web/img/" + str(clothe[0][0]))

    conexion_db.commit()
    conexion_db.close()

def login_authentication(user, password):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT user, password FROM users WHERE user=%s AND password=%s", (user,password))
        user_data = cursor.fetchone()
        #print('Datos del formulario'+ user, password)
        #print('Datos de bd' + str(user_data))
        valor = str(user_data)
        if  valor == 'None':
            access = False
        else:
            access = True
        
    return access