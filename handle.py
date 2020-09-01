import os
import re
import subprocess
from influxdb import InfluxDBClient


class InfluxClient:
    def __init__(self, download, upload, ping):
        influx_host = os.environ["INFLUX_HOST"]
        influx_port = os.environ["INFLUX_PORT"]
        influx_user = os.environ["INFLUX_USER"]
        influx_pass = os.environ["INFLUX_PASSWORD"]
        
        self.client = InfluxDBClient(influx_host, influx_port, influx_user, influx_pass, 'internetspeed')
        self.download = download
        self.upload = upload
        self.ping = ping


    def write(self):
        speed_data = [
            {
                "measurement" : "internet_speed",
                "tags" : {
                    "host": "RaspberryPiMyLifeUp"
                },
                "fields" : {
                    "download": float(self.download),
                    "upload": float(self.upload),
                    "ping": float(self.ping)
                }
            }
        ]

        self.client.write_points(speed_data)


def main(record_client=InfluxClient):
    response = subprocess.Popen("/usr/local/bin/speedtest-cli --simple", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    ping = re.findall(r"Ping:\s(.*?)\s", response, re.MULTILINE)
    download = re.findall(r"Download:\s(.*?)\s", response, re.MULTILINE)
    upload = re.findall(r"Upload:\s(.*?)\s", response, re.MULTILINE)

    ping = ping[0].replace(",", ".")
    download = download[0].replace(",", ".")
    upload = upload[0].replace(",", ".")

    record_client(download, upload, ping).write()
    

if __name__ == '__main__':
    main()