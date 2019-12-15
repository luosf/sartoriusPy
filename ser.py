#coding=utf-8
import serial

class Sartorius(serial.Serial):
    def __init__(self,port):
        """
        Initialise Sartorius device.
            Example:
            scale = Sartorius('COM1')
        """
        serial.Serial.__init__(self, port)

    def set_config(self,config):
        self.port= config['SERIAL']['COM']
        self.baudrate = int(config['SERIAL']['Baudrate'])
        self.bytesize = int(config['SERIAL']['bytesize'])
        self.parity = eval(config['SERIAL']['parity'])
        self.query = config['COMMAND']['query']
        self.zero = config['COMMAND']['zero']

    def value(self):
        """
        Return displayed scale value.
        """
        self.write(self.query.encode())
        answer = self.readline()
        return answer
    

    def tara_zero(self):
        """
        Tara and zeroing combined.
        """
        self.write('\033T\n')

    def tara(self):
        """
        Tara.
        """
        self.write('\033U\n')

    def zero(self):
        """
        Zero.
        """
        self.write('\033V\n'.encode())

if __name__ == '__main__':
    
    scale = Sartorius(config)

    print(scale.value())
    # zero scale
    # scale.zero()
    print(scale.value())
