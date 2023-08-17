from flask import Flask, render_template, request, redirect, send_file
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.backends.backend_pdf
from werkzeug.serving import run_simple

app = Flask(__name__)

# Ruta de la página de inicio
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica si se ha subido un archivo
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # Verifica si el archivo tiene un nombre
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Obtiene el nombre del archivo sin la extensión
            filename_without_extension = os.path.splitext(file.filename)[0]
            
            # Lee el archivo DAT y crea un DataFrame
            df = pd.read_csv(file, delimiter='\t')
            
            # Genera una gráfica de ejemplo (puedes modificar esto)
            plt.figure(figsize=(8, 6))
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o')
            plt.xlabel(df.columns[0])
            plt.ylabel(df.columns[1])
            
            # Guarda la gráfica en un archivo PDF
            pdf_output = BytesIO()
            pdf = matplotlib.backends.backend_pdf.PdfPages(pdf_output)
            pdf.savefig()
            plt.close()
            pdf.close()
            
            pdf_output.seek(0)
            
            # Envía el archivo PDF como respuesta para descargar
            response = send_file(pdf_output, mimetype='application/pdf')
            response.headers['Content-Disposition'] = f'attachment; filename={filename_without_extension}.pdf'
            return response
    
    return render_template('index.html')

if __name__ == '__main__':
    run_simple('localhost', 5000, app)
