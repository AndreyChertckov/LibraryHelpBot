

CREATE DATABASE librarian_site CHARACTER SET UTF8;
-- replace * on password

CREATE USER 'admin_site'@'localhost' IDENTIFIED BY 'PNt78mtJeQ3RJbZz';
GRANT ALL PRIVILEGES ON librarian_site.* TO 'admin_site'@'localhost';

CREATE DATABASE library CHARACTER SET UTF8;
-- replace * on password

CREATE USER 'admin_library'@'localhost' IDENTIFIED BY 'I53VGk2ZDHefTa1w';
GRANT ALL PRIVILEGES ON library.* TO 'admin_library'@'localhost';
FLUSH PRIVILEGES;

