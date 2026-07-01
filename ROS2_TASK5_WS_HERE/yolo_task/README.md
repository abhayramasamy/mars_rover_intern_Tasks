# TASK OF IMPLEMENTING cone detection using a YOLO model
This task requests us to design a custom yolo model to enable it to detect cones if present in the gazebo world and als differentiate the cones based on colour. *Special point to take care of: Model must detect cones comfortably in both real life as well as simulation...*


## Model descriptions: 
I trained two different YOLO models:
1) version 1) yolov8nano trained on real life cones first and finetuned off Gazebo images (2nd training iteration) using a **a node to screenshot the camera frames being published off /camera/image_raw/ topic and store it automatically** about ~160 images collected to fine tune the model to adapt to the gazebo world's rendering as well. The model detects cones and returns a Bounding Box with coordinates a separate *opencv* based pipeline present to check for the dominant hue present inside the Bounding Box and differentiate it based off colour.

2) *improvements:* By finetuning on custom dataset, the model can comfortably detect far placed cones or partially hidden cones with good confidence. Adjust to varying lighting and textures would not have been possible from real life scenarios too.

3) *Problems:* Weak generalization to new colours can only reliably detect red, blue, yellow, green, pink. purple and ignores other miscellaneous colours like drab_orange or white.

4) version 2) An upgraded Yolo26Nano model that it trained off real life cones but carries internal data augmentation *to try to reduce colour bias of the model and force it generalize to cone texture and shape*, works well on real life cones. Slight augmentation applied during training phase on Gazebo images, some pipeline changes implemented to allow for unknown colours. Now the model can check for cones for other non standard colours if necessary. 

5) *Problems:* the model has room for improvement due to textural noise on simulation data. 


## Links of work referenced:
1) *ULtralytics model stats to view* [https://platform.ultralytics.com/25f2001635-abhay-ramasamy/yolocones] 
2) *Annotated Gazebo images on Roboflow*[Custom Dataset: https://app.roboflow.com/abhay-ramasamy/gazebo_cones_dataset/]

## concepts learnt:
1) Collecting dataset carefully to match expectations and appropriate train/train-dev/dev/test distributions to try to achieve best results on both real world cones and as well on Simulation. 

2) Using a Gazebo camera based screenshotter node and Annotating custom dataset on `roboflow`.

3) Training, testing, validating models using `Ultralytics` and `google colab`.

4) Performing analysis using error metrics and improve models in iterations.

5) Data augmentation to introduce variations in dataset (*used in training of version 2*).

6) opencv based detection and display pipeline.

7) Communication inside a python virtual machine using zmq.

## issues faced:

1) version control issues avoided using `python virtual machine` 

2) Still not perfectly favarouble metrics due to Noise introduced from GAzebo dataset causing data_mismatch this is a necessary evil to help the model to generalize properly.


## how to run?
1) One need a python virtual machine use: `venv` to run. 
2) load the `aruco_cv` workspace from and build from the src directory using `colcon build`, download the required model files.
3) Download the world sdf files from `worlds` directory.
4) from scripts download the two launch files `yolo_launch.py yolo_launch_mc.py yolo_server_node.py`.*check file paths inside these folders*
5) One might need a python virtual machine to safely run the model without breaking system packages.
6) In a fresh terminal configure and activate a `venv`, with latest versions of `Ultralytics, opencv-python-heaadless, numpy, pyzmq`. then run `python3 yolo_server_node.py`.
7) To launch `yolo_test_world_v2_lowphysics.sdf` you need to run: `ros2 launch yolo_launch_mc.py`, to launch the training world you need to run `ros2 launch yolo_launch.py`.
8) Finally in another terminal after building the `aruco_cv` workspace and after sourcing it, run: `ros2 run aruco_cv yolo` to launch model: yolov8n or use `yolo_mc` to launch yolo26n version. 
9) An Opencv terminal with gazebo shows up and the cones are demarcated and displayed as such.

## screenshots:
Screenshots of the demo are included in the *Screenshots* folder.
