# get image stream from raspberry pi camera
from EI.hw import is_raspberry_pi
import time
import matplotlib.pyplot as plt
from EI.FastSAM.fastsam import FastSAM, FastSAMPrompt

on_device = is_raspberry_pi()
if on_device:
    from picamera2 import Picamera2


frame_path = "/tmp/frame.png" if on_device else "./tests/hawksbill_sea_turtle.jpg"
annotated_path = "/tmp/aframe.png"
modelPath = "./EI/checkpoints/FastSAM-x.pt"
DEVICE = "cpu"

sensor_size = [640, 480]


class SegmentConnector:
    def __init__(self):
        self.model = FastSAM(modelPath)
        if on_device:
            self.cap = Picamera2()
            camera_config = self.cap.create_preview_configuration()
            self.cap.configure(camera_config)
            self.cap.start()

    def start(self):
        time.sleep(0.2)
        if on_device:
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

        # save the image for debug purpose
        plt.savefig(annotated_path)

        # Crop the show image to square from centre
        s = min(show.shape[0], show.shape[1])
        show = show[(show.shape[0] - s) // 2:(show.shape[0] + s) // 2, (show.shape[1] - s) // 2:(show.shape[1] + s) // 2]

        return show


if __name__ == "__main__":
    segment = SegmentConnector()
    show = segment.start()
    plt.imshow(show)
    plt.show()
