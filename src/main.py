import os
from pathlib import Path
import numpy as np
import random
import supervisely as sly
import src.globals as g
from dotenv import load_dotenv
import yaml
from supervisely.app.widgets import (
    Container,
    Card,
    SelectAppSession,
    RadioGroup,
    Input,
    Button,
    Field,
    Progress,
    SelectDataset,
    LabeledImage,
    ModelInfo,
    ClassesTable,
    DoneLabel,
    ProjectThumbnail,
    Editor,
    Select,
)


# function for updating global variables
def update_globals(new_dataset_ids):
    global dataset_ids, project_id, workspace_id, project_info, project_meta
    dataset_ids = new_dataset_ids
    if dataset_ids:
        project_id = api.dataset.get_info_by_id(dataset_ids[0]).project_id
        workspace_id = api.project.get_info_by_id(project_id).workspace_id
        project_info = api.project.get_info_by_id(project_id)
        project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
        print(f"Project is {project_info.name}, {dataset_ids}")
    elif project_id:
        workspace_id = api.project.get_info_by_id(project_id).workspace_id
        project_info = api.project.get_info_by_id(project_id)
        project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
    else:
        print("All globals set to None")
        dataset_ids = []
        project_id, workspace_id, project_info, project_meta = [None] * 4


# authentication
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api()
team_id = sly.env.team_id()

# if app had started from context menu, one of this has to be set:
project_id = sly.env.project_id(raise_not_found=False)
dataset_id = sly.env.dataset_id(raise_not_found=False)
dataset_ids = [dataset_id] if dataset_id else []
project_meta = None
preview_project_meta = None
update_globals(dataset_ids)

sly.logger.info(f"App root directory: {g.app_root_directory}")
# dictionary for storing object segmentation model data
model_data = {}


### 1. Dataset selection
dataset_selector = SelectDataset(project_id=project_id, multiselect=True, select_all_datasets=True)
select_data_button = Button("Select data")
select_done = DoneLabel("Successfully selected input data")
select_done.hide()
reselect_data_button = Button(
    '<i style="margin-right: 5px" class="zmdi zmdi-rotate-left"></i>Reselect data',
    button_type="warning",
    button_size="small",
    plain=True,
)
reselect_data_button.hide()
project_settings_content = Container(
    [
        dataset_selector,
        select_data_button,
        select_done,
        reselect_data_button,
    ]
)
card_project_settings = Card(title="Dataset selection", content=project_settings_content)


### 2. Connect to object segmentation model
select_model = SelectAppSession(team_id=team_id, tags=["deployed_nn_object_segmentation"])
connect_model_button = Button(
    text='<i style="margin-right: 5px" class="zmdi zmdi-power"></i>connect to object segmentation model',
    button_type="success",
)
connect_model_done = DoneLabel("Object segmentation model connected")
connect_model_done.hide()
model_info = ModelInfo()
change_model_button = Button(
    '<i style="margin-right: 5px" class="zmdi zmdi-rotate-left"></i>change object segmentation model',
    button_type="warning",
    button_size="small",
    plain=True,
)
change_model_button.hide()
connect_model_content = Container(
    [
        select_model,
        connect_model_button,
        connect_model_done,
        model_info,
        change_model_button,
    ]
)
card_connect_model = Card(
    title="Connect to Object Segmentation Model",
    description="Select served object segmentation model from list below",
    content=connect_model_content,
    collapsable=True,
    lock_message="Complete the previous step to unlock",
)
card_connect_model.collapse()
card_connect_model.lock()


### 3. Project classes
classes_table = ClassesTable()
select_classes_button = Button("select classes")
select_classes_button.hide()
select_other_classes_button = Button(
    '<i style="margin-right: 5px" class="zmdi zmdi-rotate-left"></i>select other classes',
    button_type="warning",
    button_size="small",
    plain=True,
)
select_other_classes_button.hide()
classes_done = DoneLabel()
classes_done.hide()
classes_content = Container(
    [
        classes_table,
        select_classes_button,
        select_other_classes_button,
        classes_done,
    ]
)
card_classes = Card(
    title="Project Classes",
    description="Choose classes that will be kept after prediction, other classes will be ignored",
    content=classes_content,
    collapsable=True,
    lock_message="Complete the previous step to unlock",
)
card_classes.collapse()
card_classes.lock()


