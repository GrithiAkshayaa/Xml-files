from ncclient import manager
import time

# ConfD NETCONF server details
NETCONF_HOST = "127.0.0.1"
NETCONF_PORT = 2022  # Adjust if needed
NETCONF_USER = "admin"
NETCONF_PASS = "admin"

# Define NETCONF Notification XML for Alarm Event
notification = f"""<notification xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
    <eventTime>{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}</eventTime>
    <alarms xmlns="http://openconfig.net/yang/alarms">
        <alarm>
            <id>alarm-001</id>
            <resource>/components/component[name='slot1']</resource>
            <text>Equipment failure detected</text>
            <time-created>{int(time.time())}</time-created>
            <severity>CRITICAL</severity>
            <type-id>equipment-failure</type-id>
        </alarm>
    </alarms>
</notification>"""

# Connect to NETCONF server and send notification
try:
    with manager.connect(
        host=NETCONF_HOST,
        port=NETCONF_PORT,
        username=NETCONF_USER,
        password=NETCONF_PASS,
        hostkey_verify=False
    ) as m:
        rpc_reply = m.dispatch(notification)
        print("✅ Alarm Notification Sent Successfully!")
        print(rpc_reply)
except Exception as e:
    print(f"❌ Error: {e}")
