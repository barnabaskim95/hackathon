#!/usr/bin/env python3

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

#site = "hackathon.wopr.cc"
#script_name = "3rdparty.js"

#body = """
#A change to JavaScript ({}) has been detected on {}.
#
#Please compare the attached 'old' and 'new' versions to 
#determine whether this is an innocent or malicious change.
#""".format(script_name, site)

def send_mail(send_from, send_to, subject, text, new_script, old_script=None, server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    
    with open(new_script, "rb") as fil:
       part = MIMEApplication( fil.read(),Name=basename(new_script))
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(new_script)+".txt")
    msg.attach(part)
    
    if old_script:
       with open(old_script, "rb") as fil:
          part = MIMEApplication( fil.read(),Name=basename(old_script))
       part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(old_script)+".txt")
       msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


# 'THISIS...' would be replaced with the actual variable containing the script text.
#send_mail('cartwire@wopr.cc', ['hackathon@swynwyr.com'], 'Cartwire Alert for {}'.format(site), 
#        body, 'THISISNEWSCRIPT', 'THISISOLDSCRIPT')