### 4.1 Model settings
model_settings_editor = Editor(language_mode="yaml", height_lines=30)
save_model_settings_button = Button("save model settings")
reselect_model_settings_button = Button(
    '<i style="margin-right: 5px" class="zmdi zmdi-rotate-left"></i>reselect model settings',
    button_type="warning",
    button_size="small",
    plain=True,
)
reselect_model_settings_button.hide()
model_settings_done = DoneLabel("Model settings saved")
model_settings_done.hide()
model_settings_content = Container(
    [
        model_settings_editor,
        save_model_settings_button,
        reselect_model_settings_button,
        model_settings_done,
    ]
)
card_model_settings = Card(
    title="Model Settings",
    content=model_settings_content,
    collapsable=True,
    lock_message="Complete the previous step to unlock",
)
card_model_settings.collapse()
card_model_settings.lock()


### 4.2 Inference preview
redraw_image_button = Button(
    '<i style="margin-right: 5px" class="zmdi zmdi-image"></i>preview',
    button_type="warning",
    button_size="small",
    plain=True,
)
select_preview = Select(items=[Select.Item(value="Random image")])
preview_params = Container(
    [redraw_image_button, select_preview],
    direction="horizontal",
    fractions=[1, 1],
)
labeled_image = LabeledImage(fill_rectangle=False)
preview_content = Container(
    [
        preview_params,
        labeled_image,
    ]
)
card_preview = Card(
    title="Inference preview",
    content=preview_content,
    collapsable=True,
    lock_message="Choose model settings to unlock",
)
card_preview.collapse()
card_preview.lock()
settings_preview_content = Container(
    widgets=[card_model_settings, card_preview],
    direction="horizontal",
    fractions=[1, 1],
)


### 5. Output project
select_output_format = RadioGroup(
    items=[
        RadioGroup.Item(value="save labeled images to new project"),
        RadioGroup.Item(value="add labeled images to selected project"),
    ],
    direction="vertical",
)
select_output_format_f = Field(select_output_format, "Select output format")
output_project_name_input = Input(value="Labeled project")
output_project_name_input_f = Field(output_project_name_input, "Output project name")
apply_model_to_project_button = Button("Apply model to project")
apply_progress_bar = Progress()
output_project_thmb = ProjectThumbnail()
output_project_thmb.hide()
output_project_done = DoneLabel("done")
output_project_done.hide()
output_project_content = Container(
    [
        select_output_format_f,
        output_project_name_input_f,
        apply_model_to_project_button,
        apply_progress_bar,
        output_project_thmb,
        output_project_done,
    ]
)
card_output_project = Card(
    title="Output Project",
    description="Start labeling by object segmentation model",
    content=output_project_content,
    collapsable=True,
    lock_message="Complete the previous step to unlock",
)
card_output_project.collapse()
card_output_project.lock()


app = sly.Application(
    layout=Container(
        widgets=[
            card_project_settings,
            card_connect_model,
            card_classes,
            settings_preview_content,
            card_output_project,
        ]
    )
)


@dataset_selector.value_changed
def on_dataset_selected(new_dataset_ids):
    if new_dataset_ids == []:
        select_data_button.hide()
    elif new_dataset_ids != [] and select_data_button.is_hidden():
        select_data_button.show()
    update_globals(new_dataset_ids)
    if project_info is not None:
        # set default output project name
        output_project_name_input.set_value(value=project_info.name + " (segmented objects)")


