import requests

response = requests.post(
    'http://127.0.0.1:5000/announcement/',
    json={
        'title': 'title_1',
        'description': 'description_1',
        'author': 'author_1'
    },
)

print(response.status_code)
print(response.json())
print(response.text)
