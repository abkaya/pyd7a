#!/usr/bin/env python

import argparse

import logging

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS, ResponseMode
from d7a.system_files.uid import UidFile
from modem.modem import Modem


# This example can be used with a node running the gateway app included in OSS-7.
# The gateway is continuously listening for foreground frames.
# Messages pushed by other nodes (running for example the sensor_push app) will be received by the gateway node,
# transmitted over serial and the received_command_callback() function below will be called.
from util.logger import configure_default_logger


def received_command_callback(cmd):
  data=cmd.actions[0].operand.data
  data=map(int, data)
  publish_cozirlp(data)
  #print(data)
  #logging.info(cmd)

def publish_cozirlp(data):
  H = (data[0] << 7) | data[1]
  T = (data[2] << 7) | data[3]
  Z = (data[4] << 7) | data[5]
  # x is a two's complement integer with two bytes, therefore it needs the proper conversion for its signedness when negative
  if is_twos_negative(H):
    H = H - (1 << 16)
  if is_twos_negative(T):
    T = T - (1 << 16)
  if is_twos_negative(Z):
    Z = Z - (1 << 16)
  print("\nHumidity[?datasheet]: "+ str(H) + "\nTemperature[?datasheet]: "+ str(T) + "\nCO2[ppm]: "+ str(Z))
    #publish.single("sensordata/topic", str(x), hostname="localhost")
    #publish.single("sensordata/topic", str(y), hostname="localhost")
    #publish.single("sensordata/topic", str(z), hostname="localhost")

def is_twos_negative(val):
    constant = 1 << (15);
    if (val & constant):
        return 1;
    return 0

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
config = argparser.parse_args()

configure_default_logger(config.verbose)

modem = Modem(config.device, config.rate, unsolicited_response_received_callback=received_command_callback)

while True:
  pass
