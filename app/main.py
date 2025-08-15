import sys
import cv2 as cv
import numpy as np

import sources.Api as api

SERVER_URL = "https://localhost:2999/liveclientdata/"
CERTIFICATE = "includes/api/riotgames.pem"

def get_player_champion(live_client: api.LiveClient) -> str:
	players: list = live_client.get("playerlist").json()
	riot_id: str = live_client.get("activeplayername").text.strip("\"")

	for player in players:
		if player["riotId"] == riot_id:
			return player["championName"].lower()
	return None

def main(argc: int, argv: [str]) -> None:
	if argc != 1:
		return
	live_client = api.LiveClient(SERVER_URL, CERTIFICATE)
	champion = get_player_champion(live_client)

	map = cv.imread("includes/map.png")
	icon = cv.imread(f"includes/champions/{champion}.png")
	result = cv.matchTemplate(map, icon, cv.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
	h, w = icon.shape[:2]
	top_left = max_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
	cv.rectangle(map, top_left, bottom_right, (0, 255, 0), 2)
	# Save and print
	cv.imwrite("/mnt/c/Users/Slaye/Desktop/match_result.png", map)
	print(f"Match position: {top_left}, Confidence: {max_val}")

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
