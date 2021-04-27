import os
import sqlite3
from os import path
import re
from intra import IntraAPIClient
from datetime import datetime
import csv

# Class StudentDatabase used to create and get requests from SQLite database. When first
# initiating the class, the __init__ function does not open connection to the database. This
# is done later in init_database function, so that the database building can be done after
# Bottle has created the landing page. After the initiation functions there is a bunch of
# getter that the web interface uses to make queries to fetch data from the database.
# Below those are the functions for creating the database and calculating the evaluation
# and student points.

ic = IntraAPIClient()
time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
time_format_sql = '%Y-%m-%d %H:%M:%S'


class StudentDatabase:
    # Function used to initialize the database. The creation takes time!
    # For efficiency while developing the database, init will check from table "tables"
    # if the next part of database creation is finished and only continues when necessary
    def init_database(self, start, end):
        if not (path.exists('./student.db')):
            self.database = sqlite3.connect('./student.db')
            self.database.row_factory = sqlite3.Row
            self.database.execute("CREATE TABLE tables (name TEXT, status INT, created DATETIME, updated DATETIME)")
            self.database.execute(
                "INSERT INTO tables (name, status) VALUES (\"students\", 0), (\"scales\", 0), (\"projects\", 0), "
                "(\"student_points\", 0), (\"eval_points\", 0), (\"too_friendly\", 0)")
            self.database.commit()
        else:
            self.database = sqlite3.connect('./student.db')
            self.database.row_factory = sqlite3.Row
            self.database.commit()
        cursor = self.database.cursor()
        student_ready = cursor.execute("SELECT status FROM tables WHERE name = \"students\"").fetchone()
        if not (student_ready['status']):
            self.database.execute("drop table if exists students")
            self.database.execute(
                "CREATE TABLE students(id INTEGER, login TEXT, url TEXT, too_friendly_points INT DEFAULT 0, "
                "total_points INT DEFAULT 0, evals INT DEFAULT 0, avarage_points INT DEFAULT 0)")
            self.save_students()
        projects_ready = cursor.execute("SELECT status FROM tables WHERE name = \"projects\"").fetchone()
        if not (projects_ready['status']):
            self.database.execute("drop table if exists projects")
            self.database.execute("CREATE TABLE projects (project_id INT, name TEXT, slug TEXT)")
            self.save_projects()
        scales_ready = cursor.execute("SELECT status FROM tables WHERE name = \"scales\"").fetchone()
        if not (scales_ready['status']):
            self.database.execute("drop table if exists scales")
            self.database.execute(
                "CREATE TABLE scales(corrector TEXT, total_points INT DEFAULT 0, id INT, scale_id INT, project_id "
                "INT, comment TEXT, comment_points INT DEFAULT 0, final_mark INT, final_mark_points INT DEFAULT 0, "
                "begin_at DATETIME, corrected1 TEXT, corrected2 TEXT, corrected3 TEXT, corrected4 TEXT, "
                "too_friendly_points INT DEFAULT 0, filled_at DATETIME, duration INT, duration_points INT DEFAULT 0, "
                "true_flags INT, flags_points INT DEFAULT 0, feedback_comment TEXT, feedback_rating INT, feedback_id "
                "INT, feedback_points INT, feedback_interested INT, feedback_nice INT, feedback_punctuality INT, "
                "feedback_rigorous INT, feedback_total_points INT DEFAULT 0, team_id INT)")
            self.save_scale_teams(start=start, end=end)
        eval_points_ready = cursor.execute("SELECT status FROM tables WHERE name = \"eval_points\"").fetchone()
        if not (eval_points_ready['status']):
            self.save_eval_points()
        friendly_points_ready = cursor.execute("SELECT status FROM tables WHERE name = \"too_friendly\"").fetchone()
        if not (friendly_points_ready['status']):
            self.save_friendly_points()
        student_points_ready = cursor.execute("SELECT status FROM tables WHERE name = \"student_points\"").fetchone()
        if not (student_points_ready['status']):
            self.save_student_points()
        self.database.commit()

    def __init__(self):
        self.database = None
        self.start = ''
        self.end = ''

    #############
    #  GETTERS  #
    #############

    # getters for WebInterface to use

    def get_database(self):
        return self.database

    # ordered from least to most points, with people with 0 points in the bottom
    def get_students(self):
        cursor = self.database.cursor()
        rows = cursor.execute(
            "SELECT id, login, url, total_points, avarage_points FROM students ORDER BY total_points=0, avarage_points, login")
        return (rows)

    def get_student(self, login):
        cursor = self.database.cursor()
        student = cursor.execute(
            "SELECT id, login, url, too_friendly_points, total_points, evals, avarage_points FROM students WHERE "
            "login = ?",
            (login,)).fetchone()
        return student

    def get_eval(self, eval_id):
        cursor = self.database.cursor()
        one_eval = cursor.execute(
            "SELECT corrector, total_points, id, project_id, comment, comment_points, final_mark, final_mark_points, "
            "begin_at, corrected1, corrected2, corrected3, corrected4, too_friendly_points, duration, duration_points, "
            "flags_points, feedback_comment, feedback_points, feedback_total_points FROM scales WHERE id =" + str(
                eval_id)).fetchone()
        return one_eval

    # Already has possibility to get data ordered in different ways, I just do not have time to implement it on
    # the front! Also, the amount of evals in one page could be easily implemented to one that can be changed.
    # Start and end dates work already, allowing the search to get only some evals. Pagination works also with
    # start and end
    def get_evals(self, login=None, start=0, amount=20, order='total_points', start_date=None, end_date=None):
        cursor = self.database.cursor()
        if login:
            evals = cursor.execute(
                'SELECT total_points, id, project_id, begin_at, corrector, corrected1, corrected2, corrected3, '
                'corrected4 FROM scales WHERE corrector = "' + login + '" ORDER BY ' + order)
        elif end_date is None and start_date is None:
            evals = cursor.execute(
                "SELECT total_points, id, project_id, begin_at, corrector, corrected1, corrected2, corrected3, "
                "corrected4 FROM scales ORDER BY " + order + " LIMIT " + str(
                    amount) + " OFFSET " + str(start))
        else:
            start_time = datetime.strptime(start_date, '%Y-%m-%d')
            start_time = start_time.replace(hour=00, minute=00, second=00)
            end_time = datetime.strptime(end_date, '%Y-%m-%d')
            end_time = end_time.replace(hour=23, minute=59, second=59)
            start_str = start_time.strftime(time_format_sql)
            end_str = end_time.strftime(time_format_sql)
            evals = cursor.execute(
                'SELECT total_points, id, project_id, begin_at, corrector, corrected1, corrected2, corrected3, '
                'corrected4 FROM scales WHERE begin_at BETWEEN "' + start_str + '" AND "' + end_str + '" ORDER BY ' +
                order + ' LIMIT ' + str(amount) + ' OFFSET ' + str(start))
        return evals

    def get_project_name(self, project_id):
        project = self.database.execute("SELECT slug FROM projects WHERE project_id = " + str(project_id)).fetchone()
        project_name = project[0]
        return project_name

    #########################
    #   Database creation   #
    #########################

    # student database creation. Gets all the students of Hive Helsinki campus threaded.
    def save_student(self, student):
        cursor = self.database.cursor()
        cursor.execute("INSERT INTO students (id, login, url) VALUES (?, ?, ?)",
                       (student['id'], student['login'], student['url']))
        self.database.commit()
        return

    # saving of a single student. if there is string 3b3 in the login, meaning that there is no 
    # proper login saved in the database, the student info is not saved.
    def save_students(self):
        pattern = re.compile('3b3')
        response_list = ic.pages_threaded("campus/13/users")
        for i in response_list:
            if pattern.search(i['login']):
                continue
            else:
                self.save_student(i)
        cursor = self.database.cursor()
        time = datetime.now().strftime(time_format_sql)
        cursor.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"students\"", (time,))
        self.database.commit()
        return

    # project database creation. Downloads all the projects threaded from 42 cursus. Does a double check to see
    # that the project is assigned to Hive Helsinki.
    def save_projects(self):
        response_list = ic.pages_threaded("cursus/1/projects")
        self.save_project(response_list)
        time = datetime.now().strftime(time_format_sql)
        self.database.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"projects\"", (time,))
        self.database.commit()

    def save_project(self, project):
        for i in project:
            for w in (i['campus']):
                if w['id'] == 13:
                    self.database.execute("INSERT INTO projects (project_id, name, slug) VALUES (?, ?, ?)",
                                          (i['id'], i['name'], i['slug']))
        self.database.commit()

    # scale teams database creations. Gets the list of students from database, and uses the student id to
    # fetch all the evaluations where the student was an evaluator from the database. Goes through the list
    # it gets as the aswer and saves every individual scale team into database.
    def save_scale_teams(self, start, end):
        cursor = self.database.cursor()
        student_ids = cursor.execute("SELECT id, login FROM students")
        for i in student_ids:
            self.save_student_teams(i['id'], start, end)
        time = datetime.now().strftime(time_format_sql)
        self.database.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"scales\"", (time,))
        self.database.commit()

    # Saves the scales teams of a one student where they have been the corrector. Fetches only the time frame
    # that was given in the landing page for database creation.
    def save_student_teams(self, student_id, start, end):
        if not start:
            start = "2021-04-01"
        if not end:
            end = "2021-04-25"
        url = 'users/' + str(student_id) + '/scale_teams/as_corrector?range[begin_at]=' + start + ',' + end
        data = ic.pages_threaded(url)
        for i in data:
            self.save_scale_team(i)

    # The saving of a single scale team = evaluation.
    def save_scale_team(self, team):
        # checking that the evaluation did actually happen
        if (not team) or team['truant'] or (not team['feedback']) or (not team['feedback'][0]):
            return
        # adding only evaluations that happened after c-piscine for this test version by comparing the evaluated
        # project to the saved projects.
        project = self.database.execute(
            "SELECT name FROM projects WHERE project_id = " + str(team['team']['project_id'])).fetchone()
        if not project:
            return
        # saving some values for later use
        scale_id = team['id']
        feedback_id = team['feedbacks'][0]['id']
        start_time = datetime.strptime(team['begin_at'], time_format)
        end_time = datetime.strptime(team['filled_at'], time_format)
        begin_str = start_time.strftime(time_format_sql)
        filled_str = end_time.strftime(time_format_sql)
        # saving most of the data, those that do not need any more processing.
        cursor = self.database.cursor()
        cursor.execute(
            "INSERT INTO scales (corrector, id, scale_id, project_id, comment, final_mark, begin_at, filled_at, "
            "duration, feedback_comment, feedback_rating, feedback_id, team_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
            "?, ?, ?)",
            (team['corrector']['login'], team['id'], team['scale_id'], team['team']['project_id'], team['comment'],
             team['final_mark'], begin_str, filled_str, team['scale']['duration'], team['feedbacks'][0]['comment'],
             team['feedbacks'][0]['rating'], team['feedbacks'][0]['id'], team['team']['id']))
        # add correcteds and removing evaluations with people with no proper login
        i = 0
        pattern = re.compile('3b3')
        for person in team['correcteds']:
            if pattern.search(person['login']):
                cursor.execute('DELETE FROM scales WHERE id = ' + str(scale_id))
                self.database.commit()
                return
            if i < 4:
                executable = "UPDATE scales SET corrected" + str(i + 1) + " = \"" + person[
                    'login'] + "\" WHERE id = " + str(scale_id)
                cursor.execute(executable)
            i += 1
        # saving detailed info on the feedback rating points, the feedback is fetched from API. All the points given
        # by the correteds are added up for more accurate evaluation review
        url = "feedbacks/" + str(feedback_id)
        response = ic.get(url)
        data = response.json()
        feedback_points = 0
        for i in (data['feedback_details']):
            cursor.execute(
                "UPDATE scales SET feedback_" + i['kind'] + " = " + str(i['rate']) + " WHERE id = " + str(scale_id))
            feedback_points += i['rate']
        executable = "UPDATE scales SET feedback_points = " + str(feedback_points) + " WHERE id = " + str(scale_id)
        cursor.execute(executable)
        cursor.execute('UPDATE scales SET feedback_comment = (?) WHERE id = ' + str(scale_id), (data['comment'],))
        self.database.commit()
        return

    #########################
    #   POINT CALCULATION   #
    #########################

    # point calculation for evals. Get the list of evals from the database, and iterates through it. Every
    # evaluation is send to calculate_eval_points so that the points for that evaluation can be calculated.
    def save_eval_points(self):
        cursor = self.database.cursor()
        evals = cursor.execute("SELECT * FROM scales")
        for i in evals:
            self.calculate_eval_points(i['id'], i, i['feedback_points'])
        time = datetime.now().strftime(time_format_sql)
        cursor.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"eval_points\"", (time,))
        self.database.commit()

    # Calculates the eval points of a single evaluation.
    def calculate_eval_points(self, scale_id, team, feedback_points):
        cursor = self.database.cursor()
        final_mark_points = self.get_final_mark_points(team)
        cursor.execute("UPDATE scales SET final_mark_points =" + str(final_mark_points) + " WHERE id = (?)",
                       (scale_id,))
        comment_points = self.get_comment_points(team)
        cursor.execute("UPDATE scales SET comment_points = "+str(comment_points)+" WHERE id = (?)", (scale_id,))
        duration_points = self.get_duration_points(team, final_mark_points)
        cursor.execute("UPDATE scales SET duration_points =" + str(duration_points) + " WHERE id = (?)", (scale_id,))
        flags_points = 0
        feedback_total_points = self.get_feedback_total_points(feedback_points)
        cursor.execute("UPDATE scales SET feedback_total_points =" + str(feedback_total_points) + " WHERE id = (?)",
                       (scale_id,))
        total_points = comment_points + final_mark_points + duration_points + flags_points + feedback_total_points
        cursor.execute("UPDATE scales SET total_points =" + str(total_points) + " WHERE id = (?)", (scale_id,))
        self.database.commit()

    # Calculates the comment points. The length of the comment defines the amount of points given.
    def get_comment_points(self, team):
        comment_len = len(team[5])
        comment_points = 0
        if (comment_len > 180):
            comment_points = 5
        elif (comment_len > 360):
            comment_points = 10
        return comment_points

    # Calculates the final mark points. If the grade the student gave is smaller than avarage points
    # for that project team evaluation, or if the student has found a bug that has caused the evaluation
    # to fail with 0 points, student is rewarded with points. 
    def get_final_mark_points(self, team):
        final_marks = self.database.execute(
            "SELECT final_mark FROM scales WHERE team_id =" + str(team['team_id'])).fetchall()
        total = len(final_marks)
        final_mark_sum = 0
        for i in final_marks:
            final_mark_sum += i['final_mark']
        average = final_mark_sum / total
        if team['final_mark'] < average:
            final_mark_points = 5
        elif team['final_mark'] == 0:
            final_mark_points = 5
        else:
            final_mark_points = 0
        return final_mark_points

    # Calculates duration points. If duration is less than 66% of the estimated evaluation length given in the scale
    # information, and the evaluation did not end with a failing grade of 0 points (showing that the evaluation in fact
    # ended because a severe bug was found), -42 points are returned. If the time is less than the estimated time, -10
    # points is returned. If the student has spent more than 1,5 times the estimated time evaluating the project, 20 
    # points are returned. In other cases, 10 points are returned.
    def get_duration_points(self, team, final_mark_points):
        start_time = datetime.strptime(team[9], time_format_sql)
        end_time = datetime.strptime(team[15], time_format_sql)
        target_time = team[16]
        minimum_time = target_time * 0.66
        duration = (end_time - start_time).total_seconds()
        duration_points = 0
        if duration < minimum_time and final_mark_points <= 0:
            duration_points = -42
        elif duration < target_time and final_mark_points <= 0:
            duration_points = -10
        elif duration > target_time * 1.5:
            duration_points = 20
        else:
            duration_points = 10
        return duration_points

    # returns the feedback points, that are twice the amount of points the corrected has given for the evaluation.
    def get_feedback_total_points(self, feedback_points):
        return feedback_points * 2

    # Basic function for calculating too-friendly points. Fetches logins from the student database, and iterates
    # through the list to calculate the too friendly points. The too friendly points are calculated after other
    # evaluation points, because they take into account all the given evaluations in the database.
    def save_friendly_points(self):
        cursor = self.database.cursor()
        students = cursor.execute("SELECT login FROM students").fetchall()
        for i in students:
            self.get_too_friendly_points(i['login'])
        time = datetime.now().strftime(time_format_sql)
        cursor.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"too_friendly\"", (time,))
        self.database.commit()

    # too friendly points calculation of a single student. Creates a dictionary with all the names of the people the
    # student has evaluated with the amount of times they have evaluated them. Come to think of it, the comparison
    # should probably be done the other way around also, so that it is checked how many times each corrected has
    # corrected the corrector. That might be the record of using correct* in a sentence. Only checks the first
    # corrected now.
    def get_too_friendly_points(self, login):
        cursor = self.database.cursor()
        # check that the person has evals
        corrected_list = cursor.execute('SELECT id, corrected1 FROM scales WHERE corrector ="' + login + '"').fetchall()
        if len(corrected_list) == 0:
            return
        # create the dictionary with logins and amounts they have been evaluated.
        corrected_dict = {}
        for i in corrected_list:
            if not i['corrected1'] in corrected_dict:
                corrected_dict[i['corrected1']] = 0
                amount = 0
                for w in corrected_list:
                    if w['corrected1'] == i['corrected1']:
                        amount += 1
                corrected_dict[i['corrected1']] += amount
        corrected_amount = len(corrected_dict)
        # go through the list again and save the too friendly points of an evaluation. Also saves too_friendly points
        # to the student database in case there is only a few who the person has evaluated.
        for i in corrected_list:
            eval_too_friendly_points = 0
            if (corrected_dict[i['corrected1']]) > 2:
                eval_too_friendly_points = -10
            cursor.execute(
                "UPDATE scales SET too_friendly_points =" + str(eval_too_friendly_points) + " WHERE id = (?)",
                (i['id'],))
            cursor.execute(
                "UPDATE scales SET total_points = total_points + " + str(eval_too_friendly_points) + " WHERE id = (?)",
                (i['id'],))
        if corrected_amount < 10:
            cursor.execute("UPDATE students SET too_friendly_points =" + str(-10) + " WHERE login = (?)", (login,))
        self.database.commit()

    # Basic function for student points creation. Fetches a list of student logins from the database, iterates the list
    # and calls get_student_points for each student.
    def save_student_points(self):
        cursor = self.database.cursor()
        students = cursor.execute("SELECT login FROM students").fetchall()
        for i in students:
            self.get_student_points(i['login'])
        time = datetime.now().strftime(time_format_sql)
        cursor.execute("UPDATE tables SET status = 1, created = (?) WHERE name = \"student_points\"", (time,))
        self.database.commit()

    # Student point saving
    def get_student_points(self, login):
        cursor = self.database.cursor()
        # check that the person has evals
        corrected_list = cursor.execute('SELECT total_points FROM scales WHERE corrector ="' + login + '"').fetchall()
        if len(corrected_list) == 0:
            return
        amount = 0
        # students too friendly points calculated earlier are the base for the total points.
        student_friendly_points = cursor.execute(
            'SELECT too_friendly_points FROM students WHERE login = "' + login + '"').fetchone()
        total = student_friendly_points['too_friendly_points']
        for i in corrected_list:
            total += i['total_points']
            amount += 1
        average = total / amount
        average = "{:.1f}".format(average)
        cursor.execute('UPDATE students SET evals =' + str(amount) + ', avarage_points = ' + str(
            average) + ', total_points = ' + str(total) + ' WHERE login = ?', (login,))
        self.database.commit()

    #####################
    #   .CSV CREATION   #
    #####################

    # Creates a .csv file from evaluations in the given time frame. If the time frame is not given,
    # saves the whole database. The file static/output.csv is reused for this purpose.
    def get_csv(self, start_date, end_date):
        cursor = self.database.cursor()
        if start_date and end_date:
            start_time = datetime.strptime(start_date, '%Y-%m-%d')
            start_time = start_time.replace(hour=00, minute=00, second=00)
            end_time = datetime.strptime(end_date, '%Y-%m-%d')
            end_time = end_time.replace(hour=23, minute=59, second=59)
            start_str = start_time.strftime(time_format_sql)
            end_str = end_time.strftime(time_format_sql)
            data = cursor.execute('SELECT corrector, total_points, id, scale_id, project_id, comment, comment_points, '
                                  'final_mark, final_mark_points, begin_at, corrected1, corrected2, corrected3, '
                                  'corrected4, too_friendly_points, filled_at, duration, duration_points, true_flags, '
                                  'flags_points, feedback_comment, feedback_rating, feedback_id, feedback_points, '
                                  'feedback_interested, feedback_nice, feedback_punctuality, feedback_rigorous, '
                                  'feedback_total_points, team_id FROM scales WHERE begin_at BETWEEN "' + start_str +
                                  '" AND "' + end_str + '"')
        else:
            data = cursor.execute('SELECT corrector, total_points, id, scale_id, project_id, comment, comment_points, '
                                  'final_mark, final_mark_points, begin_at, corrected1, corrected2, corrected3, '
                                  'corrected4, too_friendly_points, filled_at, duration, duration_points, true_flags, '
                                  'flags_points, feedback_comment, feedback_rating, feedback_id, feedback_points, '
                                  'feedback_interested, feedback_nice, feedback_punctuality, feedback_rigorous, '
                                  'feedback_total_points, team_id FROM scales')
        if os.path.exists('static/output.csv'):
            os.remove('static/output.csv')
        file = open('static/output.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(['corrector', 'total_points', 'eval_id', 'scale_id', 'project_id', 'comment', 'comment_points',
                         'final_mark', 'final_mark_points', 'begin_at', 'corrected1', 'corrected2', 'corrected3',
                         'corrected4', 'too_friendly_points', 'filled_at', 'duration', 'duration_points', 'true_flags',
                         'flags_points', 'feedback_comment', 'feedback_rating', 'feedback_id', 'feedback_points',
                         'feedback_interested', 'feedback_nice', 'feedback_punctuality', 'feedback_rigorous',
                         'feedback_total_points', 'team_id'])
        writer.writerows(data)
