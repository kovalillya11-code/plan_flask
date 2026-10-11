from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "library-secret-key"

BOOKS = [
    {
        "id": 1,
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "year": 1840,
        "borrower": "Олена",
        "available": False,
    },
    {
        "id": 2,
        "title": "Тигр і лебідь",
        "author": "Сергій Бондарчук",
        "year": 2021,
        "borrower": "",
        "available": True,
    },
]


def get_next_id():
    if not BOOKS:
        return 1
    return max(book["id"] for book in BOOKS) + 1


def find_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/library")
def library():
    return render_template("library.html", books=BOOKS)


@app.route("/library/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    year = request.form.get("year", "").strip()
    borrower = request.form.get("borrower", "").strip()

    if title and author:
        BOOKS.append(
            {
                "id": get_next_id(),
                "title": title,
                "author": author,
                "year": int(year) if year.isdigit() else 0,
                "borrower": borrower,
                "available": not borrower,
            }
        )

    return redirect(url_for("library"))


@app.route("/library/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = find_book(book_id)
    if book is None:
        return redirect(url_for("library"))

    if request.method == "POST":
        book["title"] = request.form.get("title", book["title"]).strip() or book["title"]
        book["author"] = request.form.get("author", book["author"]).strip() or book["author"]
        year = request.form.get("year", str(book["year"])).strip()
        book["year"] = int(year) if year.isdigit() else book["year"]
        borrower = request.form.get("borrower", "").strip()
        book["borrower"] = borrower
        book["available"] = not borrower
        return redirect(url_for("library"))

    return render_template("edit_book.html", book=book)


@app.route("/library/<int:book_id>/lend", methods=["POST"])
def lend_book(book_id):
    book = find_book(book_id)
    if book is not None:
        borrower = request.form.get("borrower", "").strip()
        if borrower:
            book["borrower"] = borrower
            book["available"] = False
        else:
            book["borrower"] = ""
            book["available"] = True
    return redirect(url_for("library"))


@app.route("/library/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    for index, book in enumerate(BOOKS):
        if book["id"] == book_id:
            BOOKS.pop(index)
            break
    return redirect(url_for("library"))


if __name__ == "__main__":
    app.run(debug=True)
