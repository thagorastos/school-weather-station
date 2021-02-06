#!/usr/bin/env python
#
# This is a weeWX driver to enable weeWX to read data from a Microbit Climate.
#
# See here for more details:
#
# https://github.com/wrybread/ArduinoWeatherStation
#
# by th_agorastos@hotmail.com
#
#
#

"""Driver for Micro:bit Climate weather station.

See here for more info:

https://google.gr

"""

from __future__ import with_statement
import serial
import syslog
import time
import io
from pprint import pprint
import weewx.drivers

DRIVER_NAME = 'microbit'
DRIVER_VERSION = '0.1'


def loader(config_dict, _):
    return MicrobitDriver(**config_dict[DRIVER_NAME])


def confeditor_loader():
    return MicrobitConfEditor()


INHG_PER_MBAR = 0.0295333727
METER_PER_FOOT = 0.3048
MILE_PER_KM = 0.621371

DEFAULT_PORT = '/dev/ttyACM0'
DEBUG_READ = 1

def logmsg(level, msg):
    syslog.syslog(level, 'Microbit: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)







class MicrobitDriver(weewx.drivers.AbstractDevice):
    """weewx driver that communicates with an Arduino weather station

    port - serial port
    [Required. Default is /dev/ttyACM0]

    polling_interval - how often to query the serial interface, seconds
    [Optional. Default is 1]

    max_tries - how often to retry serial communication before giving up
    [Optional. Default is 5]

    retry_wait - how long to wait, in seconds, before retrying after a failure
    [Optional. Default is 10]
    """
    def __init__(self, **stn_dict):
        self.port = stn_dict.get('port', DEFAULT_PORT)

        self.polling_interval = float(stn_dict.get('polling_interval', 2))
        self.max_tries = int(stn_dict.get('max_tries', 10))
        self.retry_wait = int(stn_dict.get('retry_wait', 10))
        self.last_rain = None
        loginf('driver version is %s' % DRIVER_VERSION)
        loginf('using serial port %s' % self.port)
        loginf('polling interval is %s' % self.polling_interval)
        global DEBUG_READ
        DEBUG_READ = int(stn_dict.get('debug_read', DEBUG_READ))

        self.last_read_time = time.time()
        self.read_counter = 0


        logdbg("Opening the Arduino on port %s" % self.port)

        self.baudrate = 115200
        self.timeout = 10  # changed from 60
        self.serial_port = None

        try:
            self.serial_port = serial.Serial(self.port, self.baudrate,
                                             timeout=self.timeout)
            self.serial_port.flush()

            logdbg("Successfully opened the Arduino.")

        except Exception as e:

            logerr("Error opening the Arduino! %s" % e)

    def read_buffer(self):
        # read the buffer
        new_data = ""

        try:
            while True:
                # sio = io.TextIOWrapper(io.BufferedReader(self.serial_port))  # , newline="\r\n")
                # new_data = sio.readline()
                # new_data = new_data.replace("\r\n", "")
                new_data = self.serial_port.read(self.serial_port.inWaiting()).decode('ascii')

                self.serial_port.flush()

                return new_data

        except Exception:
            print("exception: ", self.serial_port.in_waiting)
            pass

    def parse_readings(self, b):
        """
        The Arduino script emits data in the format:

          [0]wind speed
          [1]wind direction
          [2]wind direction compass
          [3]temperature
          [4]barometer
        """
  
        data = {}

        try:
            if "," in b:
                parts = b.split(",")
                # print("parsing: ", b, "parts =", parts)
                data = dict()
                data['outTemp'] = float(parts[0])
                data['pressure'] = float(parts[1])
                data['outHumidity'] = float(parts[2])
                data['windSpeed'] = float(parts[3])
                data['windDir'] = float(parts[4])
                data['soilMoist1'] = float(parts[5])
                data['soilTemp1'] = float(parts[6])
                rain = parts[7].replace('\r\n', '').strip()
                data['rainTotal'] = float(rain)
                # pprint("Microbit driver: ", data)

        except Exception as e:
            logerr("Error parsing data: %s" % e)

        if DEBUG_READ:
            logdbg(data)

        return data





    @property
    def hardware_name(self):
        return "microbit"


    def genLoopPackets(self):

        ntries = 0

        while ntries < self.max_tries:

            ntries += 1

            try:

                packet = {'dateTime': int(time.time() + 0.5),
                          'usUnits': weewx.METRIC}

                serial_data = self.read_buffer()  # read the buffer from the microbit climate

                data = self.parse_readings(serial_data)  # parse the data

                packet.update(data)

                self._augment_packet(packet)

                ntries = 0


                '''
                # print the time between reads and the count for debugging for now
                self.read_counter += 1
                time_since_last_read = time.time() - self.last_read_time
                print("%s seconds since last read" % time_since_last_read, self.read_counter)
                self.last_read_time = time.time()
                '''

                yield packet

                if self.polling_interval:
                    time.sleep(self.polling_interval)

            except (serial.serialutil.SerialException, weewx.WeeWxIOError) as e:
                logerr("Failed attempt %d of %d to get LOOP data: %s" %
                       (ntries, self.max_tries, e))
                time.sleep(self.retry_wait)

        else:
            msg = "Max retries (%d) exceeded for LOOP data" % self.max_tries
            logerr(msg)
            raise weewx.RetriesExceeded(msg)



    def _augment_packet(self, packet):

        # no wind direction when wind speed is zero
        if 'windSpeed' in packet and not packet['windSpeed']:
            packet['windDir'] = None

	# packet['rain'] = weewx.wxformulas.calculate_rain(packet.get('rain_total'), self.last_rain)
        # self.last_rain = packet.get('rain_total')








class MicrobitConfEditor(weewx.drivers.AbstractConfEditor):

    @property
    def default_stanza(self):
        return """
[Microbit]
    # This section is for an Arduion Weather Station.

    # Serial port such as /dev/ttyACM0, /dev/ttyS0, /dev/ttyUSB0, or /dev/cuaU0
    port = /dev/ttyACM0

    # The driver to use:
    driver = user.microbit
"""

    def prompt_for_settings(self):
        print("Specify the serial port on which the station is connected, for")
        print("example /dev/ttyUSB0 or /dev/ttyACM0.")
        port = self._prompt('port', '/dev/ttyACM0')
        return {'port': port}

# define a main entry point for basic testing of the station without weewx
# engine and service overhead.  invoke this as follows from the weewx root dir:
#
# # To run on a standard apt-get install (unconfirmed, might ened to adjust path
# PYTHONPATH=bin python /home/weewx/bin/user/Microbit.py

# For setup.py instals:
# PYTHONPATH=/home/weewx/bin python /home/weewx/bin/user/Microbit.py
#

if __name__ == '__main__':

    import optparse

    usage = """%prog [options] [--help]"""

    syslog.openlog('micro', syslog.LOG_PID | syslog.LOG_CONS)
    syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_DEBUG))
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--version', dest='version', action='store_true',
                      help='display driver version')
    parser.add_option('--port', dest='port', metavar='PORT',
                      help='serial port to which the station is connected',
                      default=DEFAULT_PORT)
    (options, args) = parser.parse_args()

    if options.version:
        print("micro driver version %s" % DRIVER_VERSION)
        exit(0)



    station = MicrobitDriver()
    for packet in station.genLoopPackets():
        print(time.time(), packet)

