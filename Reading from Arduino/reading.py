import serial

ser = serial.Serial('COM3', 4800)

while True:
    data = ser.readline().decode('utf-8').strip()
    print(data)
