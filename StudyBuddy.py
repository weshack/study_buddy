from flask import Flask

app = Flask(__name__, static_url_path='')

@app.route("/")
def root():
  return app.send_static_file('html/index.html')

# Make a search for a class, and return a json object.
@app.route("/search/<keyword>")
def search(keyword):
	return "search page: " + keyword

if __name__ == "__main__":
  app.run()
