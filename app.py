from flask import Flask, request, render_template, jsonify
import pandas as pd
from collections import Counter
import os

app = Flask(__name__)

# Function to calculate percentage agreement
def calculate_percentage_agreement(column):
    counts = Counter(column.dropna())  # Count occurrences, ignoring NaNs
    if counts:
        most_common_count = max(counts.values())  # Frequency of most common score
        total = sum(counts.values())  # Total number of gradings
        return round((most_common_count / total) * 100, 2)  # Return as percentage
    return 0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    # Read Excel file
    import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    # Read Excel file
    df = pd.read_excel(file_path)

    logging.info("\n🔍 EXCEL FILE PREVIEW:")
    logging.info(df.head())  # Log first few rows

    # Ignore columns B to F, use columns G to W
    df_grades = df.iloc[:, 6:23]  # Selecting columns G to W

    logging.info("\n✅ FILTERED DATA PREVIEW (Columns G to W):")
    logging.info(df_grades.head())  # Log first few rows of the selected data

    # Define the four groups of columns
    groups = {
        "Group 1 (H-K)": df_grades.iloc[:, 1:5],  # H, I, J, K
        "Group 2 (L-O)": df_grades.iloc[:, 5:9],  # L, M, N, O
        "Group 3 (P-S)": df_grades.iloc[:, 9:13],  # P, Q, R, S
        "Group 4 (T-W)": df_grades.iloc[:, 13:17]  # T, U, V, W
    }

    # Calculate agreement factors
    agreement_results = {group: data.apply(calculate_percentage_agreement) for group, data in groups.items()}

    # Convert results to JSON
    results_json = pd.DataFrame(agreement_results).to_json(orient="records")

    return jsonify({"status": "success", "data": results_json})

    # Ignore columns B to F, use columns G to W
    df_grades = df.iloc[:, 6:23]  # Selecting columns G to W

    # Define the four groups of columns
    groups = {
        "Group 1 (H-K)": df_grades.iloc[:, 1:5],  # H, I, J, K
        "Group 2 (L-O)": df_grades.iloc[:, 5:9],  # L, M, N, O
        "Group 3 (P-S)": df_grades.iloc[:, 9:13],  # P, Q, R, S
        "Group 4 (T-W)": df_grades.iloc[:, 13:17]  # T, U, V, W
    }

    # Calculate agreement factors
    agreement_results = {group: data.apply(calculate_percentage_agreement) for group, data in groups.items()}

    # Convert results to JSON
    results_json = pd.DataFrame(agreement_results).to_json(orient="records")

    return jsonify({"status": "success", "data": results_json})

if __name__ == "__main__":
    app.run(debug=True)
