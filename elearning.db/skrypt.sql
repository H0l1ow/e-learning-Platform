CREATE DATABASE IF NOT EXISTS elearning;
USE elearning;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'admin');
INSERT INTO users (username, password) VALUES ('Dan', '4444');
INSERT INTO users (username, password) VALUES ('Rav', '1234');
