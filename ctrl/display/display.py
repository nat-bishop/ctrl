from pathlib import Path
import ctrl.config as config
import ctrl.utils.helpers as helpers
import subprocess
import cv2
import click


def display_project_output(proj_name: str) -> None:
    """Displays files in PROJ_PATH/outputs if they are supported.

    If there is a directory, it displays all supported files in the directory"""
    video_formats = ['.mov']
    image_formats = ['.png', '.jpg']

    proj_path = helpers.get_proj_path(proj_name)
    if not proj_path:
        click.echo("error, project not found")
        exit(1)

    output_path = proj_path / 'outputs'
    display_files = helpers.get_subfiles(output_path)
    for asset_dir in helpers.get_subdirs(output_path):
        display_files += helpers.get_subfiles(asset_dir)

    for file in display_files:
        if file.suffix in video_formats:
            click.echo(f'opening video: {file.name} from project: {proj_name}')
            display_video(file)
        elif file.suffix in image_formats:
            click.echo(f'opening image: {file.name} from project: {proj_name}')
            display_image(file)
        elif file.suffix == '.usd':
            click.echo(f'opening usd file: {file.name} from project: {proj_name}')
            display_usd(file)
        else:
            click.echo(f"error, file format '{file.suffix}' is not supported")


def display_image(path: Path) -> None:
    # Read image and display
    image = cv2.imread(str(path))
    if image is None:
        print(f"Error: Could not read file '{path}'")
        return
    click.echo(f"displaying image '{path.name}'")
    ims = cv2.resize(image, (1920, 1080))
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_video(path: Path) -> None:
    cap = cv2.VideoCapture(str(path))
    click.echo(f"displaying video '{path.name}', press q to exit")
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
    click.echo(f"displaying usd file: {usd_path.name} with 'usdview'")
    subprocess.run([str(usdview_path), str(usd_path), '--defaultsettings'])
