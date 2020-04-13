from Module import Module
import paramiko
import os

modules = []

def gen_server_file(flag, options):
	comment = ""
	if len(options) == 3:
		port, username, password = options
	elif len(options) == 4:
		port, username, password, comment = options
		comment = "\\r\\n".join(comment.split("|"))
	file = open("ssh_template.py", "r")
	data = file.read()
	file.close()
	data = data.replace("pOrTnUmBeR", port)
	data = data.replace("fLaG cOnTeNt", "Flag: " + flag)
	data = data.replace("UsErKeY", username)
	data = data.replace("pAsSkEy", password)

	data = data.replace("# c0mmenT", 'chan.send("' + comment.replace('"', '\\"') + '")')

	file = open("server.py", "w")
	file.write(data)
	file.close()

	if not os.access("host_rsa.key", os.R_OK):
		key = paramiko.RSAKey.generate(bits=1024)
		key.write_private_key_file("host_rsa.key")

	print("Run the SSH Server from server.py")
	return "server.py"

modules.append(Module("<X> Generate SSH Server to give flag to authed user", gen_server_file, ["Port Number (above 1000, required)", "Username, required", "Password, required", "Comment (can leave blank, separate lines with '|')"]))