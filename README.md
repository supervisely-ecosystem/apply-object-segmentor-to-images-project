<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/119248312/229512592-aa88dd5e-6653-4994-bd21-77ae4cfb0664.jpg"/>
  
# Apply Object Segmentor To Images Project
  
<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Related-Apps">Related Apps</a> •
  <a href="#Screenshot">Screenshot</a>
</p>
  
[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/apply-object-segmentor-to-images-project)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/apply-object-segmentor-to-images-project)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/apply-object-segmentor-to-images-project.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/apply-object-segmentor-to-images-project.png)](https://supervisely.com)

</div>

## Overview

This app allows to label images project using salient object segmentation model.

Application key points:

- Select datasets to label
- Connect to salient object segmentation model
- Choose project classes that will be used for prediction
- Select model settings and preview inference result
- Select output format

## Preparation

- To use this application you need to launch the Serve IS-Net, Serve SelfReformer, Serve InSPyRenet or Serve Segment Anything app and serve the model on your device. Learn more about these apps here: [Serve IS-Net](https://ecosystem.supervisely.com/apps/serve-isnet), [Serve SelfReformer](https://ecosystem.supervisely.com/apps/serve-selfreformer), [Serve InSPyReNet](https://ecosystem.supervisely.com/apps/serve-inspyrenet), [Serve Segment Anything Model](https://ecosystem.supervisely.com/apps/serve-segment-anything-model).
- Before running the application, make sure that the objects you need to segment are labeled with Bounding Boxes.

## Related apps

You can use this model's serving as a Supervisely Application ⬇️

- [Serve IS-Net](https://ecosystem.supervisely.com/apps/serve-isnet) - app allows to segment images in labeling interface using IS-Net model.  
    
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/serve-isnet" src="https://user-images.githubusercontent.com/115161827/229478001-0be3c5bc-b152-4e07-a937-1d19f1687add.png" height="70px" margin-bottom="20px"/>
    
- [Serve SelfReformer](https://ecosystem.supervisely.com/apps/serve-selfreformer) - this is a serving app that allows you to apply the SelfReformer model to an image for  Salient Instance Segmentation tasks. 
    
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/serve-selfreformer" src="https://user-images.githubusercontent.com/115161827/229481263-09f0605c-40b1-4193-ba7f-8f3b06a53578.png" height="70px" margin-bottom="20px"/>
    
- [Serve InSPyReNet](https://ecosystem.supervisely.com/apps/serve-inspyrenet) - app allows you to apply the InSPyReNet model to an image for Salient Instance Segmentation tasks.  
    
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/serve-inspyrenet" src="https://user-images.githubusercontent.com/115161827/229483668-dc48e163-5b11-4c0e-b323-e6e0d7c5df43.png" height="70px" margin-bottom="20px"/>

- [Serve Segment Anything Model](https://ecosystem.supervisely.com/apps/serve-segment-anything-model) - app allows you to apply the Segment Anything model to an image for Interactive Instance Segmentation tasks.  
    
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/serve-segment-anything-model" src="https://user-images.githubusercontent.com/115161827/233978846-c6d7415e-aaeb-4db9-b981-9b26737cc054.png" height="70px" margin-bottom="20px"/>
   
## Screenshot

<img src="https://user-images.githubusercontent.com/119248312/229124111-3da682a6-728f-4b98-9b9e-0ad2693787ed.jpg"/>

