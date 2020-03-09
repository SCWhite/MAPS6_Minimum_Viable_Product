import os
import PI_test_config as Conf
from datetime import datetime

#This function is dasable for MVP version
#doesn't support USB drive hot-plugging
def GET_STORAGE_PATH():

    # try:
    #     if len(os.listdir("/media/pi")):
    #         path = "/media/pi/" + os.listdir("/media/pi")[0]

    #         return path

    # except:
    #     path = Conf.FS_SD

    #     return path

    #only use
    path = Conf.FS_SD
    return path

def save_data(path,data_list):
    
    #CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
    CSV_msg = ""
    
    pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    #values["date"] = pairs[0]
    #values["time"] = pairs[1]

    for i in range(len(data_list)):
        CSV_msg = CSV_msg + str(data_list[i]) + ','
        
    CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data
    
    # #no you can't do this / please fix, consider USB drive and native SD slot
    # if not os.path.isdir(path):
    #     os.mkdir(path)

    with open(path + "/" + pairs[0] + ".csv", "a") as f:
       f.write(CSV_msg + "\n")


# def storage():

#     #This function is dasable for MVP version
#     #doesn't support USB drive hot-plugging

#     # if len(os.listdir("/media/pi")):
#     #     path = "/media/pi/" + os.listdir("/media/pi")[0]

#     # else:
#     #     path = Conf.FS_SD

#     #only use
#     path = Conf.FS_SD

#     #CSV_items =  ['device_id', 'date', 'time', 'Tmp',  'RH',   'PM2.5','PM10', 'PM1.0','RGB_R','RGB_G','RGB_B','RGB_C','Lux',  'CO2',  'TVOC']
#     #CSV_type  =  ['string',    'date', 'time', 'float','float','int',  'int',  'int',  'int',  'int'  ,'int',  'int',  'int',  'int',  'int' ]
#     CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
#     CSV_msg = ""

#     pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
#     values["date"] = pairs[0]
#     values["time"] = pairs[1]

#     for item in CSV_items:
#         if item in values:
#             CSV_msg = CSV_msg + str(values[item]) + ','
#         else:
#             CSV_msg = CSV_msg + "N/A" + ','
#     CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data

#     #color.print_p("CSV_MSG:")
#     #print(CSV_msg)

#     with open(path + "/" + values["date"] + ".csv", "a") as f:
#         f.write(CSV_msg + "\n")


def upload():
    restful_str = "wget -O /tmp/last_upload.log \"" + Conf.Restful_URL + "topic=" + Conf.APP_ID + "&device_id=" + Conf.DEVICE_ID + "&key=" + Conf.SecureKey + "&msg=" + msg + "\""

    color.print_p("restful_str:")
    print(restful_str)

    os.system(restful_str)
