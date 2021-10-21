from flask import Flask
from queue import Queue


app = Flask(__name__)

@app.route("/")
def hello_world():
    print(queue_list)
    # return f"{str(queue_list)}"
    
    return "<p>Hello, World!</p>"

def back_server(q_list, host="0.0.0.0", port=12345):
    global queue_list
    queue_list = q_list

    app.run(host=host, port=port)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345)
