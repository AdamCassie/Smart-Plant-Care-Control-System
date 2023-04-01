import serial
import csv
import time

ser = serial.Serial('COM3', 4800, timeout=1)
filename = 'arduino_output.csv'

while True:
    data = ser.readline().decode('utf-8')
    if data:
        data = data.strip().split(' ')
        data.append(time.strftime('%Y-%m-%d %H:%M:%S'))
        print(data)
        with open(filename, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)