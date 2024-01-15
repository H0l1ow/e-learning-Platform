CREATE DATABASE IF NOT EXISTS elearning;
USE elearning;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin BOOLEAN,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    vid1 BOOLEAN,
    vid2 BOOLEAN,
    vid3 BOOLEAN
);

INSERT INTO users (admin, username, password, vid1, vid2, vid3) Values (True ,'Rav', '1234', False, True, True);
INSERT INTO users (admin, username, password, vid1, vid2, vid3) Values (False ,'Dan', '4444', False, False, False);
INSERT INTO users (admin, username, password, vid1, vid2, vid3) Values (True ,'test', 'test', True, True, True);