import ctypes
import mmap

class LinkedMem(ctypes.Structure):
	_fields_ = [
		("uiVersion", ctypes.c_uint32),
		("uiTick", ctypes.c_uint32),
		("fAvatarPosition", ctypes.c_float * 3),
		("fAvatarFront", ctypes.c_float * 3),
		("fAvatarTop", ctypes.c_float * 3),
		("name", ctypes.c_wchar * 256),
		("fCameraPosition", ctypes.c_float * 3),
		("fCameraFront", ctypes.c_float * 3),
		("fCameraTop", ctypes.c_float * 3),
		("identity", ctypes.c_wchar * 256),
		("context_len", ctypes.c_uint32),
		("context", ctypes.c_ubyte * 256),
		("description", ctypes.c_wchar * 2048)
	]

class MumbleLink:
	def __init__(self, identity: str) -> None:
		self._memfile = mmap.mmap(-1, ctypes.sizeof(LinkedMem), tagname="MumbleLink")
		self._link = LinkedMem.from_buffer(self._memfile)
		self._link.uiVersion = 2
		self._link.name = "League of Legends"
		self._link.identity = identity
		self._link.description = "League of Legends positional audio sender"
		self._tick = 0

	def update(self, position: tuple) -> None:
		self._tick += 1
		self._link.uiTick = self._tick
		self._link.fAvatarPosition[:] = (position[0], position[1], 0)
		self._link.fAvatarFront[:] = (1, 0, 0)
		self._link.fAvatarTop[:] = (0, 0, 1)
		self._link.fCameraPosition[:] = self._link.fAvatarPosition
		self._link.fCameraFront[:] = self._link.fAvatarFront
		self._link.fCameraTop[:] = self._link.fAvatarTop
		self._memfile.flush()
