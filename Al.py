#!/usr/bin/env python3
import sys
import socket
import _confd
import _confd.dp as dp

# Alarm state data (Example)
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

# ConfD Callback: Get Alarm State Data
def get_elem(tctx, kp):
    key = dp.keypath_to_str(kp)
    
    if "/alarms/alarm{" in key:
        alarm_id = key.split("{")[1].split("}")[0]
        if alarm_id in alarms_data:
            field = key.split("/")[-1]
            if field in alarms_data[alarm_id]:
                return _confd.ConfValue(alarms_data[alarm_id][field])
    
    return _confd.CONFD_ERR

# Register the Data Provider
def register_data_provider():
    dctx = dp.init_daemon("alarm_data_provider")
    
    # Worker socket to communicate with ConfD
    wsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    _confd.connect(wsock, _confd.addr("127.0.0.1", _confd.CONFD_PORT), _confd.WORKER_PROTO)
    
    # Register callbacks
    dp.register_trans_cb(dctx, dp.trans_cb())
    dp.register_data_cb(dctx, dp.data_cb(get_elem))

    dp.register_done(dctx)
    
    print("Alarm Data Provider Registered")
    
    while True:
        dp.fd_ready(dctx, wsock.fileno())

# Run the provider
if __name__ == "__main__":
    register_data_provider()
