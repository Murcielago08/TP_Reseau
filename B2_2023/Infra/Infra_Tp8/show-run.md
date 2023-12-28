# Conf Show-run équipement réseaux

# Sommaire

- [Conf Show-run équipement réseaux](#conf-show-run-équipement-réseaux)
- [Sommaire](#sommaire)
- [🍷 Site "Meow Origins"](#-site-meow-origins)
  - [RC conf](#rc-conf)
  - [E1 conf](#e1-conf)
  - [E2 conf](#e2-conf)
  - [E3 conf](#e3-conf)
  - [SSV conf](#ssv-conf)
  - [IOU3 conf](#iou3-conf)
  - [IOU4 conf](#iou4-conf)
  - [IOU1 conf](#iou1-conf)
  - [IOU2 conf](#iou2-conf)
  - [R1 conf](#r1-conf)
  - [DHCP conf](#dhcp-conf)
  - [DNS conf](#dns-conf)
- [🚀 Site "Meow and Beyond"](#-site-meow-and-beyond)
  - [Bâtiment 1](#bâtiment-1)
    - [SSVB1 conf](#ssvb1-conf)
    - [RCB1 conf](#rcb1-conf)
    - [B1 conf](#b1-conf)
    - [DHCP conf](#dhcp-conf-1)
  - [Bâtiment 2](#bâtiment-2)
    - [B2 conf](#b2-conf)
  - [IOU10 conf](#iou10-conf)
  - [R2 conf](#r2-conf)

# 🍷 Site "Meow Origins"

## RC conf

```
RC#sh run
Building configuration...

Current configuration : 2053 bytes
!
! Last configuration change at 14:09:23 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname RC
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport access vlan 30
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 30
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 30
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 60
 switchport mode access
!
interface Ethernet1/2
 switchport access vlan 60
 switchport mode access
!
interface Ethernet1/3
 switchport access vlan 60
 switchport mode access
!
interface Ethernet2/0
 switchport access vlan 40
 switchport mode access
!
interface Ethernet2/1
!
interface Ethernet2/2
 switchport access vlan 50
 switchport mode access
!
interface Ethernet2/3
 switchport access vlan 40
 switchport mode access
!
interface Ethernet3/0
 switchport access vlan 40
 switchport mode access
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## E1 conf

```
E1#sh run
Building configuration...

Current configuration : 2155 bytes
!
! Last configuration change at 14:09:23 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname E1
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport access vlan 30
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 30
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 10
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 10
 switchport mode access
!
interface Ethernet1/2
 switchport access vlan 40
 switchport mode access
!
interface Ethernet1/3
 switchport access vlan 50
 switchport mode access
!
interface Ethernet2/0
 switchport access vlan 50
 switchport mode access
!
interface Ethernet2/1
 switchport access vlan 40
 switchport mode access
!
interface Ethernet2/2
 switchport access vlan 60
 switchport mode access
!
interface Ethernet2/3
 switchport access vlan 60
 switchport mode access
!
interface Ethernet3/0
 switchport access vlan 60
 switchport mode access
!
interface Ethernet3/1
 switchport access vlan 60
 switchport mode access
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## E2 conf

```
E2#sh run
Building configuration...

Current configuration : 2806 bytes
!
! Last configuration change at 14:09:25 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname E2
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport access vlan 20
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 20
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 20
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 30
 switchport mode access
!
interface Ethernet1/2
 switchport access vlan 30
 switchport mode access
!
interface Ethernet1/3
 switchport access vlan 10
 switchport mode access
!
interface Ethernet2/0
 switchport access vlan 10
 switchport mode access
!
interface Ethernet2/1
 switchport access vlan 40
 switchport mode access
!
interface Ethernet2/2
 switchport access vlan 40
 switchport mode access
!
interface Ethernet2/3
 switchport access vlan 50
 switchport mode access
!
interface Ethernet3/0
 switchport access vlan 50
 switchport mode access
!
interface Ethernet3/1
 switchport access vlan 60
 switchport mode access
!
interface Ethernet3/2
 switchport access vlan 60
 switchport mode access
!
interface Ethernet3/3
 switchport access vlan 60
 switchport mode access
!
interface Ethernet4/0
 switchport access vlan 60
 switchport mode access
!
interface Ethernet4/1
 switchport access vlan 60
 switchport mode access
!
interface Ethernet4/2
 switchport access vlan 60
 switchport mode access
!
interface Ethernet4/3
 switchport access vlan 60
 switchport mode access
!
interface Ethernet5/0
 switchport access vlan 60
 switchport mode access
!
interface Ethernet5/1
 switchport access vlan 60
 switchport mode access
!
interface Ethernet5/2
 switchport access vlan 30
 switchport mode access
!
interface Ethernet5/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## E3 conf

```
E3#sh run
Building configuration...

Current configuration : 1747 bytes
!
! Last configuration change at 14:09:23 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname E3
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport access vlan 40
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 40
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 50
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 50
 switchport mode access
!
interface Ethernet1/2
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## SSV conf

```
SSV#sh run
Building configuration...

Current configuration : 1852 bytes
!
! Last configuration change at 14:09:23 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname SSV
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport access vlan 140
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 140
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 40
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 40
 switchport mode access
!
interface Ethernet1/2
 switchport access vlan 50
 switchport mode access
!
interface Ethernet1/3
 switchport access vlan 50
 switchport mode access
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## IOU3 conf

```
IOU3#sh run
Building configuration...

Current configuration : 1850 bytes
!
! Last configuration change at 14:09:22 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname IOU3
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/3
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## IOU4 conf

```
IOU4#sh run
Building configuration...

Current configuration : 1850 bytes
!
! Last configuration change at 14:09:23 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname IOU4
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/3
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## IOU1 conf

```
IOU1#sh run
Building configuration...

Current configuration : 1865 bytes
!
! Last configuration change at 14:09:22 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname IOU1
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Port-channel1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 1 mode on
!
interface Ethernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 1 mode on
!
interface Ethernet0/3
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/1
!
interface Ethernet1/2
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## IOU2 conf

```
IOU2#sh run
Building configuration...

Current configuration : 1865 bytes
!
! Last configuration change at 14:09:22 UTC Wed Dec 27 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname IOU2
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Port-channel1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 1 mode on
!
interface Ethernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 1 mode on
!
interface Ethernet0/3
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet1/1
!
interface Ethernet1/2
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## R1 conf

```
R1#sh run
Building configuration...

Current configuration : 1943 bytes
!
version 12.4
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname R1
!
boot-start-marker
boot-end-marker
!
!
no aaa new-model
memory-size iomem 5
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
no ip domain lookup
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
archive
 log config
  hidekeys
!
!
!
!
ip tcp synwait-time 5
!
!
!
!
interface FastEthernet0/0
 ip address dhcp
 ip nat outside
 ip virtual-reassembly
 duplex auto
 speed auto
!
interface FastEthernet0/1
 no ip address
 ip nat inside
 ip virtual-reassembly
 duplex auto
 speed auto
!
interface FastEthernet0/1.10
 encapsulation dot1Q 10
 ip address 10.1.10.254 255.255.255.0
!
interface FastEthernet0/1.20
 encapsulation dot1Q 20
 ip address 10.1.20.254 255.255.255.0
!
interface FastEthernet0/1.30
 encapsulation dot1Q 30
 ip address 10.1.30.254 255.255.255.0
!
interface FastEthernet0/1.40
 encapsulation dot1Q 40
 ip address 10.1.40.254 255.255.255.0
!
interface FastEthernet0/1.50
 encapsulation dot1Q 50
 ip address 10.1.50.254 255.255.255.0
!
interface FastEthernet0/1.60
 encapsulation dot1Q 60
 ip address 10.1.60.254 255.255.255.0
!
interface FastEthernet0/1.140
 encapsulation dot1Q 140
 ip address 10.1.140.254 255.255.255.0
!
interface FastEthernet1/0
 no ip address
 ip nat inside
 ip virtual-reassembly
 duplex auto
 speed auto
!
interface FastEthernet1/0.10
 encapsulation dot1Q 10
 ip address 10.1.10.253 255.255.255.0
!
interface FastEthernet1/0.20
 encapsulation dot1Q 20
 ip address 10.1.20.253 255.255.255.0
!
interface FastEthernet1/0.30
 encapsulation dot1Q 30
 ip address 10.1.30.253 255.255.255.0
!
interface FastEthernet1/0.40
 encapsulation dot1Q 40
 ip address 10.1.40.253 255.255.255.0
!
interface FastEthernet1/0.50
 encapsulation dot1Q 50
 ip address 10.1.50.253 255.255.255.0
!
interface FastEthernet1/0.60
 encapsulation dot1Q 60
 ip address 10.1.60.253 255.255.255.0
!
interface FastEthernet1/0.140
 encapsulation dot1Q 140
 ip address 10.1.140.253 255.255.255.0
!
interface FastEthernet2/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
ip nat inside source list 1 interface FastEthernet1/0 overload
!
access-list 1 permit any
no cdp log mismatch duplex
!
!
!
!
!
!
control-plane
!
!
!
!
!
!
!
!
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
end
```

## DHCP conf

```bash
[joris@dhcptp8site1 ~]$ sudo dnf install -y dhcp-server
```

```conf
[joris@dhcp1client1tp4 ~]$ sudo cat /etc/dhcp/dhcpd.conf
[sudo] password for joris:
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.1.10.0 netmask 255.255.255.0 {
range 10.1.10.100 10.1.10.200;
option routers 10.1.10.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}

subnet 10.1.20.0 netmask 255.255.255.0 {
range 10.1.20.100 10.1.20.200;
option routers 10.1.20.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}

subnet 10.1.30.0 netmask 255.255.255.0 {
range 10.1.30.100 10.1.30.200;
option routers 10.1.30.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}

subnet 10.1.60.0 netmask 255.255.255.0 {
range 10.1.60.100 10.1.60.200;
option routers 10.1.60.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}
;

```

## DNS conf

```bash
[joris@dnstp8site1 ~]$ sudo dnf install bind bind-utils
```

```conf
[joris@dnstp8site1 ~]$ sudo cat /etc/named.conf

options {
        listen-on port 53 { any; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        allow-query     { any; };
        recursion yes;
        include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
        type hint;
        file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

# 🚀 Site "Meow and Beyond"

## Bâtiment 1

### SSVB1 conf

```
SSVB2#sh run
Building configuration...

Current configuration : 1745 bytes
!
! Last configuration change at 03:10:27 UTC Thu Dec 28 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname SSVB2
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport access vlan 130
 switchport mode access
!
interface Ethernet0/2
 switchport access vlan 100
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 100
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 110
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 110
 switchport mode access
!
interface Ethernet1/2
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

### RCB1 conf

```
RCB2#sh run
Building configuration...

Current configuration : 2052 bytes
!
! Last configuration change at 04:28:41 UTC Thu Dec 28 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname RCB2
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport access vlan 80
 switchport mode access
!
interface Ethernet0/2
 switchport access vlan 80
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 90
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 90
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 110
 switchport mode access
!
interface Ethernet1/2
 switchport access vlan 100
 switchport mode access
!
interface Ethernet1/3
 switchport access vlan 100
 switchport mode access
!
interface Ethernet2/0
 switchport access vlan 120
 switchport mode access
!
interface Ethernet2/1
 switchport access vlan 120
 switchport mode access
!
interface Ethernet2/2
 switchport access vlan 120
 switchport mode access
!
interface Ethernet2/3
 switchport access vlan 120
 switchport mode access
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

### B1 conf

```
B1#sh run
Building configuration...

Current configuration : 1604 bytes
!
! Last configuration change at 04:37:46 UTC Thu Dec 28 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname B1
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/3
!
interface Ethernet1/0
!
interface Ethernet1/1
!
interface Ethernet1/2
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

### DHCP conf

```bash
[joris@dhcptp8site1 ~]$ sudo dnf install -y dhcp-server
```

```conf
[joris@dhcptp8site2 ~]$ sudo cat /etc/dhcp/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#

default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.2.10.0 netmask 255.255.255.0 {
range 10.2.10.100 10.2.10.200;
option routers 10.2.10.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.2.1.1;
}

subnet 10.2.20.0 netmask 255.255.255.0 {
range 10.2.20.100 10.2.20.200;
option routers 10.2.20.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.2.1.1;
}

subnet 10.2.30.0 netmask 255.255.255.0 {
range 10.2.30.100 10.2.30.200;
option routers 10.2.30.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.2.1.1;
}

subnet 10.2.60.0 netmask 255.255.255.0 {
range 10.2.60.100 10.2.60.200;
option routers 10.2.60.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.2.1.1;
}
```

## Bâtiment 2

### B2 conf

```
B2#sh run
Building configuration...

Current configuration : 1896 bytes
!
! Last configuration change at 04:36:21 UTC Thu Dec 28 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname B2
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport access vlan 70
 switchport mode access
!
interface Ethernet0/2
 switchport access vlan 70
 switchport mode access
!
interface Ethernet0/3
 switchport access vlan 100
 switchport mode access
!
interface Ethernet1/0
 switchport access vlan 100
 switchport mode access
!
interface Ethernet1/1
 switchport access vlan 100
 switchport mode access
!
interface Ethernet1/2
 switchport access vlan 110
 switchport mode access
!
interface Ethernet1/3
 switchport access vlan 120
 switchport mode access
!
interface Ethernet2/0
 switchport access vlan 120
 switchport mode access
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## IOU10 conf

```
IOU10#sh run
Building configuration...

Current configuration : 1607 bytes
!
! Last configuration change at 04:37:27 UTC Thu Dec 28 2023
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname IOU10
!
boot-start-marker
boot-end-marker
!
!
logging discriminator EXCESS severity drops 6 msg-body drops EXCESSCOLL
logging buffered 50000
logging console discriminator EXCESS
!
no aaa new-model
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
no ip domain-lookup
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
!
interface Ethernet0/3
!
interface Ethernet1/0
!
interface Ethernet1/1
!
interface Ethernet1/2
!
interface Ethernet1/3
!
interface Ethernet2/0
!
interface Ethernet2/1
!
interface Ethernet2/2
!
interface Ethernet2/3
!
interface Ethernet3/0
!
interface Ethernet3/1
!
interface Ethernet3/2
!
interface Ethernet3/3
!
interface Vlan1
 no ip address
 shutdown
!
ip forward-protocol nd
!
ip tcp synwait-time 5
ip http server
!
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
!
end
```

## R2 conf

```
R2#sh run
Building configuration...

Current configuration : 1780 bytes
!
version 12.4
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname R2
!
boot-start-marker
boot-end-marker
!
!
no aaa new-model
memory-size iomem 5
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
no ip domain lookup
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
archive
 log config
  hidekeys
!
!
!
!
ip tcp synwait-time 5
!
!
!
!
interface FastEthernet0/0
 ip address dhcp
 ip nat outside
 ip virtual-reassembly
 duplex auto
 speed auto
!
interface FastEthernet0/1
 no ip address
 ip nat inside
 ip virtual-reassembly
 duplex auto
 speed auto
!
interface FastEthernet0/1.70
 encapsulation dot1Q 70
 ip address 10.2.70.254 255.255.255.0
!
interface FastEthernet0/1.80
 encapsulation dot1Q 80
 ip address 10.2.80.254 255.255.255.0
!
interface FastEthernet0/1.90
 encapsulation dot1Q 90
 ip address 10.2.90.254 255.255.255.0
!
interface FastEthernet0/1.100
 encapsulation dot1Q 100
 ip address 10.2.100.254 255.255.255.0
!
interface FastEthernet0/1.110
 encapsulation dot1Q 110
 ip address 10.2.110.254 255.255.255.0
!
interface FastEthernet0/1.120
 encapsulation dot1Q 120
 ip address 10.2.120.254 255.255.255.0
!
interface FastEthernet0/1.130
 encapsulation dot1Q 130
 ip address 10.2.130.254 255.255.255.0
!
interface FastEthernet1/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface FastEthernet2/0
 no ip address
 shutdown
 duplex auto
 speed auto
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
no cdp log mismatch duplex
!
!
!
!
!
!
control-plane
!
!
!
!
!
!
!
!
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
!
end
```