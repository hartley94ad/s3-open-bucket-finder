import requests
import math
from threading import Thread

para = []
theard_size = 40

f = open('bucket-names.txt', 'r')
for i in f:
    para.append(i.strip())


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


domain = input("please insert domain: ")

chunk_size = math.ceil(len(para) / theard_size)

list_chunks = list(chunks(para, chunk_size))

sucess = []

def run(l):
    for p in l:
        r = requests.head("http://%s%s.s3.amazonaws.com" % (domain, p))
        if r.status_code == 200:
            sucess.append(r.url)
        print('{} : [{}]'.format(r.url, r.status_code))


thread_list = []
for chunk in list_chunks:
    thread_list.append(Thread(target=run, args=(chunk,)))

for t in thread_list:
    t.start()

for t in thread_list:
    t.join()


print("completed")
print("successfully found following open s3 buckets")
print()
for i in sucess:
    print(i)