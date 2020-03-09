# -*- coding: UTF-8 -*-

#debug switch-- 1:on / 0:off
debug = 0
#if debug:

#command code
leading_cmd             = 0xAA
GET_TEMP_HUM_cmd        = 0xB0
GET_CO2_cmd             = 0xB1
GET_TVOC_cmd            = 0xB2
GET_LIGHT_cmd           = 0xB3
GET_PMS_cmd             = 0xB4
GET_SENSOR_ALL_cmd      = 0xB5
GET_INFO_VERSION_cmd    = 0xB6
GET_INFO_RUNTIME_cmd    = 0xB7
GET_INFO_ERROR_LOG_cmd  = 0xB8
GET_INFO_SENSOR_POR_cmd = 0xB9 # V1.1 (Update)
GET_RTC_DATE_TIME_cmd   = 0xBA
GET_INFO_PIN_STATE_cmd  = 0xBB # V1.1 (New)

SET_STATUS_LED_cmd       = 0xBC # V1.1 (New) /correct to 0xBC not 0xBF
SET_PIN_CO2_CAL_cmd      = 0xC0
SET_PIN_PMS_RESET_cmd    = 0xC1
SET_PIN_PMS_SET_cmd      = 0xC2
SET_PIN_NBIOT_PWRKEY_cmd = 0xC3
SET_PIN_NBIOT_SLEEP_cmd  = 0xC4
SET_PIN_LED_ALL_cmd      = 0xC5
SET_POLLING_SENSOR_cmd   = 0xC6 # V1.1 (Update)
SET_RTC_DATE_TIME_cmd    = 0xC7 # V1.1 (Update)
SET_PIN_FAN_ALL_cmd      = 0xC8 # V1.1 (New)

SET_PIN_CO2_CAL_key      = bytearray([0x53,0x38,0x4C,0x50])
SET_PIN_PMS_RESET_key    = bytearray([0x50,0x4D,0x53,0x33])
SET_PIN_PMS_SET_key      = bytearray([0x33,0x30,0x30,0x33])
SET_PIN_NBIOT_PWRKEY_key = bytearray([0x4E,0x42,0x2D,0x49])
SET_PIN_NBIOT_SLEEP_key  = bytearray([0x2D,0x49,0x4F,0x54])
SET_PIN_LED_ALL_key      = bytearray([0x53,0x4C,0x45,0x44])
SET_PIN_FAN_ALL_key      = bytearray([0x46,0x41,0x4E,0x63]) # V1.1 (New)


PROTOCOL_I2C_WRITE_cmd    = 0xCA
PROTOCOL_I2C_READ_cmd     = 0xCB
PROTOCOL_UART_BEGIN_cmd   = 0xCC
PROTOCOL_UART_TX_RX_cmd   = 0xCD # V1.1 (Update)
PROTOCOL_UART_TXRX_EX_cmd = 0xCE # V1.1 (New)

ENABLE_UART_ACTIVE_RX_cmd = 0xCF # V1.1 (New)
ECHO_UART_ACTIVE_RX_cmd   = 0xCF # V1.1 (New)

#expect receive

GET_TEMP_HUM_resp        = 8
GET_CO2_resp             = 8
GET_TVOC_resp            = 16
GET_LIGHT_resp           = 16
GET_PMS_resp             = 16
GET_SENSOR_ALL_resp      = 48
GET_INFO_VERSION_resp    = 6
GET_INFO_RUNTIME_resp    = 9
GET_INFO_ERROR_LOG_resp  = 16
GET_INFO_SENSOR_POR_resp = 16 # V1.1 (Update)
GET_RTC_DATE_TIME_resp   = 10
GET_INFO_PIN_STATE_resp  = 11 # V1.1 (New)

SET_STATUS_LED_resp       = 4 # V1.1 (New)
SET_PIN_CO2_CAL_resp      = 4
SET_PIN_PMS_RESET_resp    = 4
SET_PIN_PMS_SET_resp      = 4
SET_PIN_NBIOT_PWRKEY_resp = 4
SET_PIN_NBIOT_SLEEP_resp  = 4
SET_PIN_LED_ALL_resp      = 4
SET_POLLING_SENSOR_resp   = 4 # V1.1 (Update)
SET_RTC_DATE_TIME_resp    = 4 # V1.1 (Update)
SET_PIN_FAN_ALL_resp      = 4 # V1.1 (New)

PROTOCOL_I2C_WRITE_resp    = 4
#PROTOCOL_I2C_READ_resp     = 6+n
PROTOCOL_UART_BEGIN_resp   = 4
#PROTOCOL_UART_TX_RX_resp   = 6+n # V1.1 (Update)
#PROTOCOL_UART_TXRX_EX_resp = 8+n # V1.1 (New)

ENABLE_UART_ACTIVE_RX_resp = 4 # V1.1 (New)
#ECHO_UART_ACTIVE_RX_resp   = 7+n # V1.1 (New)

