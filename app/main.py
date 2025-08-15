import time

import sources.Api as api
import sources.Game as game
import sources.Mumble as mumble

SERVER_URL = "https://localhost:2999/liveclientdata/"
CERTIFICATE = "includes/api/riotgames.pem"

def main() -> None:
	try:
		print("[?] Connecting to League of Legends Live Client API")
		live_client = api.LiveClient(SERVER_URL, CERTIFICATE)
		print("[?] Creating player tracker")
		player = game.Player(live_client.get_player_champion(), 0.6)
		print("[?] Initializing Mumble Link")
		mumble_link = mumble.MumbleLink(player._champion)

		print("[?] Tracking started")
		while True:
			player.update()
			mumble_link.update(player._position)
			time.sleep(0.05)
	except Exception as e:
		print(f"[!] An error occurred: {e}")


if __name__ == "__main__":
	main()
