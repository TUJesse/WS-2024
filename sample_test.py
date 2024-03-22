import requests


def checkServiceForWord(url, keyword):
    try:
        x = requests.get(url)
        #print(x.text)
        serverStatus = 1

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
