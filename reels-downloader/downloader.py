import sys
import os
from requests_html import HTMLSession, HTML
from requests.exceptions import RequestException

# FOLDER PATH
CW_FOLDER   = os.getcwd()
REEL_FOLDER = os.path.join(CW_FOLDER, "Reels")

SESSION = HTMLSession()

if len(sys.argv[1:]) == 2:

    if sys.argv[1].__contains__("www.instagram.com/reel/"):

        if not os.path.isdir(REEL_FOLDER):
            os.mkdir(REEL_FOLDER)

        ig_response = SESSION.get(sys.argv[1])

        content = HTML(html=ig_response.text)

        meta_tags = content.find("meta")

        property_tags = [tag for tag in meta_tags if "property" in tag.attrs.keys()]

        meta_video = [tag for tag in property_tags if tag.attrs["property"] == "og:video"][0]

        video_url = meta_video.attrs["content"]

        try:

            video_response = SESSION.get(video_url, stream=True)

            if video_response.headers['Content-Type'] == 'video/mp4':
                total = 0

                video_name = os.path.join(REEL_FOLDER, f"{sys.argv[2]}.mp4")

                with open(video_name, 'wb') as video:
                    for chunk in video_response.iter_content(chunk_size=512):
                        if chunk:
                            video.write(chunk)
                            total += 512
                        print(f"{total/1024} kb so far\n")

        except RequestException as err:
            print("Error: Invalid URL")
            
    else:
        print("Error: Make sure the URL is a valid IG reel")

else:
    print("Must pass two valid arguments: Reel URL, filename")