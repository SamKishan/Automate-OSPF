The aim of network automation is to minimize the effort required and decrease the chance of human error which is one of the leading causes of network downtime. 
While using information from configuration files and deploying routine configurations onto multiple network devices is a step towards automation, this approach can be made more dynamic. Creating an interface that automates configuration from minimal user input simplifies the process, does not require the end user to know vendor-specific CLI commands, and ultimately reduces the possibility of misconfigurations. 

This network was simulated using GNS3. The routers have static routes installed on them in the beginning so that they can be sshed into. To enable ssh on cisco routers, follow the instructions provided here https://www.pluralsight.com/blog/tutorials/configure-secure-shell-ssh-on-cisco-router. These programs make use of netmiko as the module which lets you execute commands on the routers remotely. 

For best efficiency, configure routers in the order R1,R2,R4, and R3.

For more information, email me at saki8093@colorado.edu
