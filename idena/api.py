import requests


class IdenaAPI:

    _host = "localhost"
    _port = "9009"
    _timeout = 3

    def __init__(self, host=_host, port=_port, timeout=_timeout):
        self._host = host
        self._port = port
        self._timeout = timeout
        self.url = f"http://{host}:{port}"

    def __request(self, url, payload):
        try:
            response = requests.post(url, json=payload, timeout=self._timeout).json()
        except Exception as e:
            return {"success": False, "data": repr(e)}

        if response and response["result"]:
            return {"success": True, "data": response["result"]}
        else:
            return {"success": False, "data": response}

    def identities(self):
        payload = {
            "method": "dna_identities",
            "id": 1
        }
        return self.__request(self.url, payload)

    def identity(self, address):
        payload = {
            "method": "dna_identity",
            "params": [address],
            "id": 1
        }
        return self.__request(self.url, payload)

    def epoch(self):
        payload = {
            "method": "dna_epoch",
            "id": 1
        }
        return self.__request(self.url, payload)

    def ceremony_intervals(self):
        payload = {
            "method": "dna_ceremonyIntervals",
            "id": 1
        }
        return self.__request(self.url, payload)

    def address(self):
        payload = {
            "method": "dna_getCoinbaseAddr",
            "id": 1
        }
        return self.__request(self.url, payload)

    def balance(self, address):
        payload = {
            "method": "dna_getBalance",
            "params": [address],
            "id": 1
        }
        return self.__request(self.url, payload)

    def transactions(self, address, count):
        payload = {
            "method": "bcn_transactions",
            "params": [{"address": f"{address}", "count": int(count)}],
            "id": 1
        }
        return self.__request(self.url, payload)

    def pending_transactions(self, address, count):
        payload = {
            "method": "bcn_pendingTransactions",
            "params": [{"address": f"{address}", "count": int(count)}],
            "id": 1
        }
        return self.__request(self.url, payload)

    def kill_identity(self, address):
        payload = {
            "method": "dna_sendTransaction",
            "params": [{"type": 3, "from": f"{address}", "to": f"{address}"}],
            "id": 1
        }
        return self.__request(self.url, payload)

    # TODO: Rename to 'mining_on'?
    def go_online(self):
        payload = {
            "method": "dna_becomeOnline",
            "id": 1
        }
        return self.__request(self.url, payload)

    # TODO: Rename to 'mining_off'?
    def go_offline(self):
        payload = {
            "method": "dna_becomeOffline",
            "id": 1
        }
        return self.__request(self.url, payload)

    def send(self, from_address, to_address, amount):
        payload = {
            "method": "dna_sendTransaction",
            "params": [{"from": from_address, "to": to_address, "amount": amount}],
            "id": 1
        }
        return self.__request(self.url, payload)

    def sync_status(self):
        payload = {
            "method": "bcn_syncing",
            "id": 1
        }
        return self.__request(self.url, payload)

    def node_version(self):
        payload = {
            "method": "dna_version",
            "id": 1
        }
        return self.__request(self.url, payload)

    def import_key(self, key, password):
        payload = {
            "method": "dna_importKey",
            "params": [{"key": key, "password": password}],
            "id": 1
        }
        return self.__request(self.url, payload)
