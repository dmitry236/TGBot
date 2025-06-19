import requests

def ask_acetone(img_path:str):
    with open(img_path, 'rb') as file:
        ans = requests.post(
            url='https://api.acetone.ai/api/v1/remove/background?format=png',
            files={
                'image': ('temp/downloaded_photo.png', file.read()),
            },
            headers={'Token': ''}
        )
    if ans.headers['content-type'] in ('image/png', 'image/webp', 'image/jpeg'):
        with open('temp/downloaded_photo.png', 'wb') as file:
            file.write(ans.content)
    else:
        print(ans.json())    
    
#ans = ask_acetone('./downloaded_photo.jpg')


