# OS Libraries
import os
# HTTP Requests Libraries
import requests
from requests_html import HTMLSession, HTML

# The content of the page are loaded in JS so we use HTMLSession
SESSION = HTMLSession()

# Base website
SOURCE_URL = 'https://www.tamberlanecomic.com'

# Directory for saving images
TARGET_DIR = os.path.join(os.getcwd(), 'comic')

def download_image(content, image_url):
    # Save the downloaded image in the target path

    image_name = image_url.split('/')[-1].replace('_','-').replace(' ', '-') # The last element of the url contains the name of the image

    image_path = os.path.join(TARGET_DIR, image_name)

    with open(image_path, 'wb') as file:
        # The image is retrieved as an array of bytes so we use the wb (write byte) option
        print(f"Creating {image_name}")

        file.write(content)

def get_img_source(comic_page):
    # Scrape the website and find the image tag containing the comic page

    print("Retrieving website content")

    website = f'{SOURCE_URL}/comic/{comic_page}'

    request = SESSION.get(f'{website}/').content

    raw_content = HTML(html=request)

    comic_img = raw_content.find("#comic-page")[0].find('img')[0]

    comic_url = f"{SOURCE_URL}{comic_img.attrs['src']}"

    print(f"Downloading Page No. {comic_page}")

    img_content = requests.get(comic_url).content

    # Send the byte content of the image to be saved
    download_image(img_content, comic_url)

if __name__ == '__main__':
    # If target folder doesn't exists create it
    if not os.path.isdir(TARGET_DIR):
        os.mkdir(TARGET_DIR)

    # The comic has a total of 256 pages so far
    for n in range(0, 260):
        # Validate if the comic page was downloaded previously
        if not os.path.exists(os.path.join(TARGET_DIR, f'Page-{n+1}.png')):
            get_img_source(n+1) # use n+1 because range is exclusive in the last value