from flask import Flask, request, jsonify, render_template
import redis
import threading

app = Flask(__name__)

# Redis Cloud connection
redis_client = redis.StrictRedis(
    host="redis-17479.c84.us-east-1-2.ec2.redns.redis-cloud.com",   # e.g. redis-12345.c123.us-east-1-3.ec2.cloud.redislabs.com
    port=17479,           # e.g. 12345
    password="X5b97hVmeTvNGerdwJY65xUVitPjCNjN", # from Redis Cloud
    decode_responses=True
)

# Background subscriber to listen for messages
def subscribe_to_channel():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("my_channel")
    for message in pubsub.listen():
        if message['type'] == 'message':
            redis_client.rpush("messages_list", message['data'])  # save to list
            print(f"📩 Received: {message['data']}")

threading.Thread(target=subscribe_to_channel, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/publish", methods=["POST"])
def publish_message():
    data = request.json
    message = data.get("message", "Hello Redis")
    redis_client.publish("my_channel", message)
    return jsonify({"status": "Message published", "message": message})

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = redis_client.lrange("messages_list", 0,-1)
    return jsonify(messages)

@app.route("/clear", methods=["POST"])
def clear_messages():
    redis_client.delete("messages_list")
    return jsonify({"status": "Messages cleared"})

if __name__ == "__main__":
    app.run(debug=True)
