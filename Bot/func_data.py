keyboard_dict = {
    "unauth": [['Registration📝', 'Library🏤', 'Search🔎', 'Help👤']],
    "unconf": [['Library🏤', 'Search🔎', 'Help👤']],
    "auth": [['Library🏤', 'Search🔎', 'My Books📚', 'Help👤']],
    "admin": [["Check material📆", "Material management📚", "User management👥"]],
    "mat_management": [["Add material🗄", "Search🔎", "Cancel⤵"]],
    "user_management": [["Confirm application📝", "Check overdue📋", "Show users👥", "Cancel⤵️"]],
    "reg_confirm": [["All is correct✅", "Something is incorrect❌"]],
    "lib_main": [['Books📖', 'Journal Articles📰', "Audio/Video materials📼", "Cancel⤵️"]],
    "cancel": [['Cancel⤵']],
    "status": [['Student', 'Faculty (professor, instructor, TA)']]
}

sample_messages = {
    'reg': """
        During registration you have to provide your name, address, phone number and status (student or faculty).\n
        Example:
        Ivan Ivanov,
        ul. Universitetskaya 1, 2-100,
        +71234567890,
        Student     
        """,

    'correctness': """
        Check whether all data is correct:
        Name: {name}
        Address: {address}
        Phone: {phone}
        Status: {status}
        """,

    'book': """
        You have to provide book's title, authors, overview, keywords and price (in rubles).\nExample:
        Introduction to Algorithms, The third edition
        Thomas H. Cormen; Charles E. Leiserson; Ronald L. Rivest
        This book is about algorithms
        algorithms; java
        3000
        """
}

user_types = ['unauth', "unconf", "auth", 'admin']