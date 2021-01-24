-- IMP: CREATE DATABASE
-- USE THIS DATABASE NAME IN main.py
CREATE DATABASE bookshelf_2;

-- IMP: USE THIS DATABASE
USE bookshelf_2;

-- IMP: Create User Table
CREATE TABLE user(
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60),
    email VARCHAR(70),
    password VARCHAR(10) NOT NULL DEFAULT '1234'
);

-- IMP: Create Book Table
CREATE TABLE books(
    book_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(120),
    author VARCHAR(70),
    category VARCHAR(40),
    user_id INT,
    PRIMARY KEY (book_id),
    FOREIGN KEY(user_id) REFERENCES user(user_id)
);


