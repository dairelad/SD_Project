import logging as log
import socket
import atexit
from datetime import datetime
import datetime as dt
import os

# Local IP/Port for the honeypot to listen on (TCP)
LHOST = '0.0.0.0'
LPORT = 8080 # non admin http port

#Create folders for seperate days
path = os.getcwd()
if not os.path.exists('Day1'):
    for i in range(7):
        os.mkdir(f'Day{i+1}')

# Socket timeout in seconds
TIMEOUT = 0.00001

# Banner information
BANNER = "HTTP/1.1 403 Forbidden" \
         "Date: Mon, 09 Nov 2021 18:59:22 GMT" \
         "Server: Apache" \
         "Content-Length: 264" \
         "Content-Type: text/html; charset=iso-8859-1"

# Code to run segment at a particular time of day
start = dt.time(0, 0, 0)
end = dt.time(0, 1, 0)

def time_in_range(start, end, x):
	"""Return true if x is in the range [start, end]"""
	if start <= end:
		return start <= x <= end
	else:
		return start <= x or x <= end

def check_day(self):
    now = dt.datetime.now()
    hr = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    sec = int(now.strftime("%S"))
    now = dt.time(hr, min, sec)
    if time_in_range(start, end, now):
        self.day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1

def main():
    day = datetime.today().weekday() + 1  # saves current day (monday=0 & sunday=6)+1
    # code used for logging information about the attack
    log.basicConfig(
        filename=f'{path}/Day{day}/httpD{day}.log',
        level=log.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )

    print ('[*] HTTP honeypot listening for connection on ' + LHOST + ':' + str(LPORT))
    atexit.register(exit_handler)

    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(5)
    count = 0
    while True:
        try:
            (connection, address) = listener.accept()
            log.info('New connection from: ' + address[0])
            listener.settimeout(TIMEOUT)
            print ('[*] Honeypot connection from ' + address[0] + ':' + str(address[1]) + ' on port ' + str(LPORT))
            connection.send(BANNER.encode())
            count = 0
        except socket.timeout as e:
            if(count < 1):
                print("Connection closed by host.")
                connection.close()
                count += 1

def exit_handler():
    print ('\n[*] HTTP honeypot is shutting down!')
    listener.close()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass