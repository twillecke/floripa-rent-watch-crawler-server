from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

template = env.get_template('report_template.html')

html = template.render(title='Média Mensal,',
                       subtitle='Categoria Por Bairro',
                       date='06/2023',
                       chart='./chart/perfomance-chart.png')

with open('html_report_jinja.html', 'w', encoding="utf-8") as f:
    f.write(html)
