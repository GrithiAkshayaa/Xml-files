import socket
import _confd
import _confd.dp as dp
import _confd.err as confd_err

# Callback function to retrieve alarm data
def get_alarms(tctx, kp):
    try:
        print("Fetching alarms container...")

        # Example response structure
        alarms_data = [
            {"id": "1", "severity": "Critical", "message": "High link power"},
            {"id": "2", "severity": "Warning", "message": "High CPU usage"}
        ]

        # Start a new transaction reply
        dp.data_reply_value(tctx, alarms_data)
        return _confd.CONFD_OK

    except Exception as e:
        print(f"Error retrieving alarms: {e}")
        return _confd.CONFD_ERR

# Register the data provider
def register_data_provider():
    try:
        # Get ConfD port (ensure this attribute exists)
        confd_port = getattr(_confd, 'CONF_PORT', 4565)  # Default to 4565 if not found

        # Connect to ConfD
        addr = socket.getaddrinfo("127.0.0.1", confd_port, socket.AF_INET, socket.SOCK_STREAM)[0][4]
        ctlsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ctlsock.connect(addr)

        print("Connected to ConfD successfully on port", confd_port)

        # Register the data provider (Modify if needed)
        dp.init_daemon("alarms_provider")
        dp.register_data_cb("alarms_container", get_alarms)

        print("Data provider registered successfully")

    except Exception as e:
        print(f"Failed to register data provider: {e}")

# Run the registration
if __name__ == "__main__":
    register_data_provider()
