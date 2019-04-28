from  flask import render_template
from  app import app
import scapy.all as scapy
from scapy.layers import http
import sqlite3

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',title="APP Flow Mirror")
@app.route('/startscan',methods=['GET','POST'])
def startscan():
	# info list
	dns_list = []
	ua_list = []
	mac_list = []
	# capture network traffic
	pkts = capture()
	for pkt in pkts:
		if pkt.haslayer(scapy.Ether):
			mac_list.append(pkt[scapy.Ether].src)

		if scapy.DNS in pkt:
			if pkt[scapy.DNS].qr == 0:
				dns_list.append(dns_process(pkt))
		if http.HTTPRequest in pkt:
			ua_list.append(http_process(pkt))
	# read data from db and compare
	scan_tmp = []
	device_name = []
	app_name = []
	dns_tmp = []
	conn = sqlite3.connect('app/db/data.db')
	c = conn.cursor()
	result = c.execute("SELECT UA FROM DEVICE")
	for row in result:
		for ua in ua_list:
			row_b=bytes(row[0],encoding = "utf8")
			if ua.find(row_b) != -1:
				scan_tmp.append(row_b);
	for item in scan_tmp:
		names = c.execute('SELECT NAME,TYPE FROM DEVICE WHERE UA LIKE "%s"' % str(item,encoding = "utf8"))
		for name in names:
			device_name.append(name[0])
			if name[1] == 'phone': 	
				# do this, if device is a phone
				dns_tmp = []
				result_app = c.execute("SELECT DNS FROM APP")
				for row in result_app:
					for dns in dns_list:
						row_b=bytes(row[0],encoding = "utf8")
						if dns.find(row_b) != -1:
							dns_tmp.append(row_b);
				for item in dns_tmp:
					dnss = c.execute('SELECT NAME FROM APP WHERE DNS LIKE "%s"' % str(item,encoding = "utf8"))
					for dns in dnss:
						for item in dns:
							app_name.append(item)

	print(set(device_name))
	print(set(app_name))	
		
	# output : found xx device  and type of device
	return render_template('scan.html',title="Start scan",apps=set(app_name),devices=set(device_name))

def capture():
	# select interface
	pass

	return scapy.sniff(iface="eth0",counts=20000)
def dns_process(pkt):
	print('dns')
	device_mac = pkt[scapy.Ether].src
	domain = pkt[scapy.DNSQR].qname.lower()
	return domain

def http_process(pkt):
	print('http')
	ua = pkt['HTTPRequest'].fields['User-Agent']
	return ua
