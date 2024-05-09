# On Demand SDN Slices
![Topology](/images/topo2.png) 


## Section links
- [Project Description](#Project-Description)
- [Link](#Link)
- [Implementation Details](#Implementation-Details)
- [Project Layout](#Project-Layout)
- [Installation](#Installation)
- [Demo](#Demo)
- [Contacts](#Contacts)

## Project Description

This is the project of the Softwarized and Virtualized Mobile Networks course of the University of Trento.
The main goal of this project is to implement a network slicing approach to enable dynamic activation/de-activation of network slices via CLI/GUI commands.
On demand means that he user can activate and deactivate different slices.


## Link

[**Presentation Link**](https://docs.google.com/presentation/d/1hqmH79rsrdqUngCE98Dunrr3GfWYEA-AQCRVIK0HSg8/edit#slide=id.g2d9d05aa730_0_121)

[**Demo Link**](link demo) 

## Implementation Details
**ENVIRONMENT:**

This project makes substantial use of ComNetsEmu and Mininet. ComNetsEmu is a tested and network emulator designed for the NFV/SDN teaching book "Computing in Communication Networks: From Theory to Practice". The design focuses on emulating all the applications on a single computer. ComNetsEmu extends the famous Mininet network emulator. Mininet creates a realistic virtual network, running real kernel, switch and application code, on a single machine. The programming language used is Python. The project was developed in a dedicated virtual machine with Linux operating system.

**NETWORK DESCRIPTION:**

The network is made up of 2 routers connected together, and 6 hosts, the first 3 connected to the first router, the other three connected to the second one.
The network is designed to work in 3 different configurations: common, sos and custom. Each configuration has its own characteristics in terms of slicing (1, 2 or 3 slices) and capacity (the total capacity of 10 Mbps is divided differently depending on the network configuration in use)

**SLICING:**

- common_scenario: 2 slices (h1, h4) and (h2, h5) are active and the network capacity is divided equally, so each slice has 5 Mbps

- sos_scenario: all 3 slices (h1, h4), (h2, h5) and (h3, h6) are active.
The network capacity is divided as follows: 3 Mbps for the first slice, 3 Mbps for the second, 4 Mbps for the third.

- custom_scenario: in this case only one slice is active. The user can choose which one to activate. All network capacity (10 Mbps) is dedicated to the active slice.

**CLI:**

a command line interface allows the user to choose which mode to use between normal, sos and custom.
![Topology](/images/menu.png) 



**SLICING VISUALIZATION:**

Every time the user changes mode, a web server is automatically started which graphically displays the network topology and active slices.
![Topology](/images/server.png) 

When the server is acrive, it is available here:
```
http://localhost:8080
```

Note: the web server is designed to receive only one request and then it is automatically stopped, so as not to stop the execution of the main program by remaining continuously running.


## Project Layout
![Project Layout](/images/tree.png)


**my_network.py:** is the file that define the network topology;

**common_scenario.sh:** script that creates 2 slices to enable the communication between (h1, h4) and (h2, h5);

**sos_scenario.sh:** script that creates 3 slices to enable the communication between (h1, h4) , (h2, h5) and (h3, h6);

**custom_scenario.sh:** script that creates 1 slice. The user can choose, using the CLI, which slice to activate in order to enable the communication between (h1, h4) or (h2, h5) or (h3, h6);

**emergency_slicing.py:** via CLI, the user can select which scenario to activate among the 3 just mentioned and the network slicing will be performed accordingly;

**print_network.py:** allows you to view the active topology via the web.

**run.py:** and **Makefile:** are used for the execution of the project. Details will be discussed later.


## Installation
You can run this project by following this steps:
1. Install comnetsemu using VirtualBox (option A) at this [link](https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs)

2. download this project via git commands. Then, open 2 terminals in this directory:

```
cd /home/comnetsemu/comnetsemu/app/realizing_network_slicing/NetworkSlicing/code
```

3. In the first terminal:

```
make
```
This terminal can be used to perform mininet command like:
```
pingall
```
or:
```
iperf <hostA> <hostB>
```


Note 1: You may need to enter your comnetsemu password (default is "comnetsemu").

Note 2: the common scenario starts by default.

4. In the second terminal:

```
python3 run.py
```
This terminal shows the CLI for choosing the desired mode

## Demo

Questa sezione spiegherà un esempio di utilizzo completo di questa applicazione.
Supponiamo di aver gia eseguito l'installazione e di avere 2 terminali aperti  (come spiegato nella sezione precedente).

| Firts terminal                                                                     | Second terminal                                     |
|------------------------------------------------------------------------------------|-----------------------------------------------------|
|  1. Run: ```make```                                   |  2. Run: ```python3 run.py```. The CLI will appear  ![menu](/images/menu.png)
|  4. Run diagnostic commands, such as ```pingall``` or ```iperf h1 h4```                                                |  3. Scegliere una modalità, ad esempio:   ```1```. A web browser will appear to graphically display the active slices based on the chosen mode                                                           |
|  ![ping](/images/ping1.png)  ![iperf](/images/iperf1.png)        |    ![topo](/images/topo1.png)         |       
|5. Repeat steps 3 and 4 to test all modes|      |                                          
|6. Close mininet: ```exit``` | Chiudere la CLI con l'opzione:  ```4``` |
       

Note 1: Theiperf host1 host2 command will not give any results if executed with two hosts which, based on the active slices and the network topology, cannot communicate with each other. You will need to stop it manually with Ctrl+C

Note 2: pingall wastes time trying to get all hosts to communicate with each other: the following command is an alternative to test communication between 2 hosts:
```<host1> ping <host2>```

## Contacts

Riccardo Zannoni - riccardo.zannoni@studenti.unitn.it