from flask import Flask, render_template, request
import os
import datetime
from email.message import EmailMessage
import ssl
import smtplib


app = Flask(__name__)


email_sender = 'service.projectest2024@gmail.com'
email_password = 'zicu jqaw dopn hyes'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form
        filename = generate_filename(form_data)
        file_path = os.path.join("forms", filename)
        with open(file_path, 'w') as file:
            for key, value in form_data.items():
                file.write(f'{key}: {value}\n')
        return 'Form submitted successfully!'
    return render_template('index.html')    


@app.route('/send_email', methods=['GET','POST'])
def send_email():
    if request.method == 'POST':
        client_email = request.form.get('client_email')
        ip_address = request.form.get('ip_address')
        access_point = request.form.get('Access_Point')
        access_point_pwd = request.form.get('Access_point_pwd')
        port = request.form.get('port')
        service = request.form.get('service')


        if client_email and ip_address and access_point and access_point_pwd and port :
            send_email_notification(client_email, ip_address, access_point , access_point_pwd , port , service)
            return 'Email sent successfully!'
        else:
            return 'Missing required parameters in the request.', 400
    else : 
        return render_template('send_email.html')

def generate_filename(form_data):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    username = form_data.get('name')
    return f'{timestamp}_{username}_submission.txt'


def send_email_notification(client_email, ip_address, access_point , access_point_pwd , port , service):
    try :
        email_receiver = client_email
        subject = "CONTAINER's Creation response"
        body = f'Service : {service}\nIP Address: {ip_address}\nPort: {port}\nAccess Point: {access_point}\nAccess Point Password: {access_point_pwd}'
        em = EmailMessage()
        em['FROM'] = email_sender
        em['TO'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com' , 465 , context=context) as smtp :
            smtp.login(email_sender , email_password)
            smtp.sendmail(email_sender , email_receiver , em.as_string())

    except Exception as err :
        print(err)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)