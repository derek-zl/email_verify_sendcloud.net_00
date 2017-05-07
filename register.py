from flask import *
from func.process import write_data, send_email, verify_email

app = Flask(__name__)


@app.route("/register", methods=['POST', 'GET'])
def do_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        outcome = write_data(name, email)
        if outcome is False:
            return redirect(url_for('error'))
        send_email(name, email)
        return redirect(url_for('wait_verifyed'))
    return render_template('register.html')


@app.route("/error")
def error():
    msg = "Your E-mail address have already existed! Please return and change your E-mail address."
    return render_template('display.html', msg=msg)


@app.route("/do_verificatin", methods=['GET'])
def do_verification():
    token = request.args.get('token')
    authcode = request.args.get('authcode')
    if token is not None and authcode is not None and verify_email(token, authcode):
        return redirect(url_for('success'))
    else:
        return redirect(url_for('fail'))


@app.route("/success")
def success():
    msg = "success"
    return render_template('display.html', msg=msg)


@app.route("/fail")
def fail():
    msg = "Too late!Time out!"
    return render_template('display.html', msg=msg)


@app.route("/wait_verifyed")
def wait_verifyed():
    msg = "Our verification link has sent to your email, please check your E-mail !"
    return render_template('display.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
