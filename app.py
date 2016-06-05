import requests, json, sys
from urllib import request
from os import path, system, environ

api_url_iotd = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
api_url_last8 = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8"

def download_images(image_url, image_path):
    print(image_url)
    request.urlretrieve(image_url, image_path)
    
def download_json(api_url):
    try:
        response = requests.get(api_url)
        json_data = response.json()['images']
        for i in json_data:
            url = i['url']
            url = "http://www.bing.com" + url
            image_name = url.split('/')[-1]
            image_path = path.join(path.expanduser('~'),'Pictures/Bing_Images/'+image_name)
            download_images(url, image_path)
        return(image_path)
    except:
        print('Unexpected Error in function download_json')

def set_wallpaper(image_path):
    wallpaper_command = 'gsettings set org.gnome.desktop.background picture-uri file://'+image_path
    system(wallpaper_command)  

def get_desktop_environment():
    print(environ.get('DESKTOP_SESSION'))  

def main():
    option = 2
    
    if option == 1:
        print('Set the following image of the day as wallpaper')
        img_path = download_json(api_url_iotd)
        set_wallpaper(img_path)
    elif option == 2:
        print('Saving the following images of the day to the system')
        download_json(api_url_last8)
    else:
        get_desktop_environment()


if __name__ == '__main__':
    main()