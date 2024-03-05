from concurrent import futures
import grpc
import network_pb2
import network_pb2_grpc
import requests
import sys
import socket


class NodeService(network_pb2_grpc.NodeServiceServicer):
    def SendDownload(self, request, context):
        print(f"Peer received download message: {request.content}")
        

        port = int(sys.argv[2])
        downloading_uploading(port,"I'm uploading the file, so you can downloaded", "upload")
        return network_pb2.Message(content="File downloaded successfully.")

    def SendUpload(self, request, context):
        print(f"Peer received upload message: {request.content}")
        
        return network_pb2.Message(content="File uploaded successfully.")

def run_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    network_pb2_grpc.add_NodeServiceServicer_to_server(NodeService(), server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    print("Server started on port", port)
    server.wait_for_termination()

def downloading_uploading(peer_port, message, method):
    with grpc.insecure_channel(f"localhost:{peer_port}") as channel:
        stub = network_pb2_grpc.NodeServiceStub(channel)
        if method == 'download':
            response = stub.SendDownload(network_pb2.Message(content=message))
        elif method == 'upload':
            response = stub.SendUpload(network_pb2.Message(content=message))
        print("Response:", response.content)


class Pclient:
    def __init__(self,name, port):
        self.name = name
        self.port = port
        self.main_menu_options = {
            '1': 'Login',
            '2': 'Logout',
            '3': 'Index files',
            '4': 'Search files'
        }

        self.submenu_options = {
            '1': 'Suboption 1',
            '2': 'Suboption 2',
            '3': 'Go back to main menu'
        }

    def display_menu(self, options):
        print("Menu:")
        for key, value in options.items():
            print(f"{key}. {value}")

    def run(self):
        try:
            while True:
                self.display_menu(self.main_menu_options)
                choice = input("Enter your choice: ")

                if choice == '1':
                    api_url = "http://127.0.0.1:5000/login"
                    password = input("Enter your password: ")
                    url = f"https://localhost:{self.port}"
                    data_to_send = {'username': self.name, 'password': password, "url": url}
                    
                    response = requests.post(api_url, json=data_to_send)

                    if response.status_code == 200:
                        print(response.json())
                    else:
                        print(f"Error: {response.status_code}")

                elif choice == '2':
                    api_url = "http://127.0.0.1:5000/logout"
                    
                    data_to_send = {'username': self.name}
                    
                    response = requests.post(api_url, json=data_to_send)

                    if response.status_code == 200:
                        print(response.json())
                    else:
                        print(f"Error: {response.status_code}")
                elif choice == '3':
                    api_url = "http://127.0.0.1:5000/indexFiles"
                    
                    files = input("Enter your files separated by coma (,): ")
                    data_to_send = {'username': self.name, 'files': files }
                    
                    response = requests.post(api_url, json=data_to_send)

                    if response.status_code == 200:
                        print(response.json())
                    else:
                        print(f"Error: {response.status_code}")
                elif choice == '4':
                    api_url = "http://127.0.0.1:5000/searchFiles"
                    
                    file = input("Enter the file you want to search: ")
                    data_to_send = {'username': self.name, 'file': file }
                    response = requests.get(api_url, json=data_to_send)
                    if response.status_code == 200:
                        res = response.json()
                        print()
                        last_occurrence_column = res['url'].rfind(":")
                        last_occurrence_backslash = res['url'].rfind("/")
                        client_peer_port = res['url'][last_occurrence_column + 1:last_occurrence_backslash]
                        file = res['url'][last_occurrence_backslash + 1:]
                        message = f"I have to download the file: {file}"
                        downloading_uploading(int(client_peer_port), message, "download")

                        print("Downloading file... ")
                        api_url = "http://127.0.0.1:5000/indexFiles"
                        data_to_send = {'username': self.name }
                        response = requests.get(api_url, json=data_to_send)

                        if response.status_code == 200:
                            res = response.json()
                            files = res['files']
                            arrFiles = files.split(',')
                            arrFiles.append(file)
                            result_string = ','.join(arrFiles)
                            print("result_string", result_string)
                            data_to_send = {'username': self.name, 'files': result_string }

                            response = requests.post(api_url, json=data_to_send)

                            if response.status_code == 200:
                                print("File Donwloaded succesfully!")
                    else:
                        print(f"Error: {response.status_code}")
                else:
                    print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            
            api_url = "http://127.0.0.1:5000/logout"
            data_to_send = {'username': self.name}
            response = requests.post(api_url, json=data_to_send)

            if response.status_code == 200:
                print(response.json())
            else:
                print(f"Error: {response.status_code}")
    def run_submenu(self):
        while True:
            self.display_menu(self.submenu_options)
            choice = input("Enter your choice: ")

            if choice == '1':
                pass

                
            elif choice == '2':
                print("You selected Suboption 2.")
            elif choice == '3':
                print("Going back to the main menu.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Use: python peer.py <name> <port>")
        sys.exit(1)

    
    name = sys.argv[1]
    port = int(sys.argv[2])
    
    server_thread = futures.ThreadPoolExecutor(max_workers=1).submit(run_server,port)

    
    pclient = Pclient(name=name, port=port)
    pclient.run()

    
    server_thread.result()
