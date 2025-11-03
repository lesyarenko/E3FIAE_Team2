# Test
from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="../app/templates",
    static_folder="../app/static",
)
@app.route("/")
def home():
    return render_template("index.html", title="YourChatbot")

if __name__ == "__main__":
    app.run(debug=True, port=5050)
