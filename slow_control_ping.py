#!/usr/bin/env python

from ping import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import time
from time import localtime, strftime

toaddr = ''     #put email address to send to here
fromuser = 'minicleanassembly'
server = 'gmail.com'
status = True
email = False
nfail = 0
email_time = []
max_per_day = 10
timeout = 10
sleeptime = 1

def send_email(estr):
    msg = MIMEMultipart()
    msg['From'] = fromuser + '@' + server
    msg['To'] = toaddr
    msg['Subject'] = 'Slow Controls'
    msg.attach(MIMEText(estr, 'plain'))
    server = smtplib.SMTP('smtp.' + server, 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromsuer, '92r591202mod')
    server.sendmail(fromuser+'@'+server, toaddr, msg.as_string())

if __name__ == '__main__':

    while True:
        print nfail
        try:
            delay = verbose_ping('link.deapclean.org', timeout, 1)
            if delay == None:
                state = False
                nfail += 1
                print 'timeout'
            else:
                state = True
                nfail = 0
                print 'slow controls up'
        except socket.gaierror:
            state = False
            nfail += 1
            print 'error'
        if status:
            email = False
        else:
            if not email and nfail >= 10:
                email = True
                email_time.append(time.clock())
                estr = 'testing slow controls email'
                estr += strftime('%a, %d %b %Y %H:%M:%S', localtime())
                if len(email_time) < max_per_day:
                    send_email(estr)
                elif email_time[-1] - email_time[-max_per_day] > 24*3600:
                    send_email(estr)
                print estr
        if len(email_time) > 100000:
            email_time = []
        time.sleep(sleeptime)
