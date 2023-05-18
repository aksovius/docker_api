#python class template for docker controler
import docker

class DockerController:
    def __init__(self):
        self.client = docker.from_env()

    def list_containers(self):
        containers = self.client.containers.list()
        for container in containers:
            print(container.name)
        return containers

    def create_container(self, image, command, detach=True, name=None, ports=None, volumes=None):
        container = self.client.containers.run(
            image=image,
            command=command,
            detach=detach,
            name=name,
            ports=ports,
            volumes=volumes
        )
        return container

    def stop_container(self, container):
        container.stop()

    def remove_container(self, container):
        container.remove()

    def list_images(self):
        images = self.client.images.list()
        return images

    def pull_image(self, image):
        self.client.images.pull(image)

    def remove_image(self, image):
        self.client.images.remove(image)
        
    def start_containers(self,number):
        exist = 0
        for gpu in range(4):
            for device in range (7):
                if (exist < number):
                    container = self.client.containers.run(
                        'tf2:0.05', 
                        detach=True, 
                        ports={'8080/tcp': 8080+exist}, 
                        volumes={'/home/gil/Desktop/colab/': {'bind': '/home/user/workdir/data', 'mode': 'ro'}, 
                                '/home/gil/Desktop/alexander/code-server/user_dir': {'bind': '/home/user/workdir/example', 'mode': 'ro'},
                                '/etc/timezone': {'bind': '/etc/timezone', 'mode': 'ro'}, 
                                '/etc/localtime': {'bind': '/etc/localtime', 'mode': 'ro'},
                                '/home/gil/Desktop/alexander/code-server/config.yaml': {'bind': '/home/user/.config/code-server/config.yaml', 'mode': 'ro'}}, 
                        shm_size='1g', 
                        environment=['TZ=Asia/Seoul'], 
                        remove=False, 
                        name='container_'+str(exist),
                        device_requests=[{'DeviceIDs': [f'{gpu}:{device}'],
                                        'Capabilities': [['gpu']],
                                        }], 
                        command='code-server',
                        entrypoint='bash')
                    exist += 1
                    print("Run: " + container.short_id  + " gpu: " + str(gpu) + " device: " + str(device))
    def load_all_containers(self):
        for container in self.client.containers.list():
            if container.image.tags == ['tf2:1.0']:
                container.exec_run('conda run -n tf python /home/user/workdir/example/unet.py', detach=True)
    def load_one(self, id):
        for container in self.client.containers.list():
            if container.short_id == id:
                container.exec_run('conda run -n tf python /home/user/workdir/example/unet.py', detach=True)
                
    def start_one(self, name:str, port:int, gpu:int, device:int, user_dir:str):
        container = self.client.containers.run(
                    'tf2:0.05', 
                    detach=True, 
                    ports={'8080/tcp': port}, 
                    volumes={'/home/gil/Desktop/colab/': {'bind': '/home/user/workdir/data', 'mode': 'ro'}, 
                            '/home/gil/Desktop/alexander/code-server/user_dir': {'bind': '/home/user/workdir/example', 'mode': 'ro'},
                            '/etc/timezone': {'bind': '/etc/timezone', 'mode': 'ro'}, 
                            '/etc/localtime': {'bind': '/etc/localtime', 'mode': 'ro'},
                            '/home/gil/Desktop/alexander/code-server/config.yaml': {'bind': '/home/user/.config/code-server/config.yaml', 'mode': 'ro'},
                            '/home/gil/Desktop/users_data/'+ user_dir : {'bind': '/home/user/workdir', 'mode': 'rw'}
                            }, 
                    shm_size='1g', 
                    environment=['TZ=Asia/Seoul'], 
                    remove=False, 
                    name=name,
                    device_requests=[{'DeviceIDs': [f'{gpu}:{device}'],
                                    'Capabilities': [['gpu']],
                                    }], 
                    command='code-server',
                    entrypoint='bash')
        print("Run: " + container.short_id  + " gpu: " + str(gpu) + " device: " + str(device))