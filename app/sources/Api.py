import requests

class LiveClient:
	def __init__(self, url: str, certificate: str) -> None:
		self._url = url
		self._certificate = certificate

	def get(self, endpoint: str) -> str:
		response = requests.get(self._url + endpoint, verify=self._certificate)
		return response

	def get_player_champion(self) -> str:
		players: list = self.get("playerlist").json()
		riot_id: str = self.get("activeplayername").text.strip("\"")

		for player in players:
			if player["riotId"] == riot_id:
				return player["championName"].lower()
		return None