@select_data_button.click
def select_input_data():
    select_data_button.loading = True
    dataset_selector.disable()
    # download input project to ouput project directory
    if os.path.exists(g.output_project_dir):
        sly.fs.clean_dir(g.output_project_dir)
    sly.download_project(
        api=api,
        project_id=project_id,
        dest_dir=g.output_project_dir,
        dataset_ids=dataset_ids,
        log_progress=True,
        save_image_info=True,
        save_images=False,
    )
    select_data_button.loading = False
    select_data_button.hide()
    select_done.show()
    reselect_data_button.show()
    card_connect_model.unlock()
    card_connect_model.uncollapse()


@reselect_data_button.click
def reselect_input_data():
    select_data_button.show()
    reselect_data_button.hide()
    select_done.hide()
    dataset_selector.enable()


@connect_model_button.click
def connect_to_model():
    model_session_id = select_model.get_selected_id()
    if model_session_id is not None:
        connect_model_button.hide()
        connect_model_done.show()
        select_model.disable()
        # show model info
        model_info.set_session_id(session_id=model_session_id)
        model_info.show()
        change_model_button.show()
        # get model meta
        model_meta_json = api.task.send_request(
            model_session_id,
            "get_output_classes_and_tags",
            data={},
        )
        sly.logger.info(f"Detection model meta: {str(model_meta_json)}")
        model_data["model_meta"] = sly.ProjectMeta.from_json(model_meta_json)
        model_data["session_id"] = model_session_id
        # show detection classes table
        classes_table.read_meta(project_meta)
        card_classes.unlock()
        card_classes.uncollapse()


@change_model_button.click
def change_model():
    select_model.enable()
    connect_model_done.hide()
    model_info.hide()
    change_model_button.hide()
    connect_model_button.show()
    card_classes.lock()
    card_classes.collapse()


@classes_table.value_changed
def on_classes_selected(selected_classes):
    n_classes = len(selected_classes)
    if n_classes > 0:
        if n_classes > 1:
            select_classes_button.text = f"Select {n_classes} classes"
        else:
            select_classes_button.text = f"Select {n_classes} class"
        select_classes_button.show()
    else:
        select_classes_button.hide()


# function for getting random image from selected project
def get_random_image(images_info):
    image_idx = random.randint(0, len(images_info) - 1)
    random_image_info = images_info[image_idx]
    return random_image_info


# function for drawing inference previews
def draw_inference_preview(image_info, settings):
    boxes_ann_json = api.annotation.download(image_info.id).annotation
    global preview_project_meta
    image_ann = sly.Annotation.from_json(boxes_ann_json, preview_project_meta)
    boxes_labels = image_ann.labels
    for box in boxes_labels:
        box_name = box.obj_class.name
        # filter bounding boxes in annotation according to selected classes
        if box_name in model_data["selected_classes"]:
            object_roi = box.geometry.to_bbox()
            settings["rectangle"] = object_roi.to_json()
            ann = api.task.send_request(
                model_data["session_id"],
                "inference_image_id",
                data={"image_id": image_info.id, "settings": settings},
                timeout=500,
            )
            target_class_name = box_name + "_mask"
            target_class = preview_project_meta.get_obj_class(target_class_name)
            if target_class is None:  # if obj class is not in preview project meta
                target_class = sly.ObjClass(target_class_name, sly.Bitmap, [255, 0, 0])
                preview_project_meta = preview_project_meta.add_obj_class(target_class)
            ann = sly.Annotation.from_json(ann["annotation"], preview_project_meta)
            label = ann.labels[0]
            final_label = [label.clone(obj_class=target_class)]
            ann = ann.clone(labels=final_label)
            image_ann = image_ann.add_labels(ann.labels)
    # draw predicted bounding boxes on preview image
    labeled_image.set(
        title="Labeled image example",
        image_url=image_info.full_storage_url,
        ann=image_ann,
    )


