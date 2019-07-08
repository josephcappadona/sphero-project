import socket, sys
import r2d2


class Server:

    r2d2 = None

    def __init__(self, r2d2):
        if r2d2:
            self.r2d2 = r2d2
        #else:
        #    raise ValueError('Must provide valid R2D2 object')

    def start(self, host='127.0.0.1', port=1337):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.host, self.port = host, port
        self.sock.listen(1)
        self.accept()
        
    def accept(self):
        self.sock.setblocking(1)
        print('Waiting for client connection...')
        self.conn, self.client_addr = self.sock.accept()
        self.conn.setblocking(0)
        print('Client (%s) connected.' % ':'.join([str(s) for s in self.client_addr]))
        self.send_message('Connected to Sphero server.\r\n')


    def send_message(self, msg):
        self.conn.sendall(msg.encode())

    def receive_data(self):
        try:
            if self.conn == None:
                return
            data = self.conn.recv(1024)
        except socket.timeout as e:
            #print('timeout error: %s' % e)
            pass
        except socket.error as e:
            #print('socket error: %s' % e)
            pass
        else:
            if len(data) == 0:
                #print('len data is 0, orderly shutdown')
                #self.sock.close()
                pass
            else:
                print('Command: %s' % data.decode())
                return data.decode().strip()

    def handle_data(self, data, r2):
        if data == None or r2 == None:
            return
        for command_str in data.split('\r\n'):
            self.handle_command(command_str, r2)

    def handle_command(self, command_str, r2):
        command = command_str.split(' ')
        if command[0] == 'connect':
            if r2.heading != 0:
                r2.rotate(-r2.heading, send_response=False)
            self.send_message('Connected to %s.\r\n' % r2.name)
            self.send_message('Ready for commands!\r\n')
        elif command[0] == 'turn':
            angle = int(command[1])
            if (angle % 360) != r2.heading:
                to_rotate = min(angle % 360, (angle % 360) - 360, key=lambda x: abs(x))
                r2.rotate(to_rotate)
        elif command[0] == 'roll_time':
            speed, angle, time = command[1:]
            speed = min(float(speed), 1.0)
            angle = int(angle)
            time = float(time)

            r2.roll(speed, angle, time)
        elif command[0] == 'roll_continuous':
            speed = float(command[1])
            angle = int(command[2])

            self.send_message('Initializing rolling.\r\n')
            r2.roll(speed, angle, 1000)
        elif command[0] == 'set_stance':
            stance = int(command[1])
            r2.set_stance(stance)
        elif command[0] == 'quit' or command[0] == 'exit' or command[0] == 'close' or command[0] == 'disconnect':
            self.send_message('Disconnected.\r\n')
            self.conn.close()
            self.accept()

    def done_rolling(self):
        self.send_message('Done rolling.\r\n')

    def done_turning(self):
        self.send_message('Done turning.\r\n')

    def stance_set(self):
        self.send_message('Stance set.\r\n')

if __name__ == '__main__':
    s = Server(None)
    s.start()

