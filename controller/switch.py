import requests


def main(a="On", b="On", c="On", d="On"):
    url = "http://192.168.1.111/tgi/iocontrol.tgi"
    d = """
    pw1Name=
    P60={}
    P60_TS=0
    P60_TC=Off
    pw2Name=
    P61={}
    P61_TS=0
    P61_TC=Off
    pw3Name=
    P62={}
    P62_TS=0
    P62_TC=Off
    pw4Name=
    P63={}
    P63_TS=0
    """.format(a, b, c, d).replace('\n', '\r')

    requests.post(url, data=d)
