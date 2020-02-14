from flask import Flask, render_template, request, redirect, url_for
import data_handling, util, database_manager
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():

    last_five_questions = database_manager.get_last_five()

    return render_template('index.html', questions = last_five_questions,
                           page_title = 'AskMate')

@app.route('/list')As   
def list():

    question_file = database_manager.import_questions_for_list()
    titles = ['ID','Submission time','Title',]
    sort = request.args.get('sort')
    search = request.args.get('search')

    if sort:
    # If sort has a value
        sorted_question_file = util.sort(sort)


        return render_template('list.html', titles=titles, questions=sorted_question_file,
                               page_title = 'AskMate - List of questions')

    if search:

        search_result = util.search_results(question_file,search)

        return render_template('list.html', titles=titles,questions=search_result,
                               page_title = 'AskMate - List of questions')

    return render_template('list.html',titles=titles, questions=question_file,
                           page_title = 'AskMate - List of questions')

@app.route('/add_question', methods=['GET','POST'])
def add():

    if request.method == "POST":


        title = request.form['title']
        message = request.form['message']
        id = database_manager.highest_id()
        view = 0
        vote = 0
        image = None
        timestamp = datetime.now().replace(microsecond=0)

        values = (id,timestamp,view,vote,title,message,image)
        database_manager.add_question(values)


        return redirect (url_for('question',id=id))

    return render_template('add_question.html', page_title = 'AskMate - Add question')

@app.route('/question/<id>', methods=['GET','POST'])
def question(id):

    try:
        id = int(id)
    except ValueError:
        return redirect('/list')

    question = database_manager.show_question(id)
    answers = database_manager.show_answers(id)
    page_title = 'Question ' + str(id)

    if question:

        database_manager.view_counter(question_id=id)

        return render_template('question.html', id=id,question=question, answers=answers, page_title=page_title)


    return redirect('/list')

@app.route('/question/<id>/new-answer', methods=['GET','POST'])
def add_answer(id):

    try:
        id = int(id)
    except ValueError:
        return redirect('/list')

    if database_manager.is_id_in_database(id):

        if request.method == 'POST':

            answer_id = database_manager.highest_answer_id()
            timestamp = datetime.now().replace(microsecond=0)
            vote_number = 0
            question_id = id
            message = request.form['message']
            image = None

            values = (answer_id,timestamp,vote_number,question_id,message,image)
            database_manager.add_answer(values)


            return redirect(url_for('question', id=question_id))

        return render_template('new_answer.html', id=id)


    return redirect('/')

@app.route('/answer/<id>', methods=['GET','POST'])
def answer(id):

    page_title = 'Answer ' + str(id)
    index = {'ANSWER_ID':0,'TIMESTAMP':1,'VOTE':2,'QUESTION_ID':3,'MESSAGE':4,'IMAGE':5}

    try:
        id = int(id)
    except ValueError:
        return redirect('/')

    answer = database_manager.show_answer_by_id(id)

    if answer:

        answer = answer[0]

        return render_template('answer.html',id=id, answer=answer, page_title=page_title, index=index)

    return redirect('/list')

@app.route('/question/<id>/delete', methods=['GET','POST'])
def delete_question(id):

    try:
        id = int(id)
    except ValueError:
        return redirect('/list')

    if database_manager.is_id_in_database(id):

        if request.method == 'POST':

            database_manager.delete_record_from_question(id)

            return redirect('/list')

        return render_template('delete_question.html', id=id)

    return redirect('list')


@app.route('/question/<id>/vote', methods=['GET','POST'])
def vote(id):

    try:
        id = int(id)
    except ValueError:
        return redirect('/list')

    question = database_manager.is_id_in_database(id=id)

    if question:

        if request.method == 'POST':

            if request.form['button'] == 'up':

                database_manager.vote_up(question_id=id)
                return redirect (url_for('question',id=id))

            elif request.form['button'] == 'down':

                database_manager.vote_down(question_id=id)
                return redirect(url_for('question',id=id))

        return render_template('vote.html', id=id)

    return redirect('/')

@app.route('/answer/<id>/vote', methods=['GET','POST'])
def vote_answer(id):

    try:
        id = int(id)
    except ValueError:
        return redirect('/')

    answer = database_manager.show_answer_by_id(id)
    page_title = 'Vote Answer ' + str(id)

    if answer:
        if request.method == 'POST':
            if request.form['button'] == 'up':
                database_manager.answer_vote_up(id)
                return redirect(url_for('answer', id=id))
            else:
                database_manager.answer_vote_down(id)
                return redirect(url_for('answer', id=id))

        return render_template('vote_answer.html', id=id, page_title=page_title)

    return redirect('/')

@app.route('/answer/<id>/delete', methods=['GET','POST'])
def delete_answer(id):

    try:
        id = int(id)
    except ValueError:
        return redirect('/')

    answer = database_manager.show_answer_by_id(id)

    if answer:
        if request.method == 'POST':
            database_manager.delete_answer(id)
            return redirect('/list')

        return render_template('delete_answer.html', id=id)

    return redirect('/')

@app.route('/answer/<id>/edit', methods=['GET','POST'])
def edit_answer(id):

    try:
        id = int(id)
    except ValueError:
        return redirect('/')

    answer = database_manager.show_answer_by_id(id)

    if answer:

        answer=answer[0]

        if request.method == 'POST':
            if request.form['message']:
                database_manager.edit_answer(id,request.form['message'])
                return redirect(url_for('answer', id=id))

        return render_template('edit_answer.html', id=id, answer=answer)

    return redirect('/')

if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=5000 # Set custom port
    )