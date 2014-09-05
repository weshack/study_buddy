from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello world"

# Make a search for a class, and return a json object.
@app.route("/search/<keyword>")
def search(keyword):
	return "search page: " + keyword

if __name__ == "__main__":
  app.run()
