# Cura PostProcessingPlugin
# Author:   Borr Manuel
# Date:     May 2, 2020

# Description:  This plugin embed a thumbnail of the object(s)

from ..Script import Script
from cura.Snapshot import Snapshot
from UM.Logger import Logger
import re
from PyQt5.QtCore import QByteArray, QBuffer, Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor


class PrusaMods(Script):
    def __init__(self):
        super().__init__()
        self._thumbnail = None

    def getSettingDataString(self):
        return """{
            "name": "Embed Prusa Thumbnail",
            "key": "PrusaMods",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "insert_thumbnail_image":
                {
                    "label": "Embed a preview image in the Prusa's format",
                    "description": "Enabling this, a thumbnail will be generated and included into the gcode",
                    "type": "bool",
                    "default_value": false
                },
                "white_background":
                {
                    "label": "Replace black background with white",
                    "description": "Enabling this settings all backround will be rendered in white",
                    "type": "bool",
                    "default_value": false
                }
            }
        }"""

    def execute(self, in_data):
        self.out_data = in_data
        if self.getSettingValueByKey("insert_thumbnail_image"):
            self.thmb_data = []
            # Create picture
            self._create_thumbnail()
            # Resize
            Logger.log("d", "Creating Prusa thumbnail ...")
            # self._scale_thumbnail_comments()
            # Handle White BG
            Logger.log("d", "Patch white %s ..." % self.getSettingValueByKey("white_background"))
            if self.getSettingValueByKey("white_background"):
                self._patch_alpha_background()
            # Add Base64 encoded thumbnail
            self.thmb_data.append('\n'.join(self._generate_thumbnail_comments()))
            # Separate comments from GCode
            self.thmb_data[0] += ('\n')
            self.thmb_data.extend(in_data)
            self.out_data = self.thmb_data
        else:
            self.out_data=in_data

        return self.out_data

    def _create_thumbnail(self, *args):
        Logger.log("d", "Creating Prusa thumbnail ...")
        try:
            self._thumbnail = Snapshot.snapshot(width=300, height=300)
        except Exception:
            Logger.logException("w", "Failed to create thumbnail")
            self._thumbnail = None

    def _patch_alpha_background(self):
        # QtGui.QPixmap(image)
        # pixmap = QPixmap(self._thumbnail)
        imageNoAlpha = QPixmap(self._thumbnail.width(), self._thumbnail.height()).toImage();
        imageNoAlpha.fill(Qt.white)
        painter = QPainter()
        painter.begin(imageNoAlpha)
        painter.drawImage(0, 0, self._thumbnail)
        painter.end()
        self._thumbnail = imageNoAlpha

    def _generate_thumbnail_comments(self):
        width = self._thumbnail.width()
        height = self._thumbnail.height()
        data = QByteArray()
        buf = QBuffer(data)
        # Encode picture in Jpg format
        self._thumbnail.save(buf, 'JPG', 80)
        # Encode data in Base64
        base_64_thumbnail = str(data.toBase64(), "utf-8")
        # Split lines by blocks of 78 chars
        base_64_lines = re.findall('.{1,78}', base_64_thumbnail)
        thumbnail_comments = ['; thumbnail begin %dx%d %d' % (width, height, len(base_64_thumbnail))]
        for line in base_64_lines:
            thumbnail_comments.append("; %s" % line)

        thumbnail_comments.append("; thumbnail end")
        return thumbnail_comments
