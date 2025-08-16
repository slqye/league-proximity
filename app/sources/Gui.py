import tkinter as tk
import ttkbootstrap as ttk

import sources.Constants as constants
import sources.Api as api
import sources.Game as game
import sources.Mumble as mumble

class Window:
	def __init__(self, title: str, size: (int, int), theme: str) -> None:
		self._root = ttk.Window(title=title, size=size, themename=theme)
		self._tk_photo_holder = tk.PhotoImage(file="includes/champions/unknown.png")
		self._root.iconphoto(False, self._tk_photo_holder)
		self._root.resizable(False, False)
		self._root.protocol("WM_DELETE_WINDOW", self.on_close)
		self._is_running = False
		self._live_client = api.LiveClient(constants.SERVER_URL, constants.CERTIFICATE)
		self._player: game.Player = None
		self._mumble_link: mumble.MumbleLink = None
		self._toggle_btn: ttk.Button = None

	def run(self):
		self._toggle_btn = ttk.Button(
			self._root,
			text="Enable",
			bootstyle="primary",
			command=self.toggle_tracking
		)
		self._toggle_btn.pack(padx=10, pady=10, fill=tk.X)
		self._root.mainloop()

	def on_close(self):
		self._root.destroy()

	def update(self):
		if not self._is_running:
			return
		else:
			try:
				if (self._player is None and self._mumble_link is None):
					print("Connecting to live client...")
					self._player = game.Player(self._live_client.get_player_champion(), 0.6)
					self._mumble_link = mumble.MumbleLink(self._player._champion)
					self.set_icon(self._player._champion)
				self._player.update()
				self._mumble_link.update(self._player)
				self._root.after(25, self.update)
			except Exception:
				self._root.after(1000, self.update)

	def reset(self):
		self._player = None
		self._mumble_link = None
		self.set_icon("unknown")

	def toggle_tracking(self):
		self._is_running = not self._is_running
		self._toggle_btn.config(
			text="Enable" if not self._is_running else "Disable",
			bootstyle="primary" if not self._is_running else "danger"
		)
		self.update() if self._is_running else self.reset()

	def set_icon(self, icon: str):
		self._tk_photo_holder = tk.PhotoImage(file=f"includes/champions/{icon}.png")
		self._root.iconphoto(False, self._tk_photo_holder)
