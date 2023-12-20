import hrpyc
import sys
from datetime import datetime
import ctrl.utils.helpers as helpers


def save(args):
    try:
        connection, hou = hrpyc.import_remote_module(port=18812)
    except ConnectionRefusedError:
        print("could not connect to open houdini session.")
        sys.exit()

    try:
        project_name, file_name, file_type, time, extension = helpers.extract_filename(hou.hipFile.basename())
    except ValueError:
        print("could not extract filename from {}".format(hou.hipFile.basename()))
        sys.exit()

    if args.name:
        file_name = args.name

    if args.type:
        file_type = args.type

    final_name = helpers.construct_filename(project_name, file_name, file_type, datetime.now(), extension)
    save_path = helpers.get_proj_path(project_name) / 'houdini' / 'projectFiles' / final_name
    hou.hipFile.save(str(save_path))
    print(f"saved file to: {hou.hipFile.path()}")
    hou.releaseLicense()


if __name__ == "__main__":
    # Get command line arguments
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--name")
    parser.add_argument("--type")
    args = parser.parse_args()

    save(args)
