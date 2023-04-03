<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/119248312/229189558-1f87902b-95f3-498a-9edb-2093fbf576bf.jpg"/>
  
# Apply Object Segmentor To Images Project
  
<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Related-Apps">Related Apps</a> •
  <a href="#Screenshot">Screenshot</a>
</p>
  
[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/apply-object-segmentor-to-images-project)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/apply-object-segmentor-to-images-project)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/apply-object-segmentor-to-images-project.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/apply-object-segmentor-to-images-project.png)](https://supervise.ly)

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

- To use this application you need to launch the Serve IS-Net app and serve the model on your device. Learn more about this app [HERE](https://dev.supervise.ly/ecosystem/apps/serve-isnet).
- Before running this application, make sure that the objects you need to segment are labeled with `BBoxes`.

## Related apps

You can use this model's serving as a Supervisely Application ⬇️

- [Serve IS-Net](https://ecosystem.supervise.ly/apps/serve-isnet) - app allows to segment images in labeling interface using IS-Net model.  
    
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/serve-isnet" src="https://user-images.githubusercontent.com/115161827/229478001-0be3c5bc-b152-4e07-a937-1d19f1687add.png" height="70px" margin-bottom="20px"/>
    
- [Serve SelfReformer](https://ecosystem.supervise.ly/apps/serve-selfreformer) - this is a serving app that allows you to apply the SelfReformer model to an image for  Salient Instance Segmentation tasks. 
    
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/serve-selfreformer" src="XXX" height="70px" margin-bottom="20px"/>
    
- [Serve InSPyReNet](https://ecosystem.supervise.ly/apps/serve-InSPyReNet) - app allows you to apply the InSPyReNet model to an image for Salient Instance Segmentation tasks.  
    
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/serve-InSPyReNet" src="XXX" height="70px" margin-bottom="20px"/>
   
## Screenshot

<img src="https://user-images.githubusercontent.com/119248312/229124111-3da682a6-728f-4b98-9b9e-0ad2693787ed.jpg"/>

