#!/usr/bin/env python3

import smtplib
import ssl
import psycopg2 as pg
import datetime as dt
import socket
from password import pg_pw, email_pw
from query import Database

SENDER_EMAIL = 'floriparentwatch@gmail.com'

def send_weekly_report_email(stats, columns, mailing_list):
    PORT = 465  # This is the default SSL port
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(SENDER_EMAIL, email_pw())

        subject = "Relatório Semanal Floripa Rent Watch!"
        message_body = f'As estatísticas do relatório da semana de {stats[4].date()} são:\n\n'

        max_len = len(max(columns, key=len))

        for i in range(len(stats)):
            if i == 4 or i == 5:
                stats[i] = stats[i].strftime('%Y-%m-%d %H:%M:%S')
                message_body += f"\t{columns[i]}{(max_len - len(columns[i]) + 1) * ' '}: {stats[i]}\n"
            else:
                message_body += f"\t{columns[i]}{(max_len - len(columns[i]) + 1) * ' '}: {stats[i]}\n"

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        message_body += f"\nE-mail enviado em {(dt.datetime.now() - dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')} de {ip_address}."

        message = f"Subject: {subject}\n\n{message_body}"

        server.sendmail(SENDER_EMAIL, mailing_list, message.encode("utf-8"))

def main():
    db = Database()

    mailing_list = db.fetch_mailing_list()
    stats, columns = db.fetch_last_job_stats()
    db.close_conn()

    send_weekly_report_email(stats, columns, mailing_list)

if __name__ == '__main__':
    main()
