SET sql_notes = 0;
CREATE TABLE IF NOT EXISTS librarians (id INTEGER PRIMARY KEY AUTO_INCREMENT, login TEXT,password TEXT,name TEXT NOT NULL,phone TEXT,address TEXT,chat_id TEXT,privilege TINYINT);
CREATE TABLE IF NOT EXISTS sessions (id VARCHAR(32) PRIMARY KEY, user_id INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS verification_string (string VARCHAR(32) PRIMARY KEY, user_id INTEGER, is_authentication BIT(1) NOT NULL, privilege TINYINT);
SET sql_notes = 1;