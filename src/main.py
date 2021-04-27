import bottle
from bottle import route, run, redirect, post, request, static_file
from webinterface import WebInterface
from database import StudentDatabase

app = bottle.app()
studentdb = StudentDatabase()
web = WebInterface(studentdb)
user = ''


# Bottle calls for different pages. @route returns the html string to Bottle app to publish.
# get request can be processed in the @route sections, but post requests should be handled
# with separate @post functions. @route('/student/<login>') reads the login from url and the
# function connected to this @route uses login as a parameter that can be passed to webinterface.
# Static files like images and the css file are handled separately in the end of the file.
# The run command starts and runs the service.

@route('/')
def start():
    html_str = web.get_start()
    return html_str


@post('/')
def redirect_to_wait():
    button = request.forms.get('start')
    if button:
        redirect('/wait')


@route('/wait')
def wait():
    start_database = request.query.start or None
    end_database = request.query.end or None
    print(start_database)
    print(end_database)
    studentdb.init_database(start_database, end_database)
    redirect("/index")


@route('/index')
def index():
    html_str = web.get_index()
    return html_str


@route('/students')
def students():
    html_str = web.get_students()
    return html_str


@route('/student/<login>')
def student(login):
    html_str = web.get_student_page(login)
    return html_str


@route('/evals')
def evals():
    page = request.query.page or 1
    start_evals = request.query.get('eval_start') or None
    end_evals = request.query.get('eval_end') or None
    csv = request.query.get('csv') or 0
    if csv:
        web.get_csv(start=start_evals, end=end_evals)
        return static_file('output.csv', root='./static/', download='output.csv')
    html_str = web.get_evals(page=page, start=start_evals, end=end_evals)
    return html_str


@route('/eval/<eval_id>')
def one_eval(eval_id):
    html_str = web.get_eval(eval_id)
    return html_str


@route('/search')
def search():
    search_get = request.query.decode()
    eval_start = search_get.get('eval_start')
    eval_end = search_get.get('eval_end')
    error_str = ''
    if eval_start and eval_end:
        redirect("/evals?eval_start=" + eval_start + "&eval_end=" + eval_end)
    if eval_start or eval_end:
        error_str = "Select start and end date"
    html_str = web.get_search(error_str)
    return html_str


@route('/images/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='images')


@route('/static/<filename>')
def send_static(filename):
    return static_file(filename, root='./static/')


run(host='0.0.0.0', port=6660, debug=True)
