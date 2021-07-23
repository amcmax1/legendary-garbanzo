import json
import requests
import uuid

# todo: determine the file extension of each url before saving file
# todo: ensure uniqueness of uuid
# todo: extract repeated function for different outputs gp and ed


class ImageDownloadService:
    def __init__(self, json_file):
        self.json_file = json_file
        self.image_urls = []

    def parse_json(self):
        json_file = open(self.json_file)
        file_content = json_file.read()
        json_as_python_hash = json.loads(file_content)
        for key, value in json_as_python_hash.items():
            url_list = [value]
        import itertools
        self.image_urls = list(itertools.chain(*url_list))
        print(self.image_urls)

    def download_images(self):
        for url in self.image_urls:
            res = requests.get(url)
            res.raise_for_status()
            image_file_uuid = uuid.uuid4().hex[:7]

            gp_image_file = open(f'./assets/original_images_gp/{image_file_uuid}.jpg', 'wb')
            for chunk in res.iter_content(100000):
                gp_image_file.write(chunk)
            gp_image_file.close()

            ed_image_file = open(f'./assets/original_images_ed/{image_file_uuid}.jpg', 'wb')
            for chunk in res.iter_content(100000):
                ed_image_file.write(chunk)
            ed_image_file.close()