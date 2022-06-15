from app import app

@app.route("/example")
def example():
    return "Example"