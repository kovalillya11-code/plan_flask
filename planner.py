from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

TASKS = [
    {"id": 1, "title": "Здати дз з Python", "date": "2026-10-15", "description": "Я тепер вільна людина", "done": False},
    {"id": 2, "title": "Купити продукти", "date": "2026-10-12", "description": "Молоко, хліб, протеїн, філейка", "done": True},
]


def next_id():
    return max((t["id"] for t in TASKS), default=0) + 1


PAGE = """
<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Планувальник</title>
<style>
  body { font-family: Arial, sans-serif; background: #f4efe6; margin: 0; padding: 20px; color: #2b2b2b; }
  .container { max-width: 700px; margin: 0 auto; }
  h1 { color: #2d4a3e; }
  .card { background: #fff; border-left: 6px solid #a0764a; border-radius: 12px;
          padding: 16px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .card.done { opacity: .6; }
  .card.done .title { text-decoration: line-through; }
  .title { font-size: 1.2em; font-weight: bold; }
  .meta { color: #666; font-size: .9em; margin: 6px 0; }
  form.add { background: #fff; padding: 16px; border-radius: 12px; margin-bottom: 20px;
             box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  input, button { padding: 8px; margin: 4px 0; border-radius: 6px; border: 1px solid #c9b48a; }
  input { width: 100%; box-sizing: border-box; }
  button { background: #d4b06a; cursor: pointer; border: none; padding: 8px 14px; }
  button.del { background: #b84a4a; color: #fff; }
  .row { display: flex; gap: 8px; }
  @media (max-width: 500px) { .row { flex-direction: column; } }
</style>
</head>
<body>
<div class="container">
  <h1>Планувальник</h1>

  <form class="add" method="post" action="{{ url_for('add_task') }}">
    <input name="title" placeholder="Назва завдання" required>
    <div class="row">
      <input type="date" name="date" required>
      <input name="description" placeholder="Опис">
    </div>
    <button type="submit">Додати</button>
  </form>

  {% for t in tasks %}
  <div class="card {% if t.done %}done{% endif %}">
    <div class="title">{{ t.title }}</div>
    <div class="meta">📅 {{ t.date }} · {{ t.description }}</div>
    <div class="row">
      <form method="post" action="{{ url_for('toggle_task', task_id=t.id) }}">
        <button type="submit">{% if t.done %}Повернути{% else %}Виконано{% endif %}</button>
      </form>
      <form method="post" action="{{ url_for('delete_task', task_id=t.id) }}">
        <button type="submit" class="del">Видалити</button>
      </form>
    </div>
  </div>
  {% else %}
  <p>Завдань немає.</p>
  {% endfor %}
</div>
</body>
</html>
"""


@app.route("/")
def index():
    tasks = sorted(TASKS, key=lambda t: t["date"])
    return render_template_string(PAGE, tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    date = request.form.get("date", "")
    description = request.form.get("description", "").strip()
    if title and date:
        TASKS.append({"id": next_id(), "title": title, "date": date,
                      "description": description, "done": False})
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    for t in TASKS:
        if t["id"] == task_id:
            t["done"] = not t["done"]
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    TASKS[:] = [t for t in TASKS if t["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)