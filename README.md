# Simple client - server chat with Docker and Python

This simple example will show how to host one server and two clients and chat via the clients using the server.

## Setting up

Simply run `docker compose build` to build the containers

## Run the chat

First start the server from a terminal (cmd.exe, powershell, Linux/Mac terminal)

```shell
  docker compose up 
```

Then open another command shell for the first chat-party and run 
```shell
  docker attach chat_client_1
```

Repeat for the second chat-party open another shell and run

```shell
  docker attach chat_client_1
```

Now start typing in last two and see how the chat is taking place.

# Using Wireshark to listen in on the conversation

Install and run Wireshark (as admin/sudo). Find the network card created for Docker:
```shell
  docker exec -it chat_server cat /sys/class/net/eth0/iflink
  153
```

This number `153` should match an interface on your host. For Linux:
```shell
  ip addr | grep 153
```

Yields something like:
```text
  153: vethbc5b317@if152: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-03669f8067d9 state UP group default 
```

Notice the text `vethbc5b317`. In Wireshark this interface should be present in the list with interfaces:

![Wireshark-01.png](images/Wireshark-01.png)

In the image above the correct interface is highlighted in blue. Just double click on this interface and start typing. 

# Security implications

1. the person maintaining the server can see all
2. using Wireshark we see that the messages are unencrypted so anyone can listen in
