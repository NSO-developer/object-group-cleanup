import re
if __name__ == "__main__":
	rul = "extended permit tcp object-group emear-ams-extranet-regional-address-block object-group HOST:antivirus.cisco.com object-group web-services"

	m = re.findall('object-group ([\w:*.*]+[-\w+*.*]*)', rul)

	print m