@select_classes_button.click
def select_classes():
    classes_table.disable()
    # get selected classes
    model_data["selected_classes"] = classes_table.get_selected_classes()
    sly.logger.info(f"Selected classes: {str(model_data['selected_classes'])}")
    n_det_classes = len(model_data["selected_classes"])
    select_classes_button.hide()
    if n_det_classes > 1:
        classes_done.text = f"{n_det_classes} classes were selected successfully"
    else:
        classes_done.text = f"{n_det_classes} class was selected successfully"
    classes_done.show()
    select_other_classes_button.show()
    # get detection custom inference settings
    inference_settings = api.task.send_request(
        model_data["session_id"],
        "get_custom_inference_settings",
        data={},
    )
    model_data["inference_settings"] = inference_settings
    if inference_settings["settings"] is None or len(inference_settings["settings"]) == 0:
        inference_settings["settings"] = ""
    elif isinstance(inference_settings["settings"], dict):
        inference_settings["settings"] = yaml.dump(
            inference_settings["settings"], allow_unicode=True
        )
    model_settings_editor.set_text(inference_settings["settings"])
    card_model_settings.unlock()
    card_model_settings.uncollapse()
    # create preview project meta
    card_preview.loading = True
    global preview_project_meta, images_info
    preview_project_meta = api.project.get_meta(id=project_id)
    preview_project_meta = sly.ProjectMeta.from_json(preview_project_meta)
    # merge preview project meta with det model meta
    preview_project_meta = preview_project_meta.merge(model_data["model_meta"])
    # define images info
    images_info = []
    for dataset_info in api.dataset.get_list(project_id):
        images_info.extend(api.image.get_list(dataset_info.id))
    image_items = [Select.Item(value="Random image")]
    image_items.extend([Select.Item(image_info.id, image_info.name) for image_info in images_info])
    select_preview.set(items=image_items)
    preview_image_info = get_random_image(images_info)
    # draw detection preview
    draw_inference_preview(preview_image_info, inference_settings)
    card_preview.loading = False
    card_preview.uncollapse()
    card_preview.unlock()


@select_other_classes_button.click
def select_other_classes():
    classes_table.enable()
    classes_table.clear_selection()
    select_other_classes_button.hide()
    classes_done.hide()
    card_model_settings.lock()
    card_model_settings.collapse()
    card_preview.lock()
    card_preview.collapse()


@save_model_settings_button.click
def save_model_settings():
    model_settings_editor.readonly = True
    # get inference settings
    inference_settings = model_settings_editor.get_text()
    inference_settings = yaml.safe_load(inference_settings)
    model_data["inference_settings"] = inference_settings
    if inference_settings is None:
        inference_settings = {}
        sly.logger.info("Model doesn't support custom inference settings.")
    else:
        sly.logger.info("Model inference settings:")
        sly.logger.info(str(inference_settings))
    save_model_settings_button.hide()
    model_settings_done.show()
    reselect_model_settings_button.show()
    card_output_project.unlock()
    card_output_project.uncollapse()


@reselect_model_settings_button.click
def reselect_model_settings():
    model_settings_editor.readonly = False
    save_model_settings_button.show()
    model_settings_done.hide()
    reselect_model_settings_button.hide()
    card_output_project.unlock()
    card_output_project.uncollapse()


@redraw_image_button.click
def redraw_preview():
    labeled_image.hide()
    card_preview.loading = True
    if select_preview.get_value() == "Random image":
        preview_image_info = get_random_image(images_info)
    else:
        id = select_preview.get_value()
        preview_image_info = api.image.get_info_by_id(id=id)
    inference_settings = model_settings_editor.get_text()
    inference_settings = yaml.safe_load(inference_settings)
    draw_inference_preview(preview_image_info, inference_settings)
    labeled_image.show()
    card_preview.loading = False


@select_output_format.value_changed
def on_format_selected(format):
    if format == "save labeled images to new project" and output_project_name_input_f.is_hidden():
        output_project_name_input_f.show()
    elif format == "add labeled images to selected project":
        output_project_name_input_f.hide()


