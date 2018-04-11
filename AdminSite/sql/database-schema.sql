CREATE DATABASE library CHARACTER SET UTF8;
CREATE USER 'admin_library'@'localhost' IDENTIFIED BY 'I53VGk2ZDHefTa1w';
GRANT ALL PRIVILEGES ON library.* TO 'admin_library'@'localhost';
FLUSH PRIVILEGES;