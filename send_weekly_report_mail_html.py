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
        message_body = f'<html><body><h1 style="color: black;">As estatísticas do relatório da semana de {stats[4].date()} são:</h1>'
        message_body += '<table style="border-collapse: collapse; width: 100%;">'
        message_body += '<thead style="background-color: #343a40; color: white;"><tr>'
        message_body += f'<th style="border: 1px solid black; padding: 5px;">Coluna</th>'
        message_body += f'<th style="border: 1px solid black; padding: 5px;">Valor</th>'
        message_body += '</tr></thead><tbody>'

        for i in range(len(stats)):
            if i == 4 or i == 5:
                stats[i] = stats[i].strftime('%Y-%m-%d %H:%M:%S')
                stats[i] = stats[i].replace("-", "/")

            
            if stats[i] == "finished":
                cell_style = 'background-color: green; color: white;'
            else:
                cell_style = ''

            message_body += '<tr>'
            message_body += f'<td style="border: 1px solid black; padding: 5px; color: black;"><strong>{columns[i].replace("_", " ").title()}</strong></td>'
            message_body += f'<td style="border: 1px solid black; padding: 5px; color: black; {cell_style}">{stats[i]}</td>'
            message_body += '</tr>'

        message_body += '</tbody></table>'

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        message_body += f"<p>E-mail enviado em {(dt.datetime.now() - dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')} de {ip_address}.</p>"
        message_body += '</body></html>'

        message = f"Subject: {subject}\n"
        message += "MIME-Version: 1.0\n"
        message += "Content-Type: text/html\n\n"
        message += message_body

        server.sendmail(SENDER_EMAIL, mailing_list, message.encode("utf-8"))


def main():
    db = Database()

    mailing_list = db.fetch_mailing_list()
    stats, columns = db.fetch_last_job_stats()
    db.close_conn()

    send_weekly_report_email(stats, columns, mailing_list)


if __name__ == '__main__':
    main()
