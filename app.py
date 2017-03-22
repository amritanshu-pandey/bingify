import requests, json, sys, argparse
from urllib import request
#import urllib2
from os import path, system, environ
import ctypes

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
    DE = get_desktop_environment()
    print('Platform is:', DE)
    
    if DE == 'WINDOWS':
        SPI_SETDESKWALLPAPER = 20 
        print(image_path)
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path , 3)
    elif DE == 'mate':
        system("gsettings set org.mate.background picture-filename '%s'" % image_path)
    else:
        wallpaper_command = 'gsettings set org.gnome.desktop.background picture-uri file://'+image_path
        system(wallpaper_command)

def get_desktop_environment():
    if sys.platform in ['win32','cygwin']:
        return ('WINDOWS')
    else:
        return (environ.get('DESKTOP_SESSION'))  

def main():
    parser = argparse.ArgumentParser(description="Download Bing image of the day and set as wallpaper")
    parser.add_argument('--download','-d',
                    help='Download the last eight Bing of the day images',
                    action="store_true")
    args = parser.parse_args()

    if args.download:
        print('Saving the following images of the day to the system')
        download_json(api_url_last8)
    else:
        print('Set the following image of the day as wallpaper')
        img_path = download_json(api_url_iotd)
        set_wallpaper(img_path)
        
if __name__ == '__main__':
    main()
