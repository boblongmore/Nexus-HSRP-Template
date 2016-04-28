#! /usr/bin/python

from datetime import datetime
import csv

#parses csv file for IPAM information then passes to get_val to initialize variables for configuration
def get_lines():
	with open('hsrp-create.csv', 'rb') as csvfile:
		ipam_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in ipam_reader:
			hsrp_list = row[0].split(',')
			get_val(hsrp_list)

#takes each row of IPAM information and initializes IP, VLAN, name variables
def get_val(ipam_row):
	vl_num = ipam_row[0]
	vl_descr = ipam_row[1]
	vl_network = ipam_row[2]
	hsrp_create(vl_num, vl_descr, vl_network)
	vlan_create(vl_num, vl_descr)

#Create VLANs
def vlan_create(vl_num, vl_descr):
	vlan_text = 'vlan %s \ndescription %s \n' % (vl_num, vl_descr)
	with open(filename3, "a") as myfile:
		myfile.write(vlan_text)

#takes variables and creates two files with configuration templates and timestamps. The two files are for HSRP primary and HSRP Standby respectively.
def hsrp_create(vl_num, vl_descr, vl_network):
	network_split = vl_network.split('.')
	vip = network_split[:]
	svi_1 = network_split[:]
	svi_2 = network_split[:]
	vip[3] = '1'
	h_vip = '.'.join(vip)
	svi_1[3] = '2'
	h_svi_active = '.'.join(svi_1)
	svi_2[3] = '3'
	h_svi_standby = '.'.join(svi_2)
	HSRP1_text = 'int vlan %s \ndescription %s \nip add %s/24 \nhsrp ver 2 \nhsrp %s \nauthentication md5 key-chain HSRP_KEYS \npreempt \npriority 110 \nip %s \n \n' % (vl_num, vl_descr, h_svi_active, vl_num, h_vip)
	with open(filename1, "a") as myfile:
		myfile.write(HSRP1_text)
	HSRP2_text = 'int vlan %s \n description %s \nip add %s/24 \nhsrp ver 2 \nhsrp %s \nauthentication md5 key-chain HSRP_KEYS \npreempt \nip %s \n \n' % (vl_num, vl_descr, h_svi_standby, vl_num, h_vip)
	with open(filename2, "a") as myfile:
		myfile.write(HSRP2_text)

filename1 = "HSRP1-" + str(datetime.now().strftime('%Y-%m-%d_%H%M')) + ".txt"
filename2 = "HSRP2-" + str(datetime.now().strftime('%Y-%m-%d_%H%M')) + ".txt"
filename3 = "VLAN-" + str(datetime.now().strftime('%Y-%m-%d_%H%M')) + ".txt"
get_lines()