#==========CONVERT FUNC==========#

#Bit_not
#therer is 2 ways to do
#1. (N xor 0xFF...) / any digit xor with (len(n) of 1) will be reverse / 
#2. use (~N & 0xFF) / this will limit output to just 1byte  <- choose this one

def bit_reverse(byte_command):
    rev_command = (~byte_command & 0xFF)

    return rev_command


#crc_calc
#checksum = ∑( Byte n xor (n%256) )
# so in loop of len(Byte), every Byte do xor with n 
# and sum every thing, do a AND with 0xFF limit to 1 Byte

def crc_calc(byte_arr):
    checksum = 0x00    
    for i in range(len(byte_arr)):
        checksum = checksum + (byte_arr[i] ^ ((i+1)%256))
        #print(hex(byte_arr[i]).upper() + ' ^ ' + hex(((i+1)%256)).upper() + ' = ' + hex(byte_arr[i] ^ ((i+1)%256)).upper()) 
    checksum = (checksum & 0xFF)

    return checksum


#byte formater
#convert 'int' to 'byte'
#and create proper format for multiple byte 

def convert_2_byte(int_value):
    host_send = bytearray()
    host_send.append(int_value // 256)
    host_send.append(int_value % 256)
    
    return host_send


def convert_4_byte(int_value):
    host_send = bytearray()
    byte_0 = int_value // (256 * 256 * 256)
    byte_1 = (int_value % (256 * 256 * 256)) // (256 * 256)
    byte_2 = (int_value % (256 * 256)) // 256
    byte_3 = int_value % 256
    
    host_send.append(byte_0)
    host_send.append(byte_1)
    host_send.append(byte_2)
    host_send.append(byte_3)
    
    return host_send





#==========GENERAL FUNC==========#

def GENERAL_GET(cmd):
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #b_arr = bytearray(host_send)

##    print("****")
##    print(host_send)
##    print(type(host_send))
##    print("****")
    

    return host_send

def GENERAL_SET(cmd,key,state):
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #key
    host_send.append(key[0])
    host_send.append(key[1])
    host_send.append(key[2])
    host_send.append(key[3])
    #state
    host_send.append(state)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def GENERAL_RESPONSE(cmd,recive_byte):
    data = ser.read(recive_byte)

    return data

    

    


def POLLING_SET(temp_sw,co2_sw,tvoc_sw,light_sw,pms_sw,rtc_sw):
    #command for SET_POLLING_SENSOR
    cmd = SET_POLLING_SENSOR_cmd
    
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #state for 6 sensor
    host_send.append(temp_sw)
    host_send.append(co2_sw)
    host_send.append(tvoc_sw)
    host_send.append(light_sw)
    host_send.append(pms_sw)
    host_send.append(rtc_sw)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def RTC_SET(YY,MM,DD,hh,mm,ss):
    #command for SET_RTC_DATE_TIME
    cmd = SET_RTC_DATE_TIME_cmd
    
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #state for 6 sensor
    host_send.append(YY)
    host_send.append(MM)
    host_send.append(DD)
    host_send.append(hh)
    host_send.append(mm)
    host_send.append(ss)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send
    
def LED_SET(cmd,state):
    #command for SET_STATUS_LED, because there is no key
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #state
    # 2 Byte
    state = convert_2_byte(state)
    host_send.extend(state)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send

    

#===============GET COMMAND===============#
def GET_TEMP_HUM():

    #ser.write()
    if debug:
        print("AA 55 B0 4F")
    #print(GENERAL_GET(GET_TEMP_HUM_cmd))
    data = GENERAL_GET(GET_TEMP_HUM_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_TEMP_HUM_cmd,GET_TEMP_HUM_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        TEMP = (reveive_data[3]*256 + reveive_data[2])/100
        HUM  = (reveive_data[5]*256 + reveive_data[4])/100
        if debug:
            print("TEMP: "+ str(TEMP))
            print("HUM: "+ str(HUM))
            print("------------------------------")
        #
    except:
        TEMP = 0
        HUM  = 0

    return TEMP,HUM

    


def GET_CO2():

    if debug:
        print("AA 55 B1 4E")
    #print(GENERAL_GET(GET_CO2_cmd))
    data = GENERAL_GET(GET_CO2_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_CO2_cmd,GET_CO2_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        CO2      = (reveive_data[3]*256 + reveive_data[2])
        AVE_CO2  = (reveive_data[5]*256 + reveive_data[4])
        if debug:
            print("CO2: "+ str(CO2))
            print("AVE_CO2: "+ str(AVE_CO2))
            print("------------------------------")
        #
    except:
        CO2      = 0
        AVE_CO2  = 0

    return CO2,AVE_CO2

def GET_TVOC():

    if debug:
        print("AA 55 B2 4D")
    #print(GENERAL_GET(GET_TVOC_cmd))
    data = GENERAL_GET(GET_TVOC_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_TVOC_cmd,GET_TVOC_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        TVOC           = (reveive_data[3]*256 + reveive_data[2])
        eCO2           = (reveive_data[5]*256 + reveive_data[4])
        S_H2           = (reveive_data[7]*256 + reveive_data[6])
        S_ETHANOL      = (reveive_data[9]*256 + reveive_data[8])
        BASELINE_TVOC  = (reveive_data[11]*256 + reveive_data[10])
        BASELINE_eCO2  = (reveive_data[13]*256 + reveive_data[12])
        if debug:
            print("TVOC: "+ str(TVOC))
            print("eCO2: "+ str(eCO2))
            print("S_H2: "+ str(S_H2))
            print("S_ETHANOL: "+ str(S_ETHANOL))
            print("BASELINE_TVOC: "+ str(BASELINE_TVOC))
            print("BASELINE_eCO2: "+ str(BASELINE_eCO2))
            print("------------------------------")
        #
        #please consider other value(baseline)
    except:
        TVOC           = 0
        eCO2           = 0
        S_H2           = 0
        S_ETHANOL      = 0
        BASELINE_TVOC  = 0
        BASELINE_eCO2  = 0

    TVOC_ALL = [TVOC,eCO2,S_H2,S_ETHANOL,BASELINE_TVOC,BASELINE_eCO2]
    
    return TVOC_ALL

def GET_LIGHT():

    if debug:
        print("AA 55 B3 4C")
    #print(GENERAL_GET(GET_LIGHT_cmd))
    data = GENERAL_GET(GET_LIGHT_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_LIGHT_cmd,GET_LIGHT_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Illuminance         = (reveive_data[3]*256 + reveive_data[2])
        ColorTemperature    = (reveive_data[5]*256 + reveive_data[4])
        CH_R                = (reveive_data[7]*256 + reveive_data[6])
        CH_G                = (reveive_data[9]*256 + reveive_data[8])
        CH_B                = (reveive_data[11]*256 + reveive_data[10])
        CH_C                = (reveive_data[13]*256 + reveive_data[12])
        if debug:
            print("Illuminance: "+ str(Illuminance))
            print("ColorTemperature: "+ str(ColorTemperature))
            print("CH_R: "+ str(CH_R))
            print("CH_G: "+ str(CH_G))
            print("CH_B: "+ str(CH_B))
            print("CH_C: "+ str(CH_C))
            print("------------------------------")
        #
    except:
        Illuminance         = 0
        ColorTemperature    = 0
        CH_R                = 0
        CH_G                = 0
        CH_B                = 0
        CH_C                = 0

    #return a LIST
    LIGHT = [Illuminance,ColorTemperature,CH_R,CH_G,CH_B,CH_C]
    return LIGHT

def GET_PMS():

    if debug:
        print("AA 55 B4 4B")
    #print(GENERAL_GET(GET_PMS_cmd))
    data = GENERAL_GET(GET_PMS_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_PMS_cmd,GET_PMS_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        PM1_AE   = (reveive_data[3]*256 + reveive_data[2])
        PM25_AE  = (reveive_data[5]*256 + reveive_data[4])
        PM10_AE  = (reveive_data[7]*256 + reveive_data[6])
        PM1_SP   = (reveive_data[9]*256 + reveive_data[8])
        PM25_SP  = (reveive_data[11]*256 + reveive_data[10])
        PM10_SP  = (reveive_data[13]*256 + reveive_data[12])
        if debug:
            print("PM1_AE: "+ str(PM1_AE))
            print("PM25_AE: "+ str(PM25_AE))
            print("PM10_AE: "+ str(PM10_AE))
            print("PM1_SP: "+ str(PM1_SP))
            print("PM25_SP: "+ str(PM25_SP))
            print("PM10_SP: "+ str(PM10_SP))
            print("------------------------------")
        #
    except:
        PM1_AE   = 0
        PM25_AE  = 0
        PM10_AE  = 0
        PM1_SP   = 0
        PM25_SP  = 0
        PM10_SP  = 0

    #return a LIST
    PMS = [PM1_AE,PM25_AE,PM10_AE,PM1_SP,PM25_SP,PM10_SP]
    return PMS
    
def GET_SENSOR_ALL():

    if debug:
        print("AA 55 B5 4A")
    #print(GENERAL_GET(GET_SENSOR_ALL_cmd))
    data = GENERAL_GET(GET_SENSOR_ALL_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_SENSOR_ALL_cmd,GET_SENSOR_ALL_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        TEMP                = (reveive_data[3]*256 + reveive_data[2])/100
        HUM                 = (reveive_data[5]*256 + reveive_data[4])/100
        CO2                 = (reveive_data[7]*256 + reveive_data[6])
        AVE_CO2             = (reveive_data[9]*256 + reveive_data[8])
        TVOC                = (reveive_data[11]*256 + reveive_data[10])
        eCO2                = (reveive_data[13]*256 + reveive_data[12])
        S_H2                = (reveive_data[15]*256 + reveive_data[14])
        S_ETHANOL           = (reveive_data[17]*256 + reveive_data[16])
        BASELINE_TVOC       = (reveive_data[19]*256 + reveive_data[18])
        BASELINE_eCO2       = (reveive_data[21]*256 + reveive_data[20])
        Illuminance         = (reveive_data[23]*256 + reveive_data[22])
        ColorTemperature    = (reveive_data[25]*256 + reveive_data[24])
        CH_R                = (reveive_data[27]*256 + reveive_data[26])
        CH_G                = (reveive_data[29]*256 + reveive_data[28])
        CH_B                = (reveive_data[31]*256 + reveive_data[30])
        CH_C                = (reveive_data[33]*256 + reveive_data[32])
        PM1_AE              = (reveive_data[35]*256 + reveive_data[34])
        PM25_AE             = (reveive_data[37]*256 + reveive_data[36])
        PM10_AE             = (reveive_data[39]*256 + reveive_data[38])
        PM1_SP              = (reveive_data[41]*256 + reveive_data[40])
        PM25_SP             = (reveive_data[43]*256 + reveive_data[42])
        PM10_SP             = (reveive_data[45]*256 + reveive_data[44])
        #
    except:
        TEMP                = 0
        HUM                 = 0
        CO2                 = 0
        AVE_CO2             = 0
        TVOC                = 0
        eCO2                = 0
        S_H2                = 0
        S_ETHANOL           = 0
        BASELINE_TVOC       = 0
        BASELINE_eCO2       = 0
        Illuminance         = 0
        ColorTemperature    = 0
        CH_R                = 0
        CH_G                = 0
        CH_B                = 0
        CH_C                = 0
        PM1_AE              = 0
        PM25_AE             = 0
        PM10_AE             = 0
        PM1_SP              = 0
        PM25_SP             = 0
        PM10_SP             = 0

    #passthis with LIST maybe?
    SENSOR_ALL = [TEMP,HUM,CO2,AVE_CO2,TVOC,eCO2,S_H2,S_ETHANOL,BASELINE_TVOC,BASELINE_eCO2,Illuminance,ColorTemperature,CH_R,CH_G,CH_B,CH_C,PM1_AE,PM25_AE,PM10_AE,PM1_SP,PM25_SP,PM10_SP]
    #SENSOR_ALL = [TEMP,HUM,CO2,AVE_CO2,TVOC,Illuminance,CH_R,CH_G,CH_B,CH_C,PM1_AE,PM25_AE,PM10_AE]
    
    return SENSOR_ALL

def GET_INFO_VERSION():

    if debug:
        print("AA 55 B6 49")
    #print(GENERAL_GET(GET_INFO_VERSION_cmd))
    data = GENERAL_GET(GET_INFO_VERSION_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_VERSION_cmd,GET_INFO_VERSION_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        VERSION = (reveive_data[3]*256 + reveive_data[2])
        if debug:
            print("VERSION: "+ str(VERSION))
            print("------------------------------")
        #
    except:
        VERSION = 0

    return VERSION

def GET_INFO_RUNTIME():

    if debug:
        print("AA 55 B7 48")
    #print(GENERAL_GET(GET_INFO_RUNTIME_cmd))
    data = GENERAL_GET(GET_INFO_RUNTIME_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_RUNTIME_cmd,GET_INFO_RUNTIME_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        RT_DAY   = (reveive_data[3]*256 + reveive_data[2])
        RT_HOUR  = (reveive_data[4])
        RT_MIN   = (reveive_data[5])
        RT_SEC   = (reveive_data[6])
        if debug:
            print("RT_DAY: "+ str(RT_DAY))
            print("RT_HOUR: "+ str(RT_HOUR))
            print("RT_MIN: "+ str(RT_MIN))
            print("RT_SEC: "+ str(RT_SEC))
            print("------------------------------")
        #
    except:
        RT_DAY   = 0
        RT_HOUR  = 0
        RT_MIN   = 0
        RT_SEC   = 0

    #return a LIST
    RUNTIME = [RT_DAY,RT_HOUR,RT_MIN,RT_SEC]
    return RUNTIME

def GET_INFO_ERROR_LOG():

    if debug:
        print("AA 55 B8 47")
    #print(GENERAL_GET(GET_INFO_ERROR_LOG_cmd))
    data = GENERAL_GET(GET_INFO_ERROR_LOG_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_ERROR_LOG_cmd,GET_INFO_ERROR_LOG_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        ERROR_TEMP_HUM  = (reveive_data[3]*256 + reveive_data[2])
        ERROR_CO2       = (reveive_data[5]*256 + reveive_data[4])
        ERROR_TVOC      = (reveive_data[7]*256 + reveive_data[6])
        ERROR_LIGHT     = (reveive_data[9]*256 + reveive_data[8])
        ERROR_PMS       = (reveive_data[11]*256 + reveive_data[10])
        ERROR_RTC       = (reveive_data[13]*256 + reveive_data[12])
        if debug:
            print("ERROR_TEMP_HUM: "+ str(ERROR_TEMP_HUM))
            print("ERROR_CO2: "+ str(ERROR_CO2))
            print("ERROR_TVOC: "+ str(ERROR_TVOC))
            print("ERROR_LIGHT: "+ str(ERROR_LIGHT))
            print("ERROR_PMS: "+ str(ERROR_PMS))
            print("ERROR_RTC: "+ str(ERROR_RTC))
            print("------------------------------")
        #
    except:
        ERROR_TEMP_HUM  = 0
        ERROR_CO2       = 0
        ERROR_TVOC      = 0
        ERROR_LIGHT     = 0
        ERROR_PMS       = 0
        ERROR_RTC       = 0

    ERROR_LOG = [ERROR_TEMP_HUM,ERROR_CO2,ERROR_TVOC,ERROR_LIGHT,ERROR_PMS,ERROR_RTC]
    return ERROR_LOG
    
def GET_INFO_SENSOR_POR():

    if debug:
        print("AA 55 B9 46")
    #print(GENERAL_GET(GET_INFO_SENSOR_POR_cmd))
    data = GENERAL_GET(GET_INFO_SENSOR_POR_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_SENSOR_POR_cmd,GET_INFO_SENSOR_POR_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        POR_TEMP_HUM  = (reveive_data[2])
        POR_CO2       = (reveive_data[3])
        POR_TVOC      = (reveive_data[4])
        POR_LIGHT     = (reveive_data[5])
        POR_PMS       = (reveive_data[6])
        POR_RTC       = (reveive_data[7])
        POLL_TEMP_HUM = (reveive_data[8])
        POLL_CO2      = (reveive_data[9])
        POLL_TVOC     = (reveive_data[10])
        POLL_LIGHT    = (reveive_data[11])
        POLL_PMS      = (reveive_data[12])
        POLL_RTC      = (reveive_data[13])
        #
    except:
        POR_TEMP_HUM  = 0
        POR_CO2       = 0
        POR_TVOC      = 0
        POR_LIGHT     = 0
        POR_PMS       = 0
        POR_RTC       = 0
        POLL_TEMP_HUM = 0
        POLL_CO2      = 0
        POLL_TVOC     = 0
        POLL_LIGHT    = 0
        POLL_PMS      = 0
        POLL_RTC      = 0

    SENSOR_POR = [POR_TEMP_HUM,POR_CO2,POR_TVOC,POR_LIGHT,POR_PMS,POR_RTC,POLL_TEMP_HUM,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC]
    return SENSOR_POR

def GET_RTC_DATE_TIME():

    if debug:
        print("AA 55 BA 45")
    #print(GENERAL_GET(GET_RTC_DATE_TIME_cmd))
    data = GENERAL_GET(GET_RTC_DATE_TIME_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_RTC_DATE_TIME_cmd,GET_RTC_DATE_TIME_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        RTC_YY  = (reveive_data[2])
        RTC_MM  = (reveive_data[3])
        RTC_DD  = (reveive_data[4])
        RTC_hh  = (reveive_data[5])
        RTC_mm  = (reveive_data[6])
        RTC_ss  = (reveive_data[7])
    #
    except:
        RTC_YY  = 0
        RTC_MM  = 0
        RTC_DD  = 0
        RTC_hh  = 0
        RTC_mm  = 0
        RTC_ss  = 0

    DATE_TIME = [RTC_YY,RTC_MM,RTC_DD,RTC_hh,RTC_mm,RTC_ss]
    return DATE_TIME

def GET_INFO_PIN_STATE():

    if debug:
        print("AA 55 BB 44")
    #print(GENERAL_GET(GET_INFO_PIN_STATE_cmd))
    data = GENERAL_GET(GET_INFO_PIN_STATE_cmd)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_PIN_STATE_cmd,GET_INFO_PIN_STATE_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        PIN_CO2_CAL       = (reveive_data[2])
        PIN_PMS_RESET     = (reveive_data[3])
        PIN_PMS_SET       = (reveive_data[4])
        PIN_NBIOT_PWRKEY  = (reveive_data[5])
        PIN_NBIOT_SLEEP   = (reveive_data[6])
        PIN_LED_CTRL      = (reveive_data[7])
        PIN_FAN_CTRL      = (reveive_data[8])
        #
    except:
        PIN_CO2_CAL       = 0
        PIN_PMS_RESET     = 0
        PIN_PMS_SET       = 0
        PIN_NBIOT_PWRKEY  = 0
        PIN_NBIOT_SLEEP   = 0
        PIN_LED_CTRL      = 0
        PIN_FAN_CTRL      = 0

    PIN_STATE = [PIN_CO2_CAL,PIN_PMS_RESET,PIN_PMS_SET,PIN_NBIOT_PWRKEY,PIN_NBIOT_SLEEP,PIN_LED_CTRL,PIN_FAN_CTRL]
    return PIN_STATE


#===============SET COMMAND===============#
#display like 0x00 type
#data = bytearray(b'hello')
#print("".join("\\x%02x" % i for i in data))

def SET_STATUS_LED(state):

    if debug:
        #STATUS_LED state 0: LED off / 1: LED on / 2~65534:Pulse time length (ms)
        print("AA 55 BF 40 00 00 su ~s")
    #print(LED_SET(SET_STATUS_LED_cmd,state)) #there is no key for SET_STATUS_LED 
    data = LED_SET(SET_STATUS_LED_cmd,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())

    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_STATUS_LED_cmd,SET_STATUS_LED_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0

    return RESULT


def SET_PIN_CO2_CAL(state):

    if debug:
        #CO2_CAL state default:1 / set to 0 to calibrate CO2
        print("AA 55 C0 3F 53 38 4C 50 01 su ~s")
    #print(GENERAL_SET(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_key,state))
    data = GENERAL_SET(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_key,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT


def SET_PIN_PMS_RESET(state):

    if debug:
        #PMS_RESET state default:1 / set to 0 to reset PM_sensor
        print("AA 55 C1 3E 50 4D 53 33 01 su ~s")
    #print(GENERAL_SET(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_key,state))
    data = GENERAL_SET(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_key,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT


def SET_PIN_PMS_SET(state):

    if debug:
        #PMS_SET state default:1 / set to 0 to disable PM_sensor
        print("AA 55 C2 3D 33 30 30 33 01 su ~s")
    #print(GENERAL_SET(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_key,state))
    data = GENERAL_SET(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_key,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())
        
    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT
    

def SET_PIN_NBIOT_PWRKEY(state):

    if debug:
        print("AA 55 C3 3C 4E 42 4C 2D 49 su ~s")
    #print(GENERAL_SET(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_key,state))
    data = GENERAL_SET(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_key,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT


def SET_PIN_NBIOT_SLEEP(state):

    if debug:
        print("AA 55 C4 3B 2D 49 4F 54 01 su ~s")
    #print(GENERAL_SET(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_key,state))
    data = GENERAL_SET(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_key,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT


def SET_PIN_LED_ALL(state):

    if debug:
        #PIN_LED state default:1 / set to 0 to turnoff all LED
        print("AA 55 C5 3A 53 4C 45 44 01 su ~s")
    #print(GENERAL_SET(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_key,state))
    data = GENERAL_SET(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_key,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT


def SET_POLLING_SENSOR(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC):

    if debug:
        print("AA 55 C6 39 00 00 00 00 00 00 su ~s")
    #print(POLLING_SET(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC))
    data = POLLING_SET(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_POLLING_SENSOR_cmd,SET_POLLING_SENSOR_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT
    

def SET_RTC_DATE_TIME(YY,MM,DD,hh,mm,ss):

    if debug:
        print("AA 55 C7 38 00 01 01 00 00 00 su ~s")
    #print(RTC_SET(YY,MM,DD,hh,mm,ss))
    data = RTC_SET(YY,MM,DD,hh,mm,ss)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_RTC_DATE_TIME_cmd,SET_RTC_DATE_TIME_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    #add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT

def SET_PIN_FAN_ALL(state):

    if debug:
        print("AA 55 C8 37 46 41 4E 63 01 su ~s")
    #print(GENERAL_SET(SET_PIN_FAN_ALL_cmd,SET_PIN_FAN_ALL_key,state))
    data = GENERAL_SET(SET_PIN_FAN_ALL_cmd,SET_PIN_FAN_ALL_key,state)
    if debug:
        print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_FAN_ALL_cmd,SET_PIN_FAN_ALL_resp)
    if debug:
        print(reveive_data)
        print("".join("%02x " % i for i in reveive_data).upper())

    ##add exception
    try:
        Leading   = (reveive_data[0])
        Command   = (reveive_data[1])
        RESULT    = (reveive_data[2])
    #
    except:
        Leading   = 0
        Command   = 0
        RESULT    = 0
        
    return RESULT


#===============PROTOCOL COMMAND===============#


def PROTOCOL_I2C_WRITE(i2c_address,i2c_data,freq = 0):
    cmd = PROTOCOL_I2C_WRITE_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #i2c frequency (0~4) (0:no change/1:400Khz/2:200Khz/3:100Khz/4:50Khz)
    host_send.append(freq)
    #i2c address(0~127)
    host_send.append(i2c_address)
    #i2c data length
    host_send.append(len(i2c_data))
    #i2c data(N-byte bytearray)
    host_send.extend(i2c_data)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send

def PROTOCOL_I2C_READ(i2c_address,i2c_read_length,freq = 0):
    cmd = PROTOCOL_I2C_READ_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose i2c frequency (0~4) (0:no change/1:400Khz/2:200Khz/3:100Khz/4:50Khz)
    host_send.append(freq)
    #set i2c address(0~127)
    host_send.append(i2c_address)
    #set i2c data read length(1~32)
    host_send.append(i2c_read_length)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def PROTOCOL_UART_BEGIN(UART_PORT,BAUD = 0,FORMAT = 0):
    cmd = PROTOCOL_UART_BEGIN_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    #set baudrate (0~4) (0:9600/1:19200/2:38400/3:57600/4:115200)
    host_send.append(BAUD)
    #set UART format (0~5) (0:N81/1:N71/2:E81/3:E71/4:O81/5:O71)
    host_send.append(FORMAT)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send

    
def PROTOCOL_UART_TX_RX(UART_PORT,TX_DATA,RX_LENGTH,TIMEOUT):
    #TX_DATA_length : 2 Byte / RX_LENGTH : 2 Byte / TIMEOUT : 2 Byte
    cmd = PROTOCOL_UART_TX_RX_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    
    #UART TX data length (TX_DATA is bytearray)
    TX_DATA_length = convert_2_byte(len(TX_DATA))
    host_send.extend(TX_DATA_length)
    
    #recive length of RX data
    RX_LENGTH = convert_2_byte(RX_LENGTH)
    host_send.extend(RX_LENGTH)
    
    #timeout time for RX data
    TIMEOUT = convert_4_byte(TIMEOUT)
    host_send.extend(TIMEOUT)

    #UART TX data 
    host_send.extend(TX_DATA)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def PROTOCOL_UART_TXRX_EX(UART_PORT,TX_DATA,BYTE_TIMEOUT,WAIT_TIMEOUT):
    #TX_DATA_length : 2 Byte / BYTE_TIMEOUT : 1 Byte / WAIT_TIMEOUT : 2 Byte
    cmd = PROTOCOL_UART_TXRX_EX_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    #UART TX data length (TX_DATA is bytearray)
    TX_DATA_length = convert_2_byte(len(TX_DATA))
    host_send.extend(TX_DATA_length)
    #BYTE_TIMEOUT :相鄰BYTE間隔時間的最大值 數值設為0 定義為 0.5ms
    host_send.append(BYTE_TIMEOUT)
    #WAIT_TIMEOUT :接收RX_DATA 的TIMEOUT 數值範圍 0~600000ms
    WAIT_TIMEOUT = convert_4_byte(WAIT_TIMEOUT)
    host_send.extend(WAIT_TIMEOUT)
    
    #UART TX data 
    host_send.extend(TX_DATA)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))

    return host_send


def ENABLE_UART_ACTIVE_RX(UART_PORT,ENABLE,POLLING_TIME,BYTE_TIMEOUT,RCV_TIMEOUT):
    #TRCV_TIMEOUT : 2 Byte
    cmd = ENABLE_UART_ACTIVE_RX_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    #UART ENABLE
    host_send.append(ENABLE)
    #POLLING_TIME
    host_send.append(POLLING_TIME)
    #BYTE_TIMEOUT :相鄰BYTE間隔時間的最大值 數值設為0 定義為 0.5ms
    host_send.append(BYTE_TIMEOUT)
    #RCV_TIMEOUT 
    RCV_TIMEOUT = convert_2_byte(RCV_TIMEOUT)
    host_send.extend(RCV_TIMEOUT)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))


    return host_send


##
##
###===============TEST ALL ===============#
##print("START")
##ser=serial.Serial("COM57",115200,timeout=1)
##time.sleep(5)
##
###===============TEST GET===============#
##
##print("===============TEST GET===============\n")
##
##print("GET_TEMP_HUM:")
##print(GET_TEMP_HUM())
##print("\n")
##
##print("GET_CO2:")
##print(GET_CO2())
##print("\n")
##
##print("GET_TVOC:")
##print(GET_TVOC())
##print("\n")
##
##print("GET_LIGHT:")
##print(GET_LIGHT())
##print("\n")
##
##print("GET_PMS:")
##print(GET_PMS())
##print("\n")
##
##print("GET_SENSOR_ALL:")
##print(GET_SENSOR_ALL())
##print("\n")
##
##print("GET_INFO_VERSION:")
##print(GET_INFO_VERSION())
##print("\n")
##
##print("GET_INFO_RUNTIME:")
##print(GET_INFO_RUNTIME())
##print("\n")
##
##print("GET_INFO_ERROR_LOG:")
##print(GET_INFO_ERROR_LOG())
##print("\n")
##
##print("GET_INFO_SENSOR_POR:")
##print(GET_INFO_SENSOR_POR())
##print("\n")
##
##print("GET_RTC_DATE_TIME:")
##print(GET_RTC_DATE_TIME())
##print("\n")
##
##print("GET_INFO_PIN_STATE:")
##print(GET_INFO_PIN_STATE())
##print("\n")
##
###===============TEST SET===============#
##
##print("===============TEST SET===============\n")
##
##print("SET_STATUS_LED:")
##print(SET_STATUS_LED(0))
##print(SET_STATUS_LED(1))
###SET_STATUS_LED(2567)
##print("\n")
##
##print("SET_PIN_CO2_CAL:")
##print(SET_PIN_CO2_CAL(0))
##print(SET_PIN_CO2_CAL(1))
##print("\n")
##
##print("SET_PIN_PMS_RESET:")
##print(SET_PIN_PMS_RESET(0))
##print(SET_PIN_PMS_RESET(1))
##print("\n")
##
##print("SET_PIN_PMS_SET:")
##print(SET_PIN_PMS_SET(0))
##print(SET_PIN_PMS_SET(1))
##print("\n")
##
##print("SET_PIN_NBIOT_PWRKEY:")
##print(SET_PIN_NBIOT_PWRKEY(0))
##print(SET_PIN_NBIOT_PWRKEY(1))
##print("\n")
##
##print("SET_PIN_NBIOT_SLEEP:")
##print(SET_PIN_NBIOT_SLEEP(0))
##print(SET_PIN_NBIOT_SLEEP(1))
##print("\n")
##
##print("SET_PIN_LED_ALL:")
##print(SET_PIN_LED_ALL(0))
##print(SET_PIN_LED_ALL(1))
##print("\n")
##
##print("SET_POLLING_SENSOR:")
##print(SET_POLLING_SENSOR(1,1,1,1,1,1))
##print("\n")
##
##print("SET_RTC_DATE_TIME:")
##print(SET_RTC_DATE_TIME(0,1,1,0,0,0))
##print("\n")
##
##print("SET_PIN_FAN_ALL:")
##print(SET_PIN_FAN_ALL(0))
##print(SET_PIN_FAN_ALL(1))
##print("\n")
##
###===============TEST PROTOCOL===============#
##
##print("===============TEST PROTOCOL===============\n")
##
###i2c_address,i2c_data
##i2c_address = 0X3C
##
##UART_PORT = 0
##BAUD = 0
##i2c_data = bytearray([0X01,0X02,0X03,0X04])
##TX_DATA = bytearray([0X01,0X02,0X03,0X04])
##
##i2c_read_length = len(i2c_data)
##RX_LENGTH = 5
##TIMEOUT = 0
##WAIT_TIMEOUT = 5
##ENABLE = 1
##POLLING_TIME = 0
##BYTE_TIMEOUT = 10
##RCV_TIMEOUT = 15
##
##print("PROTOCOL_I2C_WRITE:")
##print("AA 55 CA 35 00 3C 04 01 02 03 04 su ~s")
##data = PROTOCOL_I2C_WRITE(i2c_address,i2c_data)
##print("".join("%02x " % i for i in data).upper())
##print("\n")
##
##
##print("PROTOCOL_I2C_READ:")
##print("AA 55 CB 34 00 3C 04 su ~s")
##data = PROTOCOL_I2C_READ(i2c_address,i2c_read_length)
##print("".join("%02x " % i for i in data).upper())
##print("\n")
##
##
##print("PROTOCOL_UART_BEGIN:")
##print("AA 55 CC 33 00 00 00 su ~s")
##data = PROTOCOL_UART_BEGIN(UART_PORT,BAUD)
##print("".join("%02x " % i for i in data).upper())
##print("\n")
##
##
##print("PROTOCOL_UART_TX_RX:")
##print("AA 55 CD 32 00 00 04 00 05 00 00 00 00 01 02 03 04 su ~s")
##data = PROTOCOL_UART_TX_RX(UART_PORT,TX_DATA,RX_LENGTH,TIMEOUT)
##print("".join("%02x " % i for i in data).upper())
##print("\n")
##
##
##print("PROTOCOL_UART_TXRX_EX:")
##print("AA 55 CE 31 00 00 04 0A 00 00 00 05 01 02 03 04 su ~s")
##data = PROTOCOL_UART_TXRX_EX(UART_PORT,TX_DATA,BYTE_TIMEOUT,WAIT_TIMEOUT)
##print("".join("%02x " % i for i in data).upper())
##print("\n")
##
##
##print("ENABLE_UART_ACTIVE_RX:")
##print("AA 55 CF 30 00 01 00 0A 00 0F su ~s")
##data = ENABLE_UART_ACTIVE_RX(UART_PORT,ENABLE,POLLING_TIME,BYTE_TIMEOUT,RCV_TIMEOUT)
##print("".join("%02x " % i for i in data).upper())
##print("\n")
##
##
###ser=serial.Serial("COM11",115200,timeout=0.5)
##
##ser.close()
##print("OK")




