@apply_model_to_project_button.click
def apply_models_to_project():
    apply_model_to_project_button.loading = True
    format = select_output_format.get_value()
    if format == "save labeled images to new project":
        output_project_name_input.enable_readonly()
    output_project = sly.Project(g.output_project_dir, mode=sly.OpenMode.READ)
    # merge output project meta with model meta
    merged_meta = output_project.meta.merge(model_data["model_meta"])
    output_project.set_meta(merged_meta)
    output_project_meta = output_project.meta
    if format == "add labeled images to selected project":
        api.project.update_meta(project_id, output_project_meta)
    # define inference settings
    inference_settings = model_data["inference_settings"]
    # get datasets info
    datasets_info = {}
    for dataset_info in api.dataset.get_list(project_id):
        dataset_dir = os.path.join(g.output_project_dir, dataset_info.name)
        datasets_info[dataset_info.id] = sly.Dataset(dataset_dir, mode=sly.OpenMode.READ)
    # apply models to project
    with apply_progress_bar(message="Applying model to project...", total=len(images_info)) as pbar:
        for image_info in images_info:
            boxes_ann_json = api.annotation.download(image_info.id).annotation
            image_ann = sly.Annotation.from_json(boxes_ann_json, output_project_meta)
            boxes_labels = image_ann.labels
            for box in boxes_labels:
                box_name = box.obj_class.name
                # filter bounding boxes in annotation according to selected classes
                if box_name in model_data["selected_classes"]:
                    object_roi = box.geometry.to_bbox()
                    inference_settings["rectangle"] = object_roi.to_json()
                    ann = api.task.send_request(
                        model_data["session_id"],
                        "inference_image_id",
                        data={"image_id": image_info.id, "settings": inference_settings},
                        timeout=500,
                    )
                    target_class_name = box_name + "_mask"
                    target_class = output_project_meta.get_obj_class(target_class_name)
                    if target_class is None:  # if obj class is not in output project meta
                        target_class = sly.ObjClass(box_name + "_mask", sly.Bitmap, [255, 0, 0])
                        output_project_meta = output_project_meta.add_obj_class(target_class)
                    global project_meta
                    if (
                        not project_meta.get_obj_class(target_class_name)
                        and format == "add labeled images to selected project"
                    ):  # if obj class is not in project meta
                        project_meta = project_meta.add_obj_class(target_class)
                    ann = sly.Annotation.from_json(ann["annotation"], output_project_meta)
                    if len(ann.labels) > 0:
                        label = ann.labels[0]
                        final_label = [label.clone(obj_class=target_class)]
                        ann = ann.clone(labels=final_label)
                        image_ann = image_ann.add_labels(ann.labels)
            # annotate image in its dataset
            image_dataset = datasets_info[image_info.dataset_id]
            if format == "save labeled images to new project":
                image_dataset.set_ann(image_info.name, image_ann)
            elif format == "add labeled images to selected project":
                api.project.update_meta(project_id, project_meta.to_json())
                image_path = image_dataset.get_item_path(image_info.name)
                api.image.download_path(image_info.id, image_path)
                new_image_info = api.image.upload_path(
                    image_info.dataset_id,
                    name="gen_" + image_info.name,
                    path=image_dataset.get_item_path(image_info.name),
                )
                api.annotation.upload_ann(new_image_info.id, image_ann)
            pbar.update()
    if format == "save labeled images to new project":
        output_project.set_meta(output_project_meta)
        # upload labeled project to platform
        final_project_id, final_project_name = sly.upload_project(
            dir=g.output_project_dir,
            api=api,
            workspace_id=workspace_id,
            project_name=output_project_name_input.get_value(),
            log_progress=True,
        )
        # prepare project thumbnail
        final_project_info = api.project.get_info_by_id(final_project_id)
        output_project_thmb.set(info=final_project_info)
    elif format == "add labeled images to selected project":
        project_info = api.project.get_info_by_id(project_id)
        output_project_thmb.set(info=project_info)
    output_project_thmb.show()
    apply_model_to_project_button.loading = False
    apply_model_to_project_button.hide()
    output_project_done.show()
    # remove unnecessary files since they are no longer needed
    sly.io.fs.remove_dir(g.app_data_dir)
    sly.logger.info("Project was successfully labeled")
    app.shutdown()
