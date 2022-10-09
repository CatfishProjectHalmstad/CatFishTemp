import SensorAbstract
import minimalmodbus

class SensorDO(SensorAbstract):
    """
    Class for the Disolved Oxygen (DO) sensor
    """

    def __init__(self, serialPath, baud):
        self.serialPath = serialPath

    initiated = False
    doSensor = None

    def initilize_sensor(self):
        self.doSensor = minimalmodbus.Instrument(self.serialPath, 21, 
                            mode=minimalmodbus.MODE_RTU)
        
        # Make the settings explicit
        self.doSensor.serial.baudrate = 9600
        self.doSensor.serial.bytesize = 8
        self.doSensor.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.doSensor.serial.stopbits = 1
        self.doSensor.serial.timeout = 5
        self.doSensor.close_port_after_each_call = True
        self.doSensor.clear_buffers_before_each_transaction = True

        self.initiated = True

    def successfully_initialized(self):
        return self.initiated

    def name(self):
        return "do_sensor"

    def get_value(self):
        if self.initiated is None or self.doSensor is None: 
            return None

        try: 
            toReturn = {}
            toReturn['temperature'] = self.doSensor.read_float(83)
            toReturn['domql'] = self.doSensor.read_float(87)
            toReturn['doppm'] = self.doSensor.read_float(89)
            return toReturn
        except:
            return None