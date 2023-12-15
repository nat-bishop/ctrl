from pathlib import Path
import ctrl.config as config
import ctrl.utils.helpers as helpers
import ctrl.utils.constants as constants
import subprocess
import cv2
import click


def display_project_output(proj_path: Path) -> None:
    """Displays files in PROJ_PATH/outputs if they are supported.

    If there is a directory, it displays all supported files in the directory"""
    video_formats = ['.mov']
    image_formats = ['.png']

    output_path = proj_path / 'outputs'
    display_files = helpers.get_subfiles(output_path)
    for asset_dir in helpers.get_subdirs(output_path):
        display_files += helpers.get_subfiles(asset_dir)

    for file in display_files:
        if file.suffix in video_formats:
            display_video(file)
        elif file.suffix in image_formats:
            display_image()
        elif file.suffix == '.usd':
            display_usd(file)
        else:
            click.echo(f"error, file format '{file.suffix}' is not supported")


def display_image(path: Path) -> None:
    # Read image and display
    image = cv2.imread(str(path))
    if image is None:
        print(f"Error: Could not read file '{path}'")
        return
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_video(path: Path) -> None:
    cap = cv2.VideoCapture(str(path))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(path.name, frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def display_usd(usd_path: Path) -> None:
    """display USD_PATH with usdview"""
    usdview_path = Path(config.USD_ROOT_PATH, 'scripts', 'usdview.bat')
    subprocess.run([str(usdview_path), str(usd_path), '--defaultsettings'])
