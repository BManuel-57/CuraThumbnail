# CuraThumbnail

## Feature
This plugin will embed a thumbnail (using Prusa picture encoding) of the object(s) sliced in GCode, the picture will be present as comments, so there is no impact on the printing.

* This thumbnail could be used in Octoprint to have an overview of the files : [PrusaSlicer Thumbnails](https://plugins.octoprint.org/plugins/prusaslicerthumbnails/)
* It's also possible to see the thumbnail directly in Windows Explorer as an icon of the Gcode file: [GcodeThumbnailExtension](https://github.com/jkavalik/GcodeThumbnailExtension/releases)

## Install
1. Donwload the file **PrusaMods.py** 
2. Place it in the folder **plugins\PostProcessingPlugin\scripts** of your install of **Ultimaker Cura**
3. Start/Restart Cura
4. Open the menu : **Extensions -> Post Processing -> Modify G-Code**
5. On the new Window click on **Add a script**
6. Choose **Embed Prusa Thumbnail**
7. Tick the checkbox **Embed a preview image...***
