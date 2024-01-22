# get image stream from raspberry pi camera

from picamera2 import Picamera2
import time
import matplotlib.pyplot as plt
from EI.FastSAM.fastsam import FastSAM, FastSAMPrompt


frame_path = "/tmp/frame.png"
annotated_path = "/tmp/aframe.png"
modelPath = "./EI/checkpoints/FastSAM-x.pt"
DEVICE = "cpu"

sensor_size = [640, 480]


class SegmentConnector:
    def __init__(self):
        self.cap = Picamera2()
        camera_config = self.cap.create_preview_configuration()
        self.cap.configure(camera_config)
        self.cap.start()
        self.model = FastSAM(modelPath)

    def start(self):
        time.sleep(0.2)
        self.cap.capture_file(frame_path)

        # Implement SAM here
        results = self.model(frame_path, device=DEVICE, imgsz=sensor_size)
        prompt_process = FastSAMPrompt(frame_path, results, device=DEVICE)

        # Prompt at the central point
        margin = 100
        prompt_box = [margin, margin, sensor_size[0] - margin, sensor_size[1] - margin]

        annotations = prompt_process.box_prompt(bbox=prompt_box)

        plt.style.use('dark_background')
        ax = plt.subplot(1, 1, 1)
        # Hide everything
        ax.set_axis_off()
        # Make the image fill the whole space
        ax.set_position([0, 0, 1, 1])
        # Show the mask
        show = prompt_process.fast_show_mask_outline(annotations, ax, random_color=True)

        # save the image
        plt.savefig(annotated_path)

        # return the ax plot as a numpy array
        return plt.imread(annotated_path)
