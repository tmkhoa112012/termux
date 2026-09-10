-import os
import subprocess
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/files", methods=["GET"])
def list_files():
    files = sorted(f for f in os.listdir(UPLOAD_DIR) if f.endswith(".py"))
    return jsonify(files)


@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Khong co file"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Chua chon file"}), 400
    if not file.filename.endswith(".py"):
        return jsonify({"error": "Chi chap nhan file .py"}), 400
    filename = os.path.basename(file.filename)
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)
    return jsonify({"message": f"Da upload {filename}", "filename": filename})


@app.route("/api/delete", methods=["POST"])
def delete_file():
    data = request.get_json(force=True)
    filename = os.path.basename(data.get("filename", ""))
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"message": f"Da xoa {filename}"})
    return jsonify({"error": "Khong tim thay file"}), 404


@app.route("/api/run", methods=["POST"])
def run_file():
    data = request.get_json(force=True)
    filename = os.path.basename(data.get("filename", ""))
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Khong tim thay file"}), 404
    try:
        result = subprocess.run(
            ["python3", filepath],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=UPLOAD_DIR,
        )
        output = result.stdout
        if result.stderr:
            output += ("\n" if output else "") + result.stderr
        if not output:
            output = "(khong co output)"
        return jsonify({"output": output, "returncode": result.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Loi: chay qua 30s, da bi ngat", "returncode": -1})
    except Exception as e:
        return jsonify({"output": f"Loi: {e}", "returncode": -1})


@app.route("/api/pip", methods=["POST"])
def pip_install():
    data = request.get_json(force=True)
    package = (data.get("package") or "").strip()
    if not package:
        return jsonify({"error": "Thieu ten package"}), 400
    try:
        result = subprocess.run(
            ["pip", "install" package],
            capture_output=True,
            text=True,
            timeout=90,
        )
        output = (result.stdout or "") + "\n" + (result.stderr or "")
        return jsonify({"output": output.strip(), "returncode": result.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Loi: pip install qua thoi gian", "returncode": -1})
    except Exception as e:
        return jsonify({"output": f"Loi: {e}", "returncode": -1})


@app.route("/api/exec", methods=["POST"])
def run_command():
    """Chay 1 lenh shell bat ky (giong Termux), gioi han thoi gian."""
    data = request.get_json(force=True)
    cmd = (data.get("cmd") or "").strip()
    if not cmd:
        return jsonify({"error": "Thieu lenh"}), 400
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=UPLOAD_DIR,
        )
        output = (result.stdout or "") + (result.stderr or "")
        if not output:
            output = "(khong co output)"
        return jsonify({"output": output, "returncode": result.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Loi: lenh chay qua 30s", "returncode": -1})
    except Exception as e:
        return jsonify({"output": f"Loi: {e}", "returncode": -1})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
