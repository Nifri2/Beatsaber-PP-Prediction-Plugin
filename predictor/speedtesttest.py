from tqdm import tqdm
import requests
import time
import json

now = time.time()

for i in tqdm(range(0,100)):
	data = {"stars": 9, "acc": i / 100}
	r = requests.post("http://127.0.0.1:5000/predict",data=data)
	json.loads(r.text)

done = time.time() 
print(f"[>] 100 requests took {done - now}s")
print(f"[>] Thats {(done - now) / 100}s per iteration ")
print(f"[>] That means a song can easily have {60 / ((done - now))} bloqs per second")