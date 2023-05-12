FROM ubuntu:latest
RUN apt-get update && apt-get install -y git && apt-get install -y python3 && apt-get install -y python3-pip
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip \
    pip install --no-cache-dir -r requirements.txt
RUN git clone --depth=1 https://github.com/XuehaiPan/nvitop.git && cd nvitop && bash install-nvidia-driver.sh --latest 
COPY exporters.py exporters.py
CMD ["python", "exporters.py"]