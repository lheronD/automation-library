import json

import requests
from requests import Response
from sekoia_automation.action import Action


class FortigateAddIPAction(Action):
    """
    Action to Add an IP Address on a remote fortigate
    """

    def run(self, arguments: dict) -> dict:
        """
        Parameters
        ----------
        name: the fw address object name (type string)
        ip: the ip address to be blocked, (for ex: '1.1.1.1') (type string)
        associated_interface: interface of the object, leave blank for 'Any' (default: Any) (type string)
        comment: (default none) (type string)

        Returns
        -------
        Http status code: 200 if ok, 4xx if an error occurs
        """

        name = arguments["name"]
        ip = arguments["ip"]
        associated_interface = arguments.get("associated_interface", "")
        comment = arguments.get("comment", "")

        payload: dict = {
            "json": {
                "type": "ipmask",
                "name": name,
                "subnet": ip + "/32",
                "associated-interface": associated_interface,
                "comment": comment,
            }
        }

        for firewall in self.module.configuration["firewalls"]:
            base_ip: str = firewall.get("base_ip")
            base_port: str = firewall.get("base_port")
            api_key: str = firewall.get("api_key")

            try:
                response: Response = requests.post(
                    "https://" + base_ip + ":" + base_port + "/api/v2/cmdb/firewall/address/",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}",
                    },
                    params={"vdom": "root"},
                    data=json.dumps(payload),
                    verify=False,
                    timeout=10,
                )
                response.raise_for_status()

            except requests.exceptions.Timeout:
                self.log("Time out session on a firewall", fw_ip=base_ip, level="error")

            except Exception:
                self.log(
                    "Impossible to add IP to the firewall",
                    level="error",
                    fw_ip=base_ip,
                    fw_port=base_port,
                    data=payload,
                )
                pass

        return payload
