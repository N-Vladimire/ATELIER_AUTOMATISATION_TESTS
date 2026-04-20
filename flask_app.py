from flask import Flask, jsonify, render_template

from storage import init_db, save_run, list_runs, get_last_run
from tester.runner import run_all_tests

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    return """
    <h1>API Monitoring - Atelier</h1>
    <ul>
        <li><a href="/run">/run</a></li>
        <li><a href="/dashboard">/dashboard</a></li>
        <li><a href="/health">/health</a></li>
    </ul>
    """


@app.route("/run")
def run():
    run_data = run_all_tests()
    save_run(run_data)
    return jsonify(run_data)


@app.route("/dashboard")
def dashboard():
    runs = list_runs(limit=20)
    last_run = get_last_run()
    return render_template("dashboard.html", runs=runs, last_run=last_run)


@app.route("/health")
def health():
    last_run = get_last_run()

    if not last_run:
        return jsonify({
            "status": "UNKNOWN",
            "message": "Aucun run disponible"
        }), 200

    return jsonify({
        "status": last_run["availability"],
        "last_timestamp": last_run["timestamp"],
        "api": last_run["api"]
    }), 200


if __name__ == "__main__":
    app.run(debug=True)