# Example MQTT bridge to publish state to a broker (e.g., for fleet dashboards)
import json, time
import paho.mqtt.client as mqtt

def publish_state(state: dict, host="localhost", topic="nirvaha/state"):
    c = mqtt.Client()
    c.connect(host, 1883, 60)
    c.publish(topic, json.dumps(state), qos=0, retain=False)
    c.disconnect()
