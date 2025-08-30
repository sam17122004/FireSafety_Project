#!/usr/bin/env python3
import argparse, time, random, json, sys
try:
    import paho.mqtt.client as mqtt
except Exception as e:
    mqtt = None

def generate_sample():
    return {
        "temperature_c": round(random.uniform(20, 120), 2),
        "smoke_ppm": round(random.uniform(50, 600), 1),
        "gas_mq2": round(random.uniform(100, 1000), 1),
        "timestamp": time.time()
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--broker", default="localhost")
    ap.add_argument("--topic", default="plant/sensors")
    ap.add_argument("--interval", type=float, default=1.0)
    args = ap.parse_args()

    client = None
    if args.publish and mqtt is not None:
        client = mqtt.Client()
        client.connect(args.broker, 1883, 60)

    try:
        while True:
            msg = generate_sample()
            line = json.dumps(msg)
            print(line)
            if client:
                client.publish(args.topic, line)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
