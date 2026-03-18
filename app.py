from flask import Flask, render_template, jsonify, request, Response
import gesture_engine

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/customize")
def customize():
    return render_template("customize.html")

@app.route("/start", methods=["POST"])
def start():
    gesture_engine.start_gesture()
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    gesture_engine.stop_gesture()
    return jsonify({"status": "stopped"})

@app.route("/status")
def status():
    return jsonify({
        "running": gesture_engine.gesture_running,
        "action": gesture_engine.current_action
    })

@app.route("/mapping")
def mapping():
    return jsonify(gesture_engine.get_mapping_with_description())

@app.route("/update-mapping", methods=["POST"])
def update_mapping():
    data = request.json
    gesture_engine.update_mapping(data["gesture"], data["action"])
    return jsonify({"status": "updated"})

@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.json
    reply = gesture_engine.gesture_assistant_reply(data.get("message", ""))
    return jsonify({"reply": reply})

@app.route("/video_feed")
def video_feed():
    return Response(
        gesture_engine.generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    app.run(debug=True)