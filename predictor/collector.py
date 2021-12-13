from multiprocessing.dummy import Pool
from pandas.core.base import DataError
from tqdm import tqdm
import pandas as pd
import requests
import pickle
import json
import csv
import sys

def getSongLeaderboard(songHash,diff,page):
    r = requests.get(
        f"https://scoresaber.com/api/leaderboard/by-hash/{songHash}/scores?difficulty={diff}&page={page}")
    return json.loads(r.text)['scores']

def calcMetadata(songHash,diff):
    r = requests.get(
        f"https://scoresaber.com/api/leaderboard/by-hash/{songHash}/scores?difficulty={diff}")
    meta = json.loads(r.text)['metadata']
    r = requests.get(
        f"https://scoresaber.com/api/leaderboard/by-hash/{songHash}/info?difficulty={diff}")
    song = json.loads(r.text)
    return {"steps":    meta["total"] // meta["itemsPerPage"],
            "modulo":   meta["total"] % meta["itemsPerPage"],
            "maxScore": song["maxScore"],
            "stars":    song["stars"]}

def doShit(data):
    dataset = []
    failed = []
    songHash = data[0]
    diff     = data[1]
    try:
        meta = calcMetadata(songHash,diff)
        for page in tqdm(range(meta["steps"])):
            try:
                scores = getSongLeaderboard(songHash,diff,page)
                for score in scores:
                    if "NF" not in score["modifiers"]:
                        acc = score["baseScore"] / meta["maxScore"]
                        pp = score["pp"]
                        dataset.append([meta["stars"],acc,pp])
            except Exception as r:
                pass
    except Exception as e:
        print("couldnt fetch song, prob rate limited or some shit")
        with open("collected/failed.txt" ,'a') as file:
            for i in failed:
                file.write(f"{i}\n")
    
    return dataset

def prepareCSV(file):
    dataset = []
    data = pd.read_csv(file)
    for h,d in zip(data.HASH, data.Difficulty):
        dataset.append([h,d])
    return dataset

def writeCSV():
    with open('collected/dataset.pkl','rb') as file:
        dataset = pickle.load(file)
    print(f'[>] Dataset Shape: {len(dataset)} x {len(dataset[0])} x {len(dataset[0][0])}')
    with open('collected/dataset.csv', 'w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["stars","acc","pp"])
        for base in dataset:
            for data in base:
                writer.writerow(data)
    print("[>] Done writing 'collected/dataset.csv'")

# (1 = Easy, 3 = Normal, 5 = Hard, 7 = Expert, 9 = Expert+)
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('not enough arguments')
        exit()
    elif len(sys.argv) > 2:
        print('too many arguments')
        exit()
    if sys.argv[1] == 'all':
        print("[>] Starting")
        data = prepareCSV("songs.list")
        # more threads = more likley to get rate limited
        pool = Pool(1)
        abs_dataset = pool.map(doShit,data)
        with open('collected/dataset.pkl','wb') as file:
            pickle.dump(abs_dataset,file)
        print("\n"*10)
        print("[>] Formatting data")
        writeCSV()
    if sys.argv[1] == 'csv':
        print("[>] Formatting data")
        writeCSV()