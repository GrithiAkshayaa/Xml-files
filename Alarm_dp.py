import socket
import _confd
import _confd.dp as dp
import _confd.error as confd_err

# Debugging prints
print("Using _confd module from:", _confd.__file__)
print("Available attributes in _confd:", dir(_confd))
print("CONF_PORT value:", getattr(_confd, "CONF_PORT", "Not Found"))

# Callback function to retrieve alarm data
def get_alarms(tctx, kp):
    try:
        print("Fetching alarms container...")

        # Example response structure
        alarms_data = [
            {"id": 1, "severity": "critical", "message": "Link Down"},
            {"id": 2, "severity": "warning", "message": "High CPU Usage"},
        ]

        # Start a new transaction reply
        dp.data_reply_value(tctx, alarms_data)
        return confd_err.CONFD_OK

    except Exception as e:
        print(f"Error retrieving alarms: {e}")
        return confd_err.CONFD_ERR

# Register the data provider
def register_data_provider():
    try:
        # Get ConfD port
        confd_port = _confd.CONF_PORT

        # Connect to ConfD
        addr = socket.getaddrinfo("127.0.0.1", confd_port, socket.AF_INET, socket.SOCK_STREAM)[0][4]
        ctlsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ctlsock.connect(addr)

        # Initialize data provider context
        dctx = dp.init_daemon("alarm_daemon")
        dp.connect(dctx, ctlsock, dp.CONTROL_SOCKET, "")
        dp.register_data_cb(dctx, {
            "get_elem": get_alarms
        })

        print("Data provider registered successfully.")

    except Exception as e:
        print(f"Failed to register data provider: {e}")

# Run the provider
if __name__ == "__main__":
    register_data_provider()
