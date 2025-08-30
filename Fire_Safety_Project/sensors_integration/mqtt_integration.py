#!/usr/bin/env python3
import argparse, json, sys, time
try:
    import paho.mqtt.client as mqtt
except Exception as e:
    mqtt = None

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except Exception:
        payload = {"raw": msg.payload.decode("utf-8", "ignore")}
    print(f"[MQTT] {msg.topic}: {payload}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--broker", default="localhost")
    ap.add_argument("--topic", default="fire/alerts")
    args = ap.parse_args()

    if mqtt is None:
        print("paho-mqtt not available. Install from requirements.txt")
        return

    client = mqtt.Client()
    client.on_message = on_message
    client.connect(args.broker, 1883, 60)
    client.subscribe(args.topic)
    print(f"Subscribed to {args.topic} on {args.broker}")
    client.loop_forever()

if __name__ == "__main__":
    main()
