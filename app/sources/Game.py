import cv2
import numpy as np

from PIL import ImageGrab

MAP_SIZE = (400, 400)

class Player:
	def __init__(self, champion: str, treshold: float) -> None:
		self._champion: str = champion
		self._treshold: float = treshold
		self._position: (float, float) = (0, 0)
		self._confidence: float = 0.0
		self._icon = cv2.imread(f"includes/champions/{self._champion}.png")
		self._icon = cv2.resize(self._icon, (28, 28), interpolation=cv2.INTER_AREA)
		self._icon = self._icon[5:23, 5:23]
		self._icon_size = self._icon.shape[:2][0]

	def update(self) -> None:
		map = Player.get_map_image(MAP_SIZE)
		map = cv2.cvtColor(map, cv2.COLOR_BGRA2BGR)
		result = cv2.matchTemplate(map, self._icon, cv2.TM_CCOEFF_NORMED)
		_, max_value, _, max_location = cv2.minMaxLoc(result)
		self._confidence = max_value
		if (max_value >= self._treshold):
			position_x: float = max_location[0] + (self._icon_size / 2)
			position_y: float = max_location[1] + (self._icon_size / 2)
			print(f"Position: ({position_x}, {position_y})")
			self._position = (position_x, position_y)

	def get_map_image(size: tuple) -> np.ndarray:
		screenshot = ImageGrab.grab()
		screen_width, screen_height = screenshot.size
		left = screen_width - size[0]
		top = screen_height - size[1]
		right = screen_width
		bottom = screen_height
		region = screenshot.crop((left, top, right, bottom))
		result = np.array(region)
		return result
