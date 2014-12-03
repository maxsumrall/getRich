#!/usr/bin/python

import os, tarfile, bz2, json, subprocess

tempdir = "/root/tempdir/"
archive = "archive-09.tar"
bz = []
tar = tarfile.TarFile("archive-09.tar")
for member in tar:
	tar.extractall(path=tempdir, members=[member])
	if(member.isfile()):
		bz = bz2.BZ2File(tempdir+member.name)
		for line in bz:
			data = json.loads(line)
			if ("text" in data.keys()) and ("en" in data["lang"]):
				print data["text"]
		subprocess.check_output("rm " + tempdir+member.name,shell=True)
		if "n" in raw_input():
			exit()

