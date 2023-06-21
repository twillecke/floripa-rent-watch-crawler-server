from weasyprint import HTML

# Path to the HTML file to convert
html_file = 'html_report_jinja.html'

# Path to save the PDF file
pdf_file = 'output.pdf'

# Convert HTML to PDF
HTML(html_file).write_pdf(pdf_file)
