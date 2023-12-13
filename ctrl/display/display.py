from pathlib import Path
import ctrl.config as config
import subprocess
import cv2


def display_file(file: Path) -> None:
    """Assumes file exists and is a format accepted by cv2"""
    # check if file is a video or  image
    if cv2.VideoCapture(str(file)).isOpened():
        # Open video and display frames
        cap = cv2.VideoCapture(str(file))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow(file.name, frame)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        # Read image and display
        image = cv2.imread(str(file))
        if image is None:
            print(f"Error: Could not read file '{file}'")
            return
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def display_asset(asset_path: Path):
    if asset_path.is_file():

    else:


def usd_record(usd_file: Path, output: Path) -> None:
    """calls usdrecord on USD_FILE and saves to OUTPUT"""
    usdview_path = config.USD_ROOT_PATH / 'bin' / 'usdrecord'
    subprocess.run([usdview_path, usd_file, output])

