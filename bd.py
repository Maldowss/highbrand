import pymysql


def conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='highbrand'
    )

# BBDD:


# CREATE TABLE IF NOT EXISTS users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user VARCHAR(255) NOT NULL,
#     password VARCHAR(255) NOT NULL
# )ENGINE=InnoDB;

# CREATE TABLE IF NOT EXISTS clothes (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     nombre VARCHAR(255),
#     marca VARCHAR(255),
#     precio VARCHAR(255),
#     imagen VARCHAR(255),
#     url VARCHAR(255),
#     user_id INT,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# )ENGINE=InnoDB;


# CREATE TABLE IF NOT EXISTS user_info (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user VARCHAR(255),
#     name VARCHAR(255),
#     last_name VARCHAR(255),
#     email VARCHAR(255),
#     tlf VARCHAR(20),
#     user_id INT,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# )ENGINE=InnoDB;

# CREATE TABLE  IF NOT EXISTS comments (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(255),
#     text VARCHAR(255),
#     user_id INT,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# )ENGINE=InnoDB;


# create TABLE if not EXISTS favorites(
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     clothe_id INT,
#     nombre VARCHAR(255),
#     marca VARCHAR(255),
#     precio VARCHAR(255),
#     imagen VARCHAR(255),
#     url VARCHAR(255),
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
#     FOREIGN KEY (clothe_id) REFERENCES clothes(id) ON DELETE CASCADE
# )ENGINE=INNODB;
