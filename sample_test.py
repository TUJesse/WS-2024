import requests

f = open('test.log', 'w+')

def saveResult(name, url, result):
    f.write('Test name:' + str(name) + '\n')
    f.write('Test URL:' + str(url) + '\n')
    f.write('Test result:' + str(result) + '\n')
    f.write('---------------------------------------------\n ')


def checkServiceForWord(url, keyword):
    result = False
    try:
        x = requests.get(url)
        #print(x.text)
        serverStatus=1

        if keyword in x.text:
            print("found keyword")
            return True
    except:
        print("error")
        return False

# Test 1
url = 'http://127.0.0.1:5000/getProducts'
result = checkServiceForWord(url, 'Jam')
print(result)

# Test 2
url = 'http://127.0.0.1:5000'
result1 = checkServiceForWord(url, '/getTitles')
print(result1)
# finish up
f.close()
