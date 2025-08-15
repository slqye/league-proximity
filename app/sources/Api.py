import requests

class LiveClient:
	def __init__(self, url: str, certificate: str) -> None:
		self._url = url
		self._certificate = certificate

	def get(self, endpoint: str) -> str:
		response = requests.get(self._url + endpoint, verify=self._certificate)
		return response
