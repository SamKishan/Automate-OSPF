import sys
try:
    import collections
    import os
    from netmiko import ConnectHandler
    import time
    from prettytable import PrettyTable
    import sshInfo
    import validateIP
    import connectivity
    import configparser
    from time import gmtime, strftime
    from threading import Thread
except TypeError:
    print("Import Error")
    sys.exit()
def retreive_conf(list_dict,i,commands,router_ids,filename):
    print("-----------------------------------------------")
    net_connect=ConnectHandler(**list_dict[i])
    output=net_connect.send_config_set(commands)
    print("exexexexexexexexexexexexexex")
    #filename=router_ids[i]+strftime("%Y-%m-%d_%H:%M:%S", gmtime())+".txt"
    f=open(filename,"w")
    print("Writing to file: "+filename)
    f.write(output)
    time.sleep(25) 
def getconf():
    a=sshInfo.func()
    status=validateIP.checkip(a)
    connection=connectivity.connectivity(status)
    print("a:")
    print(a)
    config=configparser.ConfigParser()
    config.read('test.conf')
    routers=config.sections()
    list_dict=[]

    for i in range(len(routers)):
        list_dict.append({
        'device_type':config[routers[i]]['device_type'],
        'ip':config[routers[i]]['ip'],
        'username':config[routers[i]]['username'],
        'password':config[routers[i]]['password'],
        'global_delay_factor':float(config[routers[i]]['global_delay_factor']),
    })

    commands=["do show run"]
    router_ids=config.sections()
    filenames=[]
    for i in range(len(list_dict)):
        filenames.append(router_ids[i]+strftime("%Y-%m-%d_%H:%M:%S", gmtime())+".txt")
        t=Thread(target=retreive_conf,args=(list_dict,i,commands,router_ids,filenames[i]))
        t.start()   
    time.sleep(50)
    ret="<html><body>The files are created. <br>Their names are<br>"
    for k in range(len(filenames)):
        ret+=str(k+1)+". "+filenames[k]+"<br>"
    ret+="<br><br> <a href=/> Go Back?</a> </body></html>"
    return ret
