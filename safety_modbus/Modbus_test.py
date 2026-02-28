
from pymodbus.client import ModbusSerialClient


# Modbus configuration

PORT = "COM10"          # change if needed
BAUDRATE = 9600
DEVICE_ID = 1
REGISTER_ADDR = 0

client = ModbusSerialClient(
    port=PORT,
    baudrate=BAUDRATE,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)


# Connect to Modbus server

if not client.connect():
    print("Connection failed") 
    exit()

print("Connected")
print("Enter HEX mask (example: FFFE)")
print("Type 'exit' to quit\n")


# LED state (bitmask)

#led_mask = 0     #stores current led states as bits 

#while led_mask : 0x0000   # logical ON/OFF state (1 = ON)

while True:
    user_input = input(">> ")

    if user_input.lower() == "exit":
        break

    try:
        mask = int(user_input, 16) & 0xFFFF        # e.g. FFFE

        client.write_register(
            address=REGISTER_ADDR,
            value=mask,     # active-LOW to ESP32
            device_id=DEVICE_ID
        )

        print(f"Toggled mask 0x{mask:04X}")

    except ValueError:
        print("Enter a valid HEX mask (e.g. FFFE)")



client.close()
print("Disconnected")
