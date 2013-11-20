<?xml version="1.0" encoding="utf-8"?>
<?python 
def getData():
	try:
		return "".join(file("/var/log/webbrick/daily_xml.log").readlines())
	except:
		return ""
?>
<outer>
    ${XML(getData())}
</outer>
