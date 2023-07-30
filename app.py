from flask import Flask, request, render_template, send_file
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

app = Flask(__name__)

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def execute_notebook(notebook_filename, csv_filename):
    # Convert the notebook content to a notebook object
    notebook = nbformat.read(notebook_filename, as_version=4)

    # Initialize the ExecutePreprocessor
    executor = ExecutePreprocessor(timeout=-1, kernel_name="python3")

    # Execute the notebook
    executor.preprocess(notebook, {"metadata": {"path": "./"}})

   

import pandas as pd

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and "csvFile" in request.files:
        # Traiter le fichier CSV uploadé
        csv_file = request.files["csvFile"]

        # Save the CSV file in the current directory
        csv_filename = "data.csv"
        csv_file.save(csv_filename)

        # Exécuter le notebook pour le traitement
        notebook_filename = "main.ipynb"
        execute_notebook(notebook_filename, csv_filename)
        
        # Retourner le fichier Excel en téléchargement
        link = "suivi_9_sites.xlsx"
        return send_file(link, as_attachment=True)  # Send the file as an attachment

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)

