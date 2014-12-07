#!/usr/bin/python

import os, tarfile, bz2, json, subprocess, pymongo

tempdir = "/root/tempdir/"
archive = "archive-09.tar"
bz = []
tar = tarfile.TarFile("archive-09.tar")

client = pymongo.MongoClient()
db = client.test_database
tweets = db.tweets

for member in tar:
        tar.extractall(path=tempdir, members=[member])
        if(member.isfile()):
                bz = bz2.BZ2File(tempdir+member.name)
                for line in bz:
                        data = json.loads(line)
                        if ("text" in data.keys()) and ("en" in data["lang"]):
                                #print data["text"]
                                tweets.insert({"created_at": data["created_at"], "text": data["text"]})
                subprocess.check_output("rm " + tempdir+member.name,shell=True)
                #if "n" in raw_input():
                #       exit()
