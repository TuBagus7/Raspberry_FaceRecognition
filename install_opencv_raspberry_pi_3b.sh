mkdir opencv
cd opencv

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install build-essential cmake pkg-config -y
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev -y
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
sudo apt-get install libxvidcore-dev libx264-dev -y
sudo apt-get install libgtk2.0-dev libgtk-3-dev -y
sudo apt-get install libatlas-base-dev gfortran -y
sudo apt-get install python2.7-dev python3-dev -y

wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.1.zip
unzip opencv.zip

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py

sudo pip install numpy

cd opencv-3.3.1
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j2
sudo make install
sudo ldconfig

sudo find /usr/local/lib -type f -name "cv2.*.so" -exec sh -c 'x="{}"; echo mv "$x" "$(dirname ${x})/cv2.so"' \;

echo "OpenCV is successfully installed"
