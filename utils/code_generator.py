class CodeGenerator:
    def __init__(self):
        self.templates = {
            "html": """
<!DOCTYPE html>
<html>
<head>
    <title>Generated Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>Hello World</h1>
    </div>
</body>
</html>
""",
            "flask": """
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
"""
        }
    
    def generate(self, prompt):
        # Simple template-based generation
        if "website" in prompt.lower():
            return self.templates["html"]
        elif "flask" in prompt.lower():
            return self.templates["flask"]
        return "# Generated code will appear here\nprint('Hello World')"
