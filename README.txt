For click autocompletion:
save "source /c/ctrl/scripts/.ctrl-complete.bash" to ~/.bashrc      (or whereever the root directory is)

Add uiready.py to houdini startup script pythonX.Ylibs/uiready.py

Used in houdini.py:
HYTHON_PATH = "C:\Program Files\Side Effects Software\Houdini 20.0.506\bin\hython3.10.exe"



./.venv\scripts\activate
pip install --editable .

Structure of files:
projectName_fileName_type_YYMMDD_HHMM.ext
type_options= model, render, sim, ref, diffuse

Structure of folders:
projects/
    2023/
        nureShark/
            houdini/
                projectFiles/
                    nurseShark_noTail_model_230420_1920.mb
                    nurseShark_withTail_model_230420_1002.mb
                exports/
                    nurseShark_swimmingSplash_sim_230419_0920.fbx
            maya/
            outputs/
                nurseShark_shark_render_2304210654.mov
            references/
                nurseShark_sideView_ref_23170303.png
            assets/
                redMetal/
                    nurseShark_redMetal_diffuse_23170303.png
