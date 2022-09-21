from os import name
from flask import Flask, render_template, url_for, request, make_response, redirect
import sqlite3, random, string

from werkzeug.utils import escape
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/<link>")
def shortredirect(link):
    db = sqlite3.connect('links.db')
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS links (
		link TEXT,
		shortedlink TEXT
	)''')
    db.commit()
    sql.execute('SELECT shortedlink FROM links')
    f = sql.fetchall()
    for i in range(len(f)):
        if (f[i][0] == link):
            sql.execute('SELECT link FROM links')
            s = sql.fetchall()
            return redirect(s[i][0])
    
    return "Link not found"


@app.route('/short', methods=["POST"])
def shortlink():
    db = sqlite3.connect('links.db')
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS links (
		link TEXT,
		shortedlink TEXT
	)''')
    db.commit()

    link = request.form['link']
    if (link != " " or link != ""):
        try:
            c = request.form['iscustom']
        except:
            c = "off"
        print(c)

        if (c == "off"):
            sql.execute('SELECT link FROM links')
            f = sql.fetchall()
            for i in range(len(f)):
                if (f[i][0] == link):
                    sql.execute('SELECT shortedlink FROM links')
                    s = sql.fetchall()
                    return render_template("showlink.html", link=s[i][0])

            sql.execute('SELECT shortedlink FROM links')
            f = sql.fetchall()
            r = random.choice(string.ascii_letters)
            p = 1
            k = 1
            for i in range(len(f)):
                if (f[i][0] == r):
                    while (True):
                        if (p == 104):
                            k+=1
                            p = 0
                        r = ''.join([random.choice(string.ascii_letters) for _ in range(k)])
                        p+=1
                        if (not((r,) in f)):
                            break

            sql.execute('INSERT INTO links VALUES (?, ?)', (link, r))
            db.commit()

            return render_template("showlink.html", link=r)
        else:
            nameoflink = request.form['custom']
            print("ssss", nameoflink, "sssss")
            if (nameoflink != " " or nameoflink != ""):
                sql.execute('SELECT shortedlink FROM links')
                f = sql.fetchall()
                nameoflink = nameoflink.replace(" ", "")
                if ((nameoflink,) in f):
                    return "Short address already used"
                else:
                    sql.execute('INSERT INTO links VALUES (?, ?)', (link, nameoflink))
                    db.commit()
                    return render_template("showlink.html", link=nameoflink)
            else:
                return "Customized link is null"
    else:
        return "Link is null"

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
