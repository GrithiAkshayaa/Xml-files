import sys
import time
import socket
from lxml import etree

def send_notification():
    # NETCONF notification structure
    event_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    notification = etree.Element("notification", xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0")

    event_time_elem = etree.SubElement(notification, "eventTime")
    event_time_elem.text = event_time

    alarms_elem = etree.SubElement(notification, "alarms", xmlns="http://openconfig.net/yang/alarms")
    alarm_elem = etree.SubElement(alarms_elem, "alarm")

    # Alarm details
    etree.SubElement(alarm_elem, "id").text = "alarm-001"
    etree.SubElement(alarm_elem, "resource").text = "/components/component[name='slot1']"
    etree.SubElement(alarm_elem, "text").text = "Equipment failure detected"
    etree.SubElement(alarm_elem, "time-created").text = str(int(time.time()))
    etree.SubElement(alarm_elem, "severity").text = "CRITICAL"
    etree.SubElement(alarm_elem, "type-id").text = "equipment-failure"

    xml_notification = etree.tostring(notification, pretty_print=True).decode()

    # Send the notification using NETCONF
    send_to_confd(xml_notification)

def send_to_confd(notification):
    """ Sends the notification XML to ConfD NETCONF server via socket. """
    host = "127.0.0.1"
    port = 2022  # Replace with your ConfD NETCONF port

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(notification.encode())
        sock.close()
        print("Notification sent successfully!")
    except Exception as e:
        print(f"Failed to send notification: {e}")

if __name__ == "__main__":
    send_notification()
