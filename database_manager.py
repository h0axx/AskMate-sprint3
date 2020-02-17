import basic_db_usage

@basic_db_usage.connection_handler
def highest_id(cursor):
    cursor.execute("""
                    SELECT MAX(id) FROM question;
                    """)
    try:
        highest_id = cursor.fetchall()[0][0]
        highest_id += 1
    except:
        return 1

    return highest_id

@basic_db_usage.connection_handler
def highest_answer_id(cursor):
    cursor.execute("""
                    SELECT MAX(id) FROM answer;
                    """)
    try:
        highest_id = cursor.fetchall()[0][0]
        highest_id += 1
    except:
        return 1

    return highest_id

@basic_db_usage.connection_handler
def highest_user_id(cursor):
    cursor.execute("""
                    SELECT MAX(user_id) FROM users;
                    """)
    try:
        highest_id = cursor.fetchall()[0][0]
        highest_id += 1
    except:
        return 1

    return highest_id

@basic_db_usage.connection_handler
def is_id_in_database(cursor,id):


    cursor.execute("""SELECT id FROM question;""")
    ids = cursor.fetchall()
    for data in ids:
        for int in data:
            if int == id:
                return True

    return False

@basic_db_usage.connection_handler
def show_question(cursor,id):

    cursor.execute(""" 
                        SELECT * FROM question WHERE id = %s ;""", [id])

    question = cursor.fetchall()

    if question:
        question = question[0]
        return question

@basic_db_usage.connection_handler
def show_answers(cursor,question_id):

    cursor.execute("""
                    SELECT * FROM answer WHERE question_id = %s;""", [question_id])

    answer = cursor.fetchall()
    if answer:
        return answer

@basic_db_usage.connection_handler
def import_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                    """)
    questions = cursor.fetchall()
    return questions

@basic_db_usage.connection_handler
def add_question(cursor,values):

    cursor.execute("""
                    INSERT INTO question 
                    VALUES (%s,%s,%s,%s,%s,%s,%s) ;""",
                   (values[0],values[1],values[2],values[3],values[4],values[5],values[6],))

@basic_db_usage.connection_handler
def add_answer(cursor,values):

    cursor.execute("""
                    INSERT INTO answer
                    VALUES (%s,%s,%s,%s,%s,%s) ;""",
                   (values[0],values[1],values[2],values[3],values[4],values[5],))

@basic_db_usage.connection_handler
def sort_by_id(cursor):

    cursor.execute("""
                    SELECT id,submission_time,title 
                    FROM question
                    ORDER BY id desc; """)

    questions = cursor.fetchall()

    return questions

@basic_db_usage.connection_handler
def sort_by_view(cursor):
    cursor.execute("""
                SELECT id,submission_time,title
                FROM question
                ORDER BY view_number asc; """)
    questions = cursor.fetchall()

    return questions

@basic_db_usage.connection_handler
def sort_by_vote(cursor):
    cursor.execute("""
                SELECT id,submission_time,title
                FROM question
                ORDER BY vote_number asc;""")
    questions = cursor.fetchall()

    return questions

@basic_db_usage.connection_handler
def view_counter(cursor,question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %s; """, [question_id])

@basic_db_usage.connection_handler
def vote_up(cursor,question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number + 1
                    WHERE id = %s;""", [question_id])

@basic_db_usage.connection_handler
def vote_down(cursor,question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id = %s;""", [question_id])

@basic_db_usage.connection_handler
def get_last_five(cursor):
    cursor.execute("""
                    SELECT id,title
                    FROM question
                    ORDER BY id DESC;""")
    questions = cursor.fetchall()

    if len(questions) > 5:
        last_five_or_less = questions[:5]
    else:
        last_five_or_less = questions


    return last_five_or_less

@basic_db_usage.connection_handler
def delete_record_from_question(cursor,question_id):

    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %s;""",[question_id])

    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %s;""", [question_id])

@basic_db_usage.connection_handler
def import_questions_for_list(cursor):
    cursor.execute("""
                    SELECT id,submission_time,title FROM question;
                    """)
    questions = cursor.fetchall()
    return questions

@basic_db_usage.connection_handler
def show_answer_by_id(cursor,answer_id):
    cursor.execute("""
                    SELECT * 
                    FROM answer
                    WHERE id = %s;""", [answer_id])

    answer = cursor.fetchall()
    return answer

@basic_db_usage.connection_handler
def answer_vote_up(cursor,answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + 1
                    WHERE id = %s;""", [answer_id])

@basic_db_usage.connection_handler
def answer_vote_down(cursor,answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number - 1
                    WHERE id = %s;""", [answer_id])

@basic_db_usage.connection_handler
def delete_answer(cursor,answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %s;""", [answer_id])

@basic_db_usage.connection_handler
def edit_answer(cursor,answer_id,message):
    cursor.execute("""
                    UPDATE answer
                    SET message = %s
                    WHERE id = %s;""",[message,answer_id])

@basic_db_usage.connection_handler
def add_user(cursor,values):
    cursor.execute("""
                    INSERT INTO users
                    VALUES (%s,%s,%s,%s);""",
                   (values[0],values[1],values[2],values[3]))

@basic_db_usage.connection_handler
def is_user_in_db(cursor,username,email):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE username = %s OR email = %s; """,
                   (username,email))

    result = cursor.fetchall()

    if result:
        return True
    else:
        return False

@basic_db_usage.connection_handler
def grab_password_from_db(cursor,username):

    cursor.execute("""
                    SELECT password
                    FROM users
                    WHERE username = %s;""",
                   (username,))

    password = cursor.fetchall()[0][0]

    return password

@basic_db_usage.connection_handler
def getUserIdByUsername(cursor,username):

    cursor.execute("""
                    SELECT user_id
                    FROM users
                    WHERE username = %s;""",
                   (username))

    userId = cursor.fetchall()[0][0]

    return userId