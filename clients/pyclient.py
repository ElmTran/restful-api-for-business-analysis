import requests

if __name__ == '__main__':
    url = 'http://localhost:8000/api/v1/'
    headers = {
        "Authorization": "Token ee544e3431123548961bb108e66aa6af75e87bb2"
    }

    with open('attachments/testfile.xlsx', 'rb') as f:
        files = {'file': f}
        response = requests.post(url + 'upload/', files=files, headers=headers)
        print(response.status_code)
        print(response.text)
        print(response.content)