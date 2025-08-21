from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
DB = "pets.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    species TEXT,
                    age INTEGER,
                    description TEXT,
                    image TEXT)''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM pets")
    pets = c.fetchall()
    conn.close()
    return render_template("index.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        age = request.form["age"]
        description = request.form["description"]
        image = request.form["image"]

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO pets (name, species, age, description, image) VALUES (?, ?, ?, ?, ?)",
                  (name, species, age, description, image))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add_pet.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
