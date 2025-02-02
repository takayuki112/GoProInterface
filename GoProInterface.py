import requests
import time
import yaml

class GoProInterface:
    def __init__(self, ip):
        print("\n\nInitializing GoPro Interface for IP - ", ip)
        self.ip = ip
        self.base_url = "http://" + ip + "/gopro"
        self.yaml_path = "./metadata.yaml"
       
    def enable_usb_control(self):
        enable_url = self.base_url + "/camera/control/wired_usb"
        response = requests.request("GET", enable_url, params={"p":"1"})
        
        if response.status_code != 200:
            print("Status code from initialization - ", response.status_code)
        else:
            print("Initialized USB successfully!")   
        return response.status_code 
    
    def disable_usb_control(self):
        disable_url = self.base_url + "/camera/control/wired_usb"
        response = requests.request("GET", disable_url, params={"p":"0"})
        if response.status_code != 200:
            print("Status code from disabling usb - ", response.status_code)
        else:
            print("Disabled USB successfully!")
        return response.status_code
        
    def start_recording(self):
        url = self.base_url + "/camera/shutter/start"
        response = requests.request("GET", url)
        timestamp = time.time_ns()
        
        if response.status_code == 200:
            print("Started Recording at timestamp - ", timestamp)
            return timestamp
        else:
            print("Failed to start recording at timestamp - ", timestamp, "status code - ", response.status_code)
            

    def stop_recording(self):
        url = self.base_url + "/camera/shutter/stop"
        response = requests.request("GET", url)
        timestamp = time.time_ns()
        time.sleep(1)
        if response.status_code == 200:
            print("Stopped Recording at timestamp - ", timestamp)
            print("File saved at - ", self.get_last_media_path())
            return self.get_last_media_path(), timestamp
        else:
            print("Failed to stop recording at timestamp - ", timestamp, "status code - ", response.status_code)
            return None, None
            
    def get_last_media_path(self):
        url = self.base_url + "/media/list"
        response = requests.request("GET", url)
        print("Media response status code - ", response.status_code)
        last_dir = response.json()['media'][-1]
        filename = last_dir['fs'][-1]['n']
        path = last_dir['d'] + "/" + filename
        return path        
    
    def append_metadata(self, metadata):
        with open(self.yaml_path, 'a') as file:
            yaml.dump(metadata, file)
        
    
    # __unused__
    def get_media_list(self):
        url = self.base_url + "/media/list"
        response = requests.request("GET", url)
        print("Media response status code - ", response.status_code)
        
        response_media = response.json()['media']
        # print("Number of Directories - ", len(response_media))
        
        # for directory in response_media:
        #     print(directory['d'])
        #     for file in directory['fs']:
        #         print(file['n'])
        #     print("\n\n")
        
        last_dir_array = response_media[-1]['fs']
        for dict in last_dir_array:
            print(dict['n'], "created - ", dict['cre'])
        
        # print("Response media - ", response_media)
        
        # for k, v in response_media.items():
        #     print(k, v)
        #     print("\n")
        # for item in response_media_dict:
        #     print(item)
        #     print("\n\n")
        

def test():
    ip_1 = "172.20.134.51:8080"
    gopro1 = GoProInterface(ip_1)
    gopro1.enable_usb_control()
    gopro1.start_recording()
    time.sleep(2)
    gopro1.stop_recording()
    gopro1.disable_usb_control()
    print("Done recording!\n\n")
    time.sleep(1)
    
    gopro1.get_media_list() 
    print("Saved at - ", gopro1.get_last_media_path())
test()