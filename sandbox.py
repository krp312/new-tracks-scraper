import subprocess

link = 'emily haines'

subprocess.call(["youtube-dl", "-f", "bestaudio[ext=m4a]", f"ytsearch:{link}"])