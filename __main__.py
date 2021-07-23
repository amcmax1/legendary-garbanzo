import time
import json
import os
import pickle
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from services.image_download_service import ImageDownloadService
from services.image_projector_service import ImageProjectorService
from services.image_edge_detection_service import ImageEdgeDetectionService
from models.ImageData import ImageData

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

# todo: extract the switch cases into separate method to dispatch to services taking event.src_path as argument

def on_created(event):
    if "/json_requests" in event.src_path:
        print(f"{event.src_path} in json_requests created!")

        # Initiates Image Download Service to download images in JSON file
        image_download_service = ImageDownloadService(event.src_path)
        image_download_service.parse_json()
        image_download_service.download_images()
        # todo: rescue errors, http request failures

        # Deletes file
        os.remove(event.src_path)

    elif "/original_images_ed" in event.src_path:
        print(f"Image Download Service created {event.src_path} in /original_images_ed!")

        # Initiates Edge Detection Service on original image
        edge_detection_service = ImageEdgeDetectionService(event.src_path)
        edge_detection_service.detect_edges()
        # todo: rescue errors

        # Initializes ImageData object for data analysis and persists with pickle
        image_data = ImageData(image_path=event.src_path, type="original_image")
        save_object(image_data, f"db/image_data/{image_data.uuid}.pkl")
        print(image_data)

        # Saves ImageData object to JSON file in db/json folder
        # todo: extract to separate service
        print(json.dumps(vars(image_data)))
        json_string = json.dumps(vars(image_data))
        json_file = open(f"db/json/{image_data.uuid}.json", "w")
        json_file.write(json_string)
        json_file.close

        # Deletes file
        os.remove(event.src_path)

    elif "/original_images_gp" in event.src_path:
        print(f"Image Download Service created {event.src_path} in /original_images_gp!")

        gnomonic_projector_service = ImageProjectorService(event.src_path)
        print(gnomonic_projector_service.uuid)
        gnomonic_projector_service.project_image()
        # todo: rescue errors

        os.remove(event.src_path)

    elif "/detection_images" in event.src_path:
        print(f"Edge Detection Service created {event.src_path} in /detection_images!")

        image_data = ImageData(image_path=event.src_path, type="edge_detection_image")
        save_object(image_data, f"db/image_data/{image_data.uuid}.pkl")

        print(image_data)
        print(json.dumps(vars(image_data)))
        json_string = json.dumps(vars(image_data))

        # todo: extract to separate service
        json_file = open(f"db/json/{image_data.uuid}_ed.json", "w")
        json_file.write(json_string)
        json_file.close

        os.remove(event.src_path)

    elif "/projector_images" in event.src_path:
        print(f"Projection Service created {event.src_path} in /projector_images!")

        image_data = ImageData(image_path=event.src_path, type="gnomonic_projection")
        save_object(image_data, f"db/image_data/{image_data.uuid}.pkl")

        print(image_data)
        print(json.dumps(vars(image_data)))
        json_string = json.dumps(vars(image_data))

        # todo: extract to separate service
        json_file = open(f"db/json/{image_data.uuid}_gp.json", "w")
        json_file.write(json_string)
        json_file.close

        os.remove(event.src_path)

    else:
        print("File created in unknown directory")


def on_deleted(event):
    print(f"{event.src_path} deleted after process finished.")


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted

path = "assets"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()