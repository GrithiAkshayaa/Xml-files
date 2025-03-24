import socket
import json

# Mock state data
def get_state():
    return {
        "component1": {"oper-status": "ACTIVE", "temperature": 45.3},
        "component2": {"oper-status": "DOWN", "temperature": 30.5}
    }

# Handle incoming requests from ConfD
def handle_request(request):
    state_data = get_state()
    if request in state_data:
        return json.dumps(state_data[request])  # Convert dictionary to JSON
    return json.dumps({})  # Return empty if not found

# Create a socket to communicate with ConfD
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 4565))  # ConfD IPC port
server_socket.listen(5)

print("State provider running...")

while True:
    conn, addr = server_socket.accept()
    request = conn.recv(1024).decode()
    response = handle_request(request)
    conn.send(response.encode())
    conn.close()
