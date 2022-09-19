

Install the dependencies with

```
pip install open3d
pip install msgpack-rpc-python
pip install airsim
pip install pandas pillow tqdm
```


### Scripted Recording

In many cases, it may be preferable to automate the data collection process. An example script demonstrating how to generate waypoints in a "lawnmower" pattern is provided in `airsim_collect.py`. It can be run with

```
python airsim_collect.py
```

This script connects to the AirSim drone using the Python API. It tells the drone to start recording and then moves between waypoints. Since the settings file is configured to record only after moving, it collects a new frame at each waypoint. The data is stored in a timestamped folder in your AirSim directory, `C:\Users\<username>\Documents\AirSim`.

The script defines a bounding region around the initial starting location, an altitude, and a step size. The units for working with AirSim are in meters. In the example, the bounds are set to +/- 100 m in the x and y directions, with an altitude of 50 m and a step size of 50 m. After each waypoint is generated, the AirSim API function `simSetVehiclePose` is called to move the drone and record a new frame. A short delay is included to ensure that the data from each waypoint has time to be written to disk. Including a delay can also help with loading assets into the Unreal environment after moving the camera.

This scripting approach can also be used for other collection patterns. Optionally, waypoints could be loaded from an external source, such as a CSV file, and then used to position the drone camera for each frame.

For more interactive control, it may be useful to use the AirSim Image APIs to access the image data directly in the Python code. We recommend the `simGetImages` function call, which can provide multiple image types simultaneously. More information can be found at https://microsoft.github.io/AirSim/image_apis/.

## 3D Reconstruction

The reconstruction script `airsim_reconstruct.py` can be used to build a 3D point cloud from a recorded AirSim sequence. Options are provided to load a specific run by its folder name (timestamp) or to simply reconstruct the last run. Additionally, we can specify a step size to skip frames, a maximum depth distance, and choose whether to save a point cloud for each frame or just the entire combined scene. The option flag `--seg` will use the segmentation colormap instead of the true image colors, and the flag `--vis` will automatically display the result.

Here is the full parameter list for the reconstruction script:

```
>python airsim_reconstruct.py --help
usage: airsim_reconstruct.py [-h] (-r RUN | -l) [-s STEP] [-t DEPTH_TRUNC] [-w] [--seg] [--vis]

optional arguments:
  -h, --help            show this help message and exit
  -r RUN, --run RUN     folder name of the run
  -l, --last            use last run
  -s STEP, --step STEP  frame step
  -t DEPTH_TRUNC, --depth_trunc DEPTH_TRUNC
                        max distance of depth projection
  -w, --write_frames    save a point cloud for each frame
  --seg                 use segmentation colors
  --vis                 show visualization
```

After collecting a data sequence with the `airsim_collect.py` script, we run

```
python airsim_reconstruct.py -l -w --vis
```
This will loop over all the frames in the last recording and show the combined point cloud in an Open3D window. You can navigate the 3D view using the mouse and adjust the point size with the `+`/`-` keys. The position of the camera for each frame is also displayed in this view. The combined point cloud is saved in the recording directory as `points_rgb.pcd` using the commonly used [PCD file format](https://en.wikipedia.org/wiki/Point_Cloud_Library#PCD_File_Format). Since the `-w` parameter is included, the points for each frame are saved in the `points` folder, along with the camera parameters in a 'json' format that is compatible with Open3D. Running the command again with the `--seg` flag will also create point clouds using the segmentation colors.

#Example:
![neighborhood_reconstruction](https://user-images.githubusercontent.com/13792078/190964535-59331162-6d34-44a6-9a3d-9dc3da22cf20.png)

