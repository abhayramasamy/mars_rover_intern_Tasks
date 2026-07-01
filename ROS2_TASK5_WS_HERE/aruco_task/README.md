# TASK OF IMPLEMENTING ARUCO MARKER DETECTION USING OPENCV2 AND PUBLISHING TRANSFORMS (pose):
In this task we are implementing Aruco detection on opencv using one of the cameras to see the markers. identify them, detect them and then apply `singlePoseEstimation` to detect the pose of the Aruco markers w.r.t to camera link and display them on RVIZ2.

## what the project will do?
The project when run will display the aruco marker detection using opencv (in a imwindow) and also publishes transforms from `camera_link` as base to tf structure to be displayable on RViz2.

## concepts learnt:
1) aruco markers types, id's and textures.
2) spawnining custom textures on Gazebo to display aruco markers.
3) proper cv2 pipeline to detect arucomarkers, iding them.
4) estimating the pose vectors from `singlePoseEstimation` and publishing the tf tree onto Rviz2 for visualization.


## issues faced:
1) opencv2 versioning issues, and version mismatch due to cv_bridge() requirirng an older version of numpy.
2) I was unable to create a proper texture and I was unable to import any aruco_markers properly so iam forced to import textures and a generator script to create the aruco "boxes" with markers on them from repository: [https://github.com/SaxionMechatronics/ros2-gazebo-aruco]

> *versions: to ensure it runs for ROS2 humble* <br/>
> 1) opencv --> 4.5.x
> 2) numpy --> 1.26.x


## How to launch...
1)  Download the following: `Aruco_WS`, `launch` and `worlds`, `models`, `meshes`
2) 	A small extra point: if one needs custom Aruco Markers of a different dictionary, padding, markers etc one needs to downlaoad and run `scripts/create_marker_tile_image.py` make required changes in the code and pass arguments `--tile size and --marker_fraction` to adjust sizes on `aruco_box` textures and replace the image generated inside `meshes/aruco_box/materials/textures` to apply changes.
3) Observe the downloaded files and change the file paths inside each code carefully.
4) build the packages inside `Aruco_WS` by simply `colcon build` on workspace directory.
5) run: `ros2 launch aruco_launch` 
6) run: `ros2 run aruco_cv aruco_tf` from the `Aruco_WS` directory.
7) run `rviz2` open it, click on add "tf" and change fixed frame to `camera_link` now visualize.

## screenshots:
1) screenshots of the aruco marker detection, and rviz2 tf structure is present inside *screenshots* folder.

