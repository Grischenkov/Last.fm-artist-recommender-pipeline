import requests

def update_server():
    requests.post(f"http://http://87.239.106.15:8080/update")

if __name__ == "__main__":
    update_server()