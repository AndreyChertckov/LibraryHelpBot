# Library Help Bot

## Purpose of the application

This is the implementation of Library Management System (LMS). LMSs are used in libraries to track the different items in the library. The system contains all information about books, magazines, audio/video materials, as well as people allowed to check out the materials or those in charge of the management. LMS is implemented as a Telegram bot.

## How it works
[![How it work picture](https://github.com/LibrinnoTeam/LibraryHelpBot/blob/master/howitworks.png?raw=true)](https://github.com/LibrinnoTeam/LibraryHelpBot)


1.  Bot package sends request to Telegram via API and as a response it gets messages from users exploiting the bot.
2.  Bot analyzes the response and sends commands to the controller which executes the command and makes according changes in the database.

## Dependencies
* wheel
* python-telegram-bot
* pytest
* flask
* PyMySQL
* PySocks

## Installation

### Requirements
* python3
* pip3
* git
## Preparing
1.  Install all libraries stated in the requirements.txt by typing the command below in command line.
    ```sh
    pip3 install -r requirements.txt
    ```
2.  Install MariaDB from official site
3.  Downlaod the repository from Github
First way is to download zip archive and then unzip it to the work directory.
Second way is to clone repository to the work directory via
    ```sh
    git clone https://github.com/LibrinnoTeam/LibraryHelpBot.git
    ```
4.  Change password in database-schema.sql 
5.  Execute database-schema.sql in MariaDB
    ```sh
    source path/to/work/directory/AdminSite/database-schema.sql
    ```
6.  Create file configs.py in work directory
    ```sh
    token                     = '*' # Token for telegram bot 
    library_login_database    = 'admin_library' # login for library user MariaDB
    library_password_database = '*'
    library_database          = 'library' #May be change

    admin_user_login = 'admin'
    admin_user_pass = '*'

    host = 'localhost' #May be change
    port = '8080' #May be change

    inet_addr = 'localhost' #May be change

    debug = False

    telegram_alias = 'compet_bot' #May be change
    ```
    
## Running
1.  To run the application with default parameters just typing the command below in command line.
   ```sh
    python3 main.py
    ```
2.  General view of the command that starts a bot
    ```sh
    python3 main.py -t -c --log_file=<filelog> --database=<filedb> --cleanup_database
```
>   Argument -t means that the command runs the tests
Argument -c means that the application will write logs into console
Argument --log_file= means that the application will write logs into file with name in parameter
Argument --database= means that the application will use bd in file with name in parameter
> Argument --cleanup_database means that the application will drop tables in database
