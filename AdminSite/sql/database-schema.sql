

CREATE DATABASE librarian_site CHARACTER SET UTF8;
-- replace * on password

CREATE USER 'admin_site'@'localhost' IDENTIFIED BY 'PNt78mtJeQ3RJbZz';
GRANT ALL PRIVILEGES ON librarian_site.* TO 'admin_site'@'localhost';
FLUSH PRIVILEGES;
