import serial

# Replace 'COM5' with your actual COM port
ser = serial.Serial("COM5", 9600)

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()

        # Display the received data in the terminal
        print("A0 Value:", line)
except KeyboardInterrupt:
    # Close the serial port when the script is interrupted
    ser.close()
