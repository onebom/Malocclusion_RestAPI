import requests
import sys

username = 'mmmil'
if len(sys.argv) > 1:
    name = sys.argv[1]

# local의 경우
url = 'http://127.0.0.1:8000/DeepLearningModelInference/'
# Dentis Server의 경우
# url = 'http://117.16.56.202:8000/DeepLearningModelInference/'


# AWS의 경우
#url = 'http://3.36.162.250:8000/DeepLearningModelInference/'
# Post 할 이미지 파일 
fstr = input("malocclusion image path : ")


with open(fstr, 'rb') as files:

    obj = {'name':username }
    upload = {'Medical_image':files}
    res = requests.post(url, files=upload, data=obj)
    
    print(res.status_code)
    print(res.json())
#     print(res.content)