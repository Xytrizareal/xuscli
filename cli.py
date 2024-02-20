import argparse
import sys
import os
from pathlib import Path
import json
try:
    import requests
except ImportError:
    os.system(sys.executable + " -m pip install requests")
    import requests

def save_api_key(api_key):
    home = str(Path.home())
    file_path = os.path.join(home, "xytriza")
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path, "uploading-service.json")
    config = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            config = json.load(file)
    config["api_key"] = api_key
    with open(file_path, "w") as file:
        json.dump(config, file, indent=4)
    return True

def get_config(data):
    home = str(Path.home())
    file_path = os.path.join(home, "xytriza", "uploading-service.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            config = json.load(file)
            if data in config:
                return config[data]
    return None

def create_config():
    home = str(Path.home())
    file_path = os.path.join(home, "xytriza")
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path, "uploading-service.json")
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({"api_key": None}, file, indent=4)
    return True

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    try:
        create_config()
    except Exception as e:
        print("Error: " + str(e))
        print("Regenerating config file and trying again...")
        os.remove(os.path.join(str(Path.home()), "xytriza", "uploading-service.json"))
        create_config()

    parser = argparse.ArgumentParser(description="Xytriza's Uploading Service CLI")
    parser.add_argument('--config', type=str, help='Use this option to save your API key. Example: --config apikey=your_api_key_here')
    parser.add_argument('--upload', type=str, help='Use this option to upload a file to the server. Example: --upload filepath')
    parser.add_argument('--delete', type=str, help='Use this option to delete a file from the server. Example: --delete deletion_key')

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.config:
        if args.config.startswith("apikey="):
            key = args.config.split("=")[1]
            response = requests.get("https://upload.xytriza.com/api/checkAPIKey.php", headers={"key": key})
            data = response.json()
            if data["success"] == 'true' and response.status_code == 200:
                save_api_key(key)
                print("API key saved successfully")
            else:
                print("Error: " + data["response"] + " - " + str(response.status_code))
        else:
            print("Invalid argument")

    if args.upload:
        api_key = get_config("api_key")
        if api_key is not None:
            with open(args.upload, "rb") as file:
                response = requests.post("https://upload.xytriza.com/api/uploadFile.php", files={"file": file}, headers={"key": api_key})
            data = response.json()

            if data["success"] == True and response.status_code == 200:
                print("File uploaded successfully")
                print("File URL: " + data["fileUrl"])
                print("Deletion URL: " + data["deletionUrl"])
                print("Deletion Key: " + data["deletionKey"])
            else:
                print("Error: " + data["response"] + " - " + str(response.status_code))
        else:
            print("API key not found. Please save your API key using --config apikey=your_api_key_here")

    if args.delete:
        deletionkey = args.delete
            
        response = requests.get("https://upload.xytriza.com/api/deleteFile.php", headers={"deletionkey": deletionkey})
        data = response.json()

        if data["success"] == True and response.status_code == 200:
            print("File deleted successfully")
        else:
            print("Error: " + data["response"] + " - " + str(response.status_code))