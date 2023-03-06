import os
from pathlib import Path
import supervisely as sly
from dotenv import load_dotenv

load_dotenv("local.env")

app_root_directory = str(Path(__file__).parent.absolute().parents[0])
app_data_dir = os.path.join(app_root_directory, "tempfiles")
output_project_dir = os.path.join(app_data_dir, "output_project_dir")
static_dir = Path(os.path.join(app_data_dir, "preview_files"))

app_session_id = sly.io.env.task_id()

local_preview_path = os.path.join(static_dir, "preview.jpg")
remote_preview_path = os.path.join(
    "Apply_Object_Segmentor_to_Images_Project",
    str(app_session_id),
    "preview.jpg",
)
