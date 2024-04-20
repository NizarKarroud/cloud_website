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
        container_info = request.form.get('container_info')

        if client_email and ip_address and container_info:
            send_email_notification(client_email, ip_address, container_info)
            return 'Email sent successfully!'
        else:
            return 'Missing required parameters in the request.', 400
    else : 
        return render_template('send_email.html')

def generate_filename(form_data):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    username = form_data.get('name')
    return f'{timestamp}_{username}_submission.txt'


def send_email_notification(client_email, ip_address, container_info):
    try :
        email_receiver = client_email
        subject = "CONTAINER's Creation response"
        body = f'Your allocated IP address: {ip_address}\nContainer Info: {container_info}'
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