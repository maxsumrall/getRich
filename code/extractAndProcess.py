#!/usr/bin/python

import os, tarfile, bz2, json, subprocess, pymongo

tempdir = "/root/tempdir/"
archive = "archive-08.tar"
bz = []
tar = tarfile.TarFile("archive-08.tar")

client = pymongo.MongoClient()
db = client.test_database
tweets = db.tweets

for member in tar:
    tar.extractall(path=tempdir, members=[member])
    tweets_in_file = [] #for batch insertion
    if (member.isfile()): #these things will either be files or the folders
        bz = bz2.BZ2File(tempdir + member.name)
        for line in bz:
            data = json.loads(line)
            if ("text" in data.keys()) and ("en" in data["lang"]):
                tweets_in_file.append({"created_at": data["created_at"], "text": data["text"]})
        tweets.insert(tweets_in_file) #batch insert the tweets into mongo
        subprocess.check_output("rm " + tempdir + member.name, shell=True) #Delete the file

