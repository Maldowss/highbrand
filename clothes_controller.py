from bd import conexion
import os
import bcrypt

def query_clothes():
    conexion_db= conexion()
    clothes = []
    with conexion_db.cursor() as cursor:
        cursor.execute('SELECT * FROM clothes')
        clothes = cursor.fetchall()
    conexion_db.close()
    return clothes

def query_clothes_admin(id):
    conexion_db= conexion()
    clothes = []
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT * FROM clothes where user_id= %s", (id))
        clothes = cursor.fetchall()
    conexion_db.close()
    return clothes

def query_clothes_favorites(id):
    conexion_db= conexion()
    clothes = []
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT * FROM favorites where user_id= %s", (id))
        clothes = cursor.fetchall()
    conexion_db.close()
    return clothes

def search_clothes(search):
    conexion_db= conexion()
    clothes = []
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT * FROM clothes WHERE marca LIKE %s", (search))
        clothes = cursor.fetchall()
        conexion_db.close()
    return clothes

def insert_clothe(name, brand, price, image, url, user_id):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("INSERT INTO clothes(nombre, marca, precio, imagen, url, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, brand, price, image, url, user_id))
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

def delete_images_directory(id):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT imagen from clothes WHERE user_id = %s", (id))
        clothes=cursor.fetchall()

        for clothe in clothes:
            if os.path.exists("templates/web/img/"+str(clothe[0])):
                os.unlink("templates/web/img/" + str(clothe[0]))

    conexion_db.commit()
    conexion_db.close()

def update_clothe(id, name, brand, price, image, url, condition):
    if condition == True:
        delete_image_directory(id)

    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("UPDATE clothes SET nombre=%s, marca=%s, precio=%s, imagen=%s, url=%s WHERE id=%s",
                       (name, brand, price, image, url, id))
    conexion_db.commit()
    conexion_db.close()

def login_authentication(user, password):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT user, password FROM users WHERE user=%s", (user))
        user_data = cursor.fetchone()

        
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
            access = True
        else:
            access = False

        return access
    
def register_user(user, password):
    pwd = password.encode('utf-8')
    sal = bcrypt.gensalt()
    encript = bcrypt.hashpw(pwd, sal)
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("INSERT INTO users(user, password) VALUES (%s, %s)",
                       (user, encript))
    conexion_db.commit()
    conexion_db.close()

def delete_user(id):
    delete_images_directory(id)
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("DELETE FROM users where id = %s", (id))
    conexion_db.commit()
    conexion_db.close()

def query_id_user(user):
    conexion_db= conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT id FROM users where user like %s", (user))
        id = cursor.fetchone()
    conexion_db.close()
    return id

def query_user(id):
    conexion_db= conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT user FROM users where id= %s", (id))
        user = cursor.fetchone()
    conexion_db.close()
    return user

def query_info_user(id):
    conexion_db= conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT * FROM user_info where user_id= %s", (id))
        user = cursor.fetchone()
    conexion_db.close()
    return user

def check_user_existence(user):
    conexion_db= conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT user FROM users where user like %s", (user))
        cUser = cursor.fetchone()
    conexion_db.close()
    if cUser is None:
        return False
    elif len(cUser) > 0:
        return True
    
def insert_comment(name, text, _id_user):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("INSERT INTO comments(name, text, user_id) VALUES (%s, %s, %s)",
                       (name, text, _id_user))
    conexion_db.commit()
    conexion_db.close()

def query_comments():
    conexion_db= conexion()
    comments = []
    with conexion_db.cursor() as cursor:
        cursor.execute('SELECT * FROM comments')
        comments = cursor.fetchall()
    conexion_db.close()
    return comments

def update_user_info(name, last_name, email, tlf, id_user):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("UPDATE user_info SET name=%s, last_name=%s, email=%s, tlf=%s WHERE user_id=%s",
                       (name, last_name, email, tlf, id_user))
    conexion_db.commit()
    conexion_db.close()

def add_favorite( user_id, clothe_id, name, brand, price, image, url):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("INSERT INTO favorites(user_id, clothe_id, nombre, marca, precio, imagen, url) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (user_id, clothe_id, name, brand, price, image, url))
    conexion_db.commit()
    conexion_db.close()

def delete_favorite(user_id, clothe_id):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("DELETE FROM favorites WHERE user_id = %s AND clothe_id = %s", (user_id, clothe_id))
    conexion_db.commit()
    conexion_db.close()

def check_favorites(user_id, clothe_id):
    conexion_db = conexion()
    with conexion_db.cursor() as cursor:
        cursor.execute("SELECT * FROM favorites WHERE user_id = %s AND clothe_id = %s", (user_id, clothe_id))
        data = cursor.fetchone()
    conexion_db.commit()
    conexion_db.close()
    if data is None:
        return False
    elif len(data) > 0:
        return True