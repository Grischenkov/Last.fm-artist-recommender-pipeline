import requests

def update_server():
    try:
        requests.post(f"http://http://87.239.106.15:8080/update")
    except:
        pass

if __name__ == "__main__":
    update_server()
