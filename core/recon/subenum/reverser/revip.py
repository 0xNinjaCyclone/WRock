# Author    =>  Abdallah Mohamed
# Date      =>  26-1-2022

import requests, json
from core.config.enumerator import ReverseIPConfig

class ReverseIPBase:

    def __init__(self, config: ReverseIPConfig) -> None:
        self.config     = config
        self.target     = self.config.GetTarget()
        self.headers    = self.config.GetHeaders()
        self.timeout    = self.config.GetTimeout()

    def get_url(self):
        pass

    def enumerate(self):
        pass


class Sonar(ReverseIPBase):
    def __init__(self, config: ReverseIPConfig) -> None:
        ReverseIPBase.__init__(self, config)

    def get_url(self):
        return "https://sonar.omnisint.io/reverse/" + self.target

    def enumerate(self):
        # subdomains container
        subdomains = list()

        # Service url
        url = self.get_url()

        try:
            res = requests.get(url, headers=self.headers.GetAll(), timeout=self.timeout)
            if 'application/json' in res.headers.get("Content-Type"):
                data = json.loads(res.text)
                
                # Check if valid data
                if data:
                    # Append subdomains to the container
                    for item in range(len(data)):
                        if data[item] not in subdomains:
                            subdomains.append(data[item])
            
        except:
            pass
            

        return subdomains
