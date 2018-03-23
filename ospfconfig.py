import sys
from netmiko import ConnectHandler
from prettytable import PrettyTable
nbr_table=PrettyTable()
nbr_table.field_names=["Neighbor ID","State","Interface"]

def conf_ospf(physical_ip, loopback_ip,process_id,router_id,area_id,username,password,router_number):
    print("Inside the function now")
    router= {
    'device_type':'cisco_ios',
    'ip':str(physical_ip),
    'username':str(username),
    'password':str(password),
    'global_delay_factor':3,
}

    '''print("set the router parameters")
    print("physical ip:"+str(physical_ip))
    print("loopback ip:"+str(loopback_ip))
    print("process id:"+str(process_id))
    print("router id:"+str(router_id))
    print("area_id:"+str(area_id))
    print("username:"+str(username))
    print("password:"+str(password))
    print("router number:"+str(router_number))'''  

    commands=["router ospf "+str(process_id),"router-id "+router_id,"network "+loopback_ip+" 0.0.0.0 area "+str(area_id)]
    if(router_number==1):
        print("opening ospf_r1.conf")
        with open("ospf_r1.conf") as f:
            for line in f:
                commands.append(line)

    elif(router_number==2):
        with open("ospf_r2.conf") as f:
            for line in f:
                commands.append(line)
   
    elif(router_number==3):
        with open("ospf_r3.conf") as f:
            for line in f:
                commands.append(line)
   
    elif(router_number==4):
        with open("ospf_r4.conf") as f:
            for line in f:
                commands.append(line)
    print("Commands to be executed")
    for l in range(len(commands)):
        print(commands[l])  
    net_connect=ConnectHandler(**router)
    output=net_connect.send_config_set(commands)
    
def ospf_neighbhor(physical_ip,username,password,router_number):
    router= {
    'device_type':'cisco_ios',
    'ip':str(physical_ip),
    'username':str(username),
    'password':str(password),
    'global_delay_factor':3,
    }
    
    neighbors_command=["do show ip ospf neighbor"]
    net_connect=ConnectHandler(**router)
    neighbors=net_connect.send_config_set(neighbors_command)
    f=open("nbr_details.txt","w")
    f.write(neighbors)
    f.close()
    nbr_table.clear_rows()
    with open("nbr_details.txt") as f:
        for line in f:
            components=line.split()
            if(len(components)>3 and ("Neighbor" not in components[0]) and "Fast" in line):
                print("comp_0:"+components[0])
                print("comp_2:"+components[2])
                print("comp_5:"+components[5])
                nbr_table.add_row([components[0],components[2],components[5]])                        
    print(nbr_table)
    data=nbr_table.get_string()
    with open("nbr_router"+str(router_number)+".txt","wb") as f:
        f.write(data)
    
def ospf_ping(r1_user,r1_pass,r1_ip,r2_user,r2_pass,r2_ip):
    r1= {
    'device_type':'cisco_ios',
    'ip':str(r1_ip),
    'username':str(r1_user),
    'password':str(r1_pass),
    'global_delay_factor':3,
    }
   

    r2= {
    'device_type':'cisco_ios',
    'ip':str(r2_ip),
    'username':str(r2_user),
    'password':str(r2_pass),
    'global_delay_factor':3,
    }
    print("Router 1")
    cmd_r1="do show ip int brief"
    net_connect_r1=ConnectHandler(**r1) 
    lo_r1=net_connect_r1.send_config_set(cmd_r1)
    f=open("lo_r1.txt","w")
    f.write(lo_r1)
    f.close()
    with open("lo_r1.txt") as f:
        for line in f:
            comps=line.split()
            if("Loop" in comps[0]):
                loip_r1=comps[1]
    print("Router 2")
    cmd_r2="do show ip int brief"
    net_connect_r2=ConnectHandler(**r2) 
    lo_r2=net_connect_r2.send_config_set(cmd_r2)
    f=open("lo_r2.txt","w")
    f.write(lo_r2)
    f.close()
    with open("lo_r2.txt") as f:
        for line in f:
            comps=line.split()
            if("Loop" in comps[0]):
                loip_r2=comps[1]
    print("pinging")
    ping_r1="do ping "+str(loip_r2)
    ping_r1=net_connect_r1.send_config_set(ping_r1)
    ping_r2="do ping "+str(loip_r1)
    ping_r2=net_connect_r2.send_config_set(ping_r2)
    print("\n\n\nOutput from R1:")
    print(ping_r1)
    print("\n\n\nOutput from R2:")
    print(ping_r2)
    if("0/5" not in ping_r1 and "0/5" not in ping_r1):
        return 1
    else:
        return 0
 
    
   
    
