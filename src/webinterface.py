from bottle import template


# Class to create webpages to bottle from templates. Templates are saved in ./views
class WebInterface:
    def __init__(self, studentdb):
        self.student_database = studentdb
        self.page_number = 0

    # gets all the students at Hive Helsinki
    def get_students(self):
        data = self.student_database.get_students()
        html_insert = ''
        for student in data:
            html_insert += '<a href="/student/' + student['login'] + '">' + student[
                'login'] + '</a>, total points: ' + str(student['total_points']) + '<br>\n'
        return template('students', students=html_insert, style="styles.css")

    # get the page of a single student
    def get_student_page(self, login):
        student_data = self.student_database.get_student(login)
        student_evals = self.student_database.get_evals(login)
        html_insert = '<h1>' + login + '</h1></div><div class="card">'
        html_insert += '<p>Total points: ' + str(student_data['total_points']) + '</p>'
        html_insert += '<p>Eval point average: ' + str(student_data['avarage_points']) + '</p>'
        html_insert += '<p>Amount of evals: ' + str(student_data['evals']) + '</p>'
        html_insert += '<p>Too friendly points: ' + str(
            student_data['too_friendly_points']) + '</p><br><h2>Students evals</h2>'
        for data in student_evals:
            html_insert += '<a href="/eval/' + str(data['id']) + '">' + str(
                data['id']) + '</a><br>total_points: ' + str(data['total_points']) + '<br>time: ' + data[
                               'begin_at'] + '<br>corrector: ' + data['corrector'] + '<br>correcteds: ' + data[
                               'corrected1']
            if data['corrected2']:
                html_insert += ' ' + data['corrected2']
            if data['corrected3']:
                html_insert += ' ' + data['corrected3']
            if data['corrected4']:
                html_insert += ' ' + data['corrected4']
            html_insert += '<br><br>\n'
        return template('student', html_insert=html_insert, style="style.css")

    # the landing page
    def get_start(self):
        unicorns = 'burpuni.gif'
        return template('start', picture=unicorns, style='styles.css')

    # front page after database has been created
    def get_index(self):
        return template('index', style="styles.css")

    # page listing all the evaluations
    def get_evals(self, start=None, end=None, page=1):
        start_index = (int(page) - 1) * 20
        evals = self.student_database.get_evals(start=start_index, start_date=start, end_date=end)
        html_insert = ''
        if (not evals) and start:
            html_insert = '<p>error with search dates</p>'
            return template('evals', evals=html_insert, style="styles.css")
        if not evals:
            return template('evals', evals=html_insert, style="styles.css")
        date_str = ''
        if start and end:
            date_str = "&eval_start=" + start + "&eval_end=" + end
        if int(page) > 1:
            html_insert += '<a href="/evals?page=' + str(int(page) - 1) + date_str + '" style="float:right;">prev</a>'
        if evals:
            html_insert += '<a href="/evals?page=' + str(int(page) + 1) + date_str + '" style="float:left;">next</a' \
                                                                                     '><br><br> '
        start_str = start or ''
        end_str = end or ''
        html_insert += '<form action="/evals" method="get"><input type="hidden" name="eval_start" value="' + start_str + '"> <input type="hidden" name="eval_end" value="' + end_str + '"><input type="hidden" name="csv" value=1><button type="submit" value="Submit">Create .csv</button></form> <br><br>'
        for data in evals:
            html_insert += '<a href="/eval/' + str(data['id']) + '">' + str(
                data['id']) + '</a><br>total_points: ' + str(data['total_points']) + '<br>time: ' + data[
                               'begin_at'] + '<br>corrector: ' + data['corrector'] + '<br>correcteds: ' + data[
                               'corrected1']
            if data['corrected2']:
                html_insert += ' ' + data['corrected2']
            if data['corrected3']:
                html_insert += ' ' + data['corrected3']
            if data['corrected4']:
                html_insert += ' ' + data['corrected4']
            html_insert += '<br><br>\n'
        return template('evals', evals=html_insert, style="styles.css")

    # page for single eval with more information. For some reason I did not get the python code to work on templates,
    # so I am passing every value separately..
    def get_eval(self, scale_id):
        one_eval = self.student_database.get_eval(scale_id)
        project_name = self.student_database.get_project_name(one_eval['project_id'])
        correcteds = one_eval['corrected1']
        if one_eval['corrected2']:
            correcteds += ', ' + one_eval['corrected2']
        if one_eval['corrected3']:
            correcteds += ', ' + one_eval['corrected3']
        if one_eval['corrected4']:
            correcteds += ', ' + one_eval['corrected4']
        corrector = one_eval['corrector']
        comment = one_eval['comment']
        comment_points = one_eval['comment_points']
        final_mark = one_eval['final_mark']
        final_mark_points = one_eval['final_mark_points']
        begin_at = one_eval['begin_at']
        duration = one_eval['duration']
        duration_points = one_eval['duration_points']
        feedback_comment = one_eval['feedback_comment']
        feedback_rating = one_eval['feedback_points']
        feedback_points = one_eval['feedback_total_points']
        too_friendly_points = one_eval['too_friendly_points']
        return template('eval', too_friendly_points=too_friendly_points, one_eval=one_eval, project_name=project_name,
                        corrector=corrector, correcteds=correcteds, style="styles.css", comment=comment,
                        comment_points=comment_points, final_mark=final_mark, final_mark_points=final_mark_points,
                        begin_at=begin_at, duration=duration, duration_points=duration_points,
                        feedback_comment=feedback_comment, feedback_rating=feedback_rating,
                        feedback_points=feedback_points)

    def get_search(self, error_str=''):
        return template('search', style="styles.css", errorstr=error_str)

    def get_csv(self, start=None, end=None):
        self.student_database.get_csv(start, end)
        return
