from flask import Flask, render_template, request, jsonify
import os, json

app = Flask(__name__)

# Path to JSON files
JSON_FOLDER = '/data/data/com.termux/files/home/storage/downloads/quizhub/json_files'

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Search functionality
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify([])  # Return empty list if query is empty

    try:
        files = os.listdir(JSON_FOLDER)
    except FileNotFoundError:
        return jsonify({"error": "JSON folder not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    results = [
        f for f in files if query.replace(' ', '_') in f.lower()
    ]
    return jsonify(results[:10])  # Return top 10 results

# Fetch and display quiz
@app.route('/quiz/<filename>')
def quiz(filename):
    try:
        filepath = os.path.join(JSON_FOLDER, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
        return render_template('quiztemplate.html', quiz=data)
    except FileNotFoundError:
        return "File not found", 404
    except json.JSONDecodeError:
        return "Error decoding JSON file", 500
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
