keyboard_dict = {
    "unauth": [['Registration📝', 'Library🏤', 'Search🔎', 'Help👤']],
    "unconf": [['Library🏤', 'Search🔎', 'Help👤']],
    "auth": [['Library🏤', 'Search🔎', 'My Books📚', 'Help👤']],
    "admin": [["Check material📆", "Material management📚", "User management👥"]],
    "mat_management": [["Add material🗄", "Search🔎", 'Cancel⤵️']],
    "user_management": [["Confirm application📝", "Check overdue📋", "Show users👥", 'Cancel⤵️']],
    "reg_confirm": [["All is correct✅", "Something is incorrect❌"]],
    "lib_main": [['Books📖', 'Journal Articles📰', "Audio/Video materials📼", 'Cancel⤵️']],
    "cancel": [['Cancel⤵']],
    "status": [['Student', 'Faculty (professor, instructor, TA)']]
}

sample_messages = {
    'reg': """
        You have to provide your name, address, phone number and status (student or faculty).\n
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

    'correctness_book': """
        Check whether all data is correct:
        Title: {title}
        Authors: {authors}
        Overview: {overview}
        Keywords: {keywords}
        Price: {price}
    """,

    'correctness_article': """
        Check whether all data is correct:
        Title: {title}
        Authors: {authors}
        Journal: {journal}
        Issue: {issue}
        Editors: {editors}
        Keywords: {keywords}
        Price: {price}
    """,

    'correctness_media': """
        Check whether all data is correct:
        Title: {title}
        Authors: {authors}
        Keywords: {keywords}
        Price: {price}
    """,

    'book': "You have to provide book's title, authors, overview, list of keywords and price (in rubles).",

    'article': "You have to provide article's title, one or more authors, title of journal and its issue with editors and a\
        publication date. Also you need to provide list of keywords and price (in rubles).",

    'media': "You have to provide title, list of authors, list of keywords and price"
}

lists = {
    "user_types": ['unauth', "unconf", "auth", 'admin'],
    "reg_fields": ["name", "address", "phone", "status"],
    "book": ['title', ' list of authors (separated by ";")', 'overview', 'keywords (separated by ";")', 'price'],
    "article": ['title', ' list of authors (separated by ";")', 'journal title', 'issue', 'issue editors',
                'date of publication', 'keywords (separated by ";")', 'price'],
    "media": ['title', ' list of authors (separated by ";")', 'keywords (separated by ";")', 'price'],
    "book_bd": ['title', 'authors', 'overview', 'keywords', 'price'],
    "article_bd": ['title', 'authors', 'journal', 'issue', 'editors', 'date', 'keywords', 'price'],
    "media_bd": ['title', 'authors', 'keywords', 'price'],
}
