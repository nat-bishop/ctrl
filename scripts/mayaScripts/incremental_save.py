import maya.cmds as cmds
import time
import pymel.core as pm


def save_scene(full_path):
    """
    Save the current scene
    :param str full_path: Path to save the file to.
    """
    file_type = 'mayaAscii' if full_path.endswith('ma') else 'mayaBinary'
    cmds.file(rename=full_path)
    cmds.file(save=True, type=file_type, force=True)
    pm.displayInfo(f'saved to {full_path}')

def increment_save():
    """
    Save the current scene incrementally with time.
    """
    current_scene_name = cmds.file(query=True, sceneName=True)

    if current_scene_name:
        string_time = time.strftime("%y%m%d_%H%M")
        file_info, extension = current_scene_name.split('.')
        project_name, file_name, file_type, yymmdd, hhmm = file_info.split('_')
        new_scene_name = f'{project_name}_{file_name}_{file_type}_{string_time}.{extension}'
        save_scene(new_scene_name)
    else:
        cmds.warning('Please save your scene first.')


if __name__ == '__main__':
    increment_save()
