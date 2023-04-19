import platform
import sys
import time

# TODO: Check if we are running on Raspberry Pi
system = f"{platform.uname().system} {platform.uname().release}"

print("Green Garden IoT Controller started")
print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
print(f"System: {system}")
print("")

try:
	i = 0
	while True:
		i += 1
		print(f"{i}")
		time.sleep(1)
except KeyboardInterrupt:
	print("")
	print("Exiting...")
	sys.exit(0)
