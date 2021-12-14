from matplotlib import pyplot as plt
from tqdm import tqdm
import requests
import time
import json

now = time.time()
pdata = []

for j in range(1,15):
	g = []
	for i in tqdm(range(0,1000)):
		data = {"stars": j, "acc": i / 1000}
		r = requests.post("http://127.0.0.1:5000/predict",data=data)
		g.append(json.loads(r.text)['pp'])
	pdata.append(g)

done = time.time() 
print(f"[>] 100 requests took {done - now}s")
print(f"[>] Thats {(done - now) / 100}s per iteration ")
print(f"[>] That means a song can easily have {60 / ((done - now))} bloqs per second")

for i in pdata:
	plt.plot(i)
plt.show()