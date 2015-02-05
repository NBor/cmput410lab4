"""Flask project with sqlite3 backend."""
#!/usr/bin/env python
import sqlite3
from flask import Flask, request, redirect#, url_for


app = Flask(__name__)


class DBConnection(object):

    def __init__(self):
        self.conn = None

    def get_conn(self):
        dbfile = 'tasks.db'
        if self.conn is None:
            self.conn = sqlite3.connect(dbfile)
            self.conn.row_factory = sqlite3.Row

    def close_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def query_db(self, query, args=(), one=False):
        cur = self.conn.cursor()
        cur.execute(query, args)
        rec = cur.fetchall()
        cur.close()
        return (rec[0] if rec else None) if one else rec

    def add_task(self, category, priority, description):
        cmd = ('insert into tasks(category, priority, description) '
               'values(?, ?, ?)')
        args = [category, priority, description]
        ret_code = self.query_db(cmd, args, one=True)
        self.conn.commit()
        return ret_code

    def print_tasks(self):
        tasks = self.query_db('select * from tasks')
        for task in tasks:
            print task
        print "%d tasks in total" % len(tasks)

#@app.teardown_appcontext
#def close(connection):
#    DB.conn.close_conn()


@app.route('/')
def welcome():
    """Serve a welcome page."""
    return 'Welcome to Flask!'


@app.route('/task', methods=['GET', 'POST'])
def update_tasks():
    """Serve a page with an database backend."""
    response = """\
<form action="" method=post>
<p>Category: <input type=text name=category></p>
<p>Priority: <input type=text name=priority></p>
<p>Description: <input type=text name=description></p>
<p><input type=submit value=Add></p>
</form>


<table border="1" cellpadding="3">
    <tbody>
        <tr>
            <th>Category</th>
            <th>Priority</th>
            <th>Description</th>
        </tr>
"""

    db_conn = DBConnection()
    db_conn.get_conn()

    #db_conn.query_db('delete from tasks')
    if request.method == 'POST':
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        db_conn.add_task(category, priority, description)
        return redirect('/task')
        #return redirect(url_for('task')) # method name

    for single_task in db_conn.query_db('select * from tasks'):
        if single_task['category'] or single_task['priority'] or single_task['description']:
            response += "<tr><td>%s</td>" % (single_task['category'])
            response += "<td>%s</td>" % (single_task['priority'])
            response += "<td>%s</td></tr>" % (single_task['description'])
    response += "</tbody></table>"

    db_conn.close_conn()
    return response


if __name__ == '__main__':
    app.debug = True
    app.run()
