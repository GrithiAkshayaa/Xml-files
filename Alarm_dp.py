import _confd
import _confd.dp as dp
import _confd.maapi as maapi
import socket
import struct
import sys

# Alarm Data
alarms_data = {
    "alarm-001": {
        "id": "alarm-001",
        "resource": "CPU",
        "text": "CPU usage exceeded 90%",
        "time-created": 1711555123,
        "severity": "CRITICAL",
        "type-id": "cpu-overload"
    }
}

# Callback function to provide alarm data
def get_alarm_data(tctx, kp):
    key = str(kp[0][1])  # Extract alarm ID
    if key in alarms_data:
        dp.data_reply_dict(tctx, alarms_data[key])
    else:
        dp.data_reply_error(tctx, _confd.ERR_NOEXISTS)

# Register the data provider
def register_data_provider():
    addr = _confd.addr("127.0.0.1", _confd.CONFD_PORT)
    wsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wsock.connect(addr)

    dctx = dp.init_daemon("alarm_data_provider")
    dp.connect(dctx, wsock, dp.DP_WORKER)
    dp.register_data_cb(dctx, dp.data_cbs(get_elem=get_alarm_data))
    
    dp.register_done(dctx)
    print("Data provider for alarms started...")
    
    while True:
        dp.fd_ready(dctx, wsock.fileno())

if __name__ == "__main__":
    register_data_provider()
