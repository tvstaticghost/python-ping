import os
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime

targets = ['8.8.8.8', '9.9.9.9']

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


with open('log.txt', 'w') as overwrite:
    overwrite.writelines('')


with open('log.txt', 'a') as f:
    for target in targets:
        command = os.system(f'ping -c 4 {target}')
        if command == 0:
            f.writelines(f'{formatted_datetime} - Connection to {target} successful\n')
        else:
            f.writelines(f'{formatted_datetime} - Connection to {target} FAILED\n')
    f.writelines(f'-----END-----\n')


em = EmailMessage()
em['From'] = 'testalert.nsoc@gmail.com'
em['To'] = 'testalert.nsoc@gmail.com'
em['Subject'] = f'Log {formatted_datetime}'
em.set_content('Test Body')


with open('log.txt', 'rb') as attachment:
    em.add_attachment(attachment.read(), filename='log.txt', maintype='application', subtype='octet-stream')


sender = 'testalert.nsoc@gmail.com'
password = 'eufqxfidmswzkrch'
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender, password)
    smtp.sendmail(sender, 'testalert.nsoc@gmail.com', em.as_string())