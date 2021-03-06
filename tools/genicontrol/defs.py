#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2016 by Christoph Schueler <github.com/Christoph2,
##                                      cpu12.gems@googlemail.com>
##
##  All Rights Reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##

from collections import namedtuple
import os

##
## Common constants.
##
HOME_DIRECTORY = os.path.abspath(os.path.expanduser('~/'))
CONFIGURATION_DIRECTORY = os.path.join(HOME_DIRECTORY, 'GeniControl')
if not os.access(CONFIGURATION_DIRECTORY, os.F_OK):
    print("Configuration directory '{0}' doesn't exist. creating...".format(CONFIGURATION_DIRECTORY))
    os.mkdir(CONFIGURATION_DIRECTORY)

##
## Connection constants.
##
CONNECTION_SIMULATOR    = 0
CONNECTION_GENBUS_TCP   = 1
CONNECTION_GENIBUS_DLL  = 2

##
## GeniBus constants.
##
START_DELIMITER     = 0
LENGTH              = 1
DESTINATION_ADRESS  = 2
SOURCE_ADDRESS      = 3
PDU_START           = 4

CRC_HIGH            = -2
CRC_LOW             = -1

MAX_TELEGRAM_LEN    = 259
MAX_PDU_LEN         = 253
SLAVE_ADDR_OFFSET   = 32
CONNECTION_REQ_ADDR = 254
BROADCAST_ADDR      = 255

SD_DATA_REQUEST     = 0x27
SD_DATA_REPLY       = 0x24
SD_DATA_MESSAGE     = 0x26

## Access constants.
ACC_RO  = 0x01
ACC_WO  = 0x02
ACC_WR  = 0x03


##
## APDU classes.
##
class APDUClass:
    PROTOCOL_DATA                       = 0
    BUS_DATA                            = 1
    MEASURED_DATA                       = 2
    COMMANDS                            = 3
    CONFIGURATION_PARAMETERS            = 4
    REFERENCE_VALUES                    = 5
    TEST_DATA                           = 6
    ASCII_STRINGS                       = 7
    MEMORY_BLOCKS                       = 8
    EMBEDDED_PUDS                       = 9
    DATA_OBJECTS                        = 10
    SIXTEENBIT_MEASURED_DATA            = 11
    SIXTEENBIT_CONFIGURATION_PARAMETERS = 12
    SIXTEENBIT_REFERENCE_VALUES         = 13

    nameDict = {
        PROTOCOL_DATA                       : 'PROTOCOL_DATA',
        BUS_DATA                            : 'BUS_DATA',
        MEASURED_DATA                       : 'MEASURED_DATA',
        COMMANDS                            : 'COMMANDS',
        CONFIGURATION_PARAMETERS            : 'CONFIGURATION_PARAMETERS',
        REFERENCE_VALUES                    : 'REFERENCE_VALUES',
        TEST_DATA                           : 'TEST_DATA',
        ASCII_STRINGS                       : 'ASCII_STRINGS',
        MEMORY_BLOCKS                       : 'MEMORY_BLOCKS',
        EMBEDDED_PUDS                       : 'EMBEDDED_PUDS',
        DATA_OBJECTS                        : 'DATA_OBJECTS',
        SIXTEENBIT_MEASURED_DATA            : 'SIXTEENBIT_MEASURED_DATA',
        SIXTEENBIT_CONFIGURATION_PARAMETERS : 'SIXTEENBIT_CONFIGURATION_PARAMETERS',
        SIXTEENBIT_REFERENCE_VALUES         : 'SIXTEENBIT_REFERENCE_VALUES',
    }

    @staticmethod
    def toString(klass):
        return APDUClass.nameDict[klass]


NICE_CLASS_NAMES = {
    APDUClass.PROTOCOL_DATA:                       "Protocol Data",
    APDUClass.BUS_DATA:                            "Bus Data",
    APDUClass.MEASURED_DATA:                       "Measured Data",
    APDUClass.COMMANDS:                            "Commands",
    APDUClass.CONFIGURATION_PARAMETERS:            "Configuration Parameters",
    APDUClass.REFERENCE_VALUES:                    "Reference Values",
    APDUClass.TEST_DATA:                           "Test Data",
    APDUClass.ASCII_STRINGS:                       "ASCII Strings",
    APDUClass.MEMORY_BLOCKS:                       "Memory Blocks",
    APDUClass.EMBEDDED_PUDS:                       "Embedded PDUs",
    APDUClass.DATA_OBJECTS:                        "Data Objects",
    APDUClass.SIXTEENBIT_MEASURED_DATA:            "16Bit Measured Data",
    APDUClass.SIXTEENBIT_CONFIGURATION_PARAMETERS: "16Bit Configuration Parameters",
    APDUClass.SIXTEENBIT_REFERENCE_VALUES:         "16Bit Reference Values",
}


##
## Supported classes (by GeniControl).
##
SUPPORTED_CLASSES = (
    APDUClass.PROTOCOL_DATA,
    APDUClass.MEASURED_DATA,
    APDUClass.COMMANDS,
    APDUClass.CONFIGURATION_PARAMETERS,
    APDUClass.REFERENCE_VALUES,
    APDUClass.ASCII_STRINGS,
    APDUClass.SIXTEENBIT_MEASURED_DATA
)


##
## Operation specifiers.
##
OS_GET  = 0
OS_SET  = 2
OS_INFO = 3

##
## Acknowledges.
##
ACK_OK                  = 0
ACK_CLASS_UNKNOWN       = 1
ACK_ID_UNKNOWN          = 2
ACK_OPERATION_ILLEGAL   = 3

##
## Valid operations for APDU classes.
##
CLASS_CAPABILITIES = {
    APDUClass.PROTOCOL_DATA                       : (OS_GET, ),
    APDUClass.BUS_DATA                            : (OS_GET, ),
    APDUClass.MEASURED_DATA                       : (OS_GET, OS_INFO),
    APDUClass.COMMANDS                            : (OS_SET, OS_INFO),
    APDUClass.CONFIGURATION_PARAMETERS            : (OS_GET, OS_SET, OS_INFO),
    APDUClass.REFERENCE_VALUES                    : (OS_GET, OS_SET, OS_INFO),
    APDUClass.TEST_DATA                           : (OS_GET, OS_SET, ),
    APDUClass.ASCII_STRINGS                       : (OS_GET, ),
    APDUClass.MEMORY_BLOCKS                       : (OS_GET, OS_SET, ),
    APDUClass.EMBEDDED_PUDS                       : (OS_GET, ),
    APDUClass.DATA_OBJECTS                        : (OS_GET, OS_SET, ),
    APDUClass.SIXTEENBIT_MEASURED_DATA            : (OS_GET, OS_INFO),
    APDUClass.SIXTEENBIT_CONFIGURATION_PARAMETERS : (OS_GET, OS_SET, OS_INFO),
    APDUClass.SIXTEENBIT_REFERENCE_VALUES         : (OS_GET, OS_SET, OS_INFO)
}

class IllegalOperationError(Exception): pass

def operationToString(op):
    if op == OS_GET:
        return "Read"
    elif op == OS_SET:
        return "Write"
    elif op == OS_INFO:
        return "Info-Request"

Item = namedtuple('Item', 'name value info')
Info = namedtuple('Info', 'head unit zero range')
