import smtplib, ssl
import psycopg2 as pg
import datetime as dt
import socket

conn = pg.connect(
    host = 'localhost',
    database = 'rent_watch',
    port = 5432,
    user ='postgres',
    password = '123'
    )

cur = conn.cursor()

sql_stats = "SELECT * FROM job_stats ORDER BY 1 DESC LIMIT 1;"
sql_columns = """
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'job_stats';
"""

cur.execute(sql_stats)
stats = cur.fetchone()

stats = [stat for stat in stats]

cur.execute(sql_columns)
columns = cur.fetchall()

columns = [elem[0] for elem in columns]

cur.close()
conn.close()

PORT = 465  # This is the default SSL port
PASSWORD = "kcxoktznxpghterw"

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
    server.login("floriparentwatch@gmail.com", PASSWORD)

    subject = "Relatório Semanal Floripa Rent Watch!"
    message_body = f'As estatísticas do relátorio da semana de {stats[4].date()} são:\n\n' 

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

    sender_address = "floriparentwatch@gmail.com"
    receiver_address = ["floriparentwatch@gmail.com", "gbarbosa1407@gmail.com", "thiagogwillecke@gmail.com"]
    
    print(message)
#    server.sendmail(sender_address, receiver_address, message.encode("utf-8"))
