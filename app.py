from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# HTML and CSS as a string
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter Header Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        .container {
            width: 50%;
            margin: 50px auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        h1 {
            margin-bottom: 20px;
        }

        input[type="file"] {
            margin-bottom: 20px;
        }

        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        #results {
            margin-top: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }

        th {
            background-color: #f4f4f4;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Extract Chapter Headers from .txt</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" id="fileInput" name="text_file" accept=".txt" required>
            <button type="submit">Upload and Process</button>
        </form>
        {% if headers %}
            <div id="results">
                <table>
                    <thead>
                        <tr>
                            <th>Chapter</th>
                            <th>Title</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for header in headers %}
                            <tr>
                                <td>{{ header.header }}</td>
                                <td>{{ header.title }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def extract_chapter_headers(text):
    headers = []
    pattern = re.compile(r'CHAPTER\s+\w+\s*(?:\n\n|\n\s*)([^\n]+)', re.IGNORECASE)
    matches = pattern.findall(text)
    for match in matches:
        headers.append({'header': match.strip(), 'title': match.strip()})
    return headers

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    headers = []
    if request.method == 'POST':
        text_file = request.files.get('text_file')
        if text_file:
            text = text_file.read().decode('utf-8')
            headers = extract_chapter_headers(text)
    return render_template_string(HTML_CONTENT, headers=headers)

if __name__ == "__main__":
    app.run(debug=True)
