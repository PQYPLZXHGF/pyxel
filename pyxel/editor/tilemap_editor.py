import pyxel
from pyxel.constants import RENDERER_IMAGE_COUNT, RENDERER_TILEMAP_COUNT

from .edit_frame import EditFrame
from .editor import Editor
from .editor_number_picker import EditorNumberPicker
from .editor_radio_button import EditorRadioButton
from .image_frame import ImageFrame
from .tilemap_frame import TilemapFrame


class TileMapEditor(Editor):
    def __init__(self, parent):
        super().__init__(parent, "tilemap_editor.png")

        self._edit_frame = EditFrame(self, is_tilemap_mode=True)
        self._tilemap_frame = TilemapFrame(self)
        self._select_frame = ImageFrame(self, is_tilemap_mode=True)
        self._tilemap_number = EditorNumberPicker(
            self, 48, 161, 25, 7, 0, RENDERER_TILEMAP_COUNT - 1
        )
        self._tool_button = EditorRadioButton(self, 81, 161, 7, 1, 2)
        self._image_number = EditorNumberPicker(
            self, 192, 161, 25, 7, 0, RENDERER_IMAGE_COUNT - 2
        )

        self.color = 0
        self.tool = 1

        self.add_event_handler("undo", self.__on_undo)
        self.add_event_handler("redo", self.__on_redo)

    @property
    def tilemap(self):
        return self._tilemap_number.value

    @tilemap.setter
    def tilemap(self, value):
        self._tilemap_button.value = value

    @property
    def color(self):
        return (
            self._select_frame.select_y // 8
        ) * 32 + self._select_frame.select_x // 8

    @color.setter
    def color(self, value):
        self._select_frame.cursor_y = (value // 32) * 8
        self._select_frame.cursor_x = (value % 32) * 8

    @property
    def tool(self):
        return self._tool_button.value

    @tool.setter
    def tool(self, value):
        self._tool_button.value = value

    @property
    def image(self):
        return self._image_number.value

    @image.setter
    def image(self, value):
        self._image_button.value = value

    @property
    def edit_x(self):
        return self._edit_frame.viewport_x

    @edit_x.setter
    def edit_x(self, value):
        self._edit_frame.viewport_x = value

    @property
    def edit_y(self):
        return self._edit_frame.viewport_y

    @edit_y.setter
    def edit_y(self, value):
        self._edit_frame.viewport_y = value

    # @property
    # def select_x(self):
    #    return self._select_frame.select_x

    # @property
    # def select_y(self):
    #    return self._select_frame.select_y

    def __on_undo(self, data):
        tm = data["tilemap"]
        x, y = data["pos"]
        dest = pyxel.tilemap(tm).data[y : y + 16, x : x + 16]
        dest[:, :] = data["before"]

        self._edit_frame.edit_x = x
        self._edit_frame.edit_y = y
        self._tilemap_number.value = tm

    def __on_redo(self, data):
        tm = data["tilemap"]
        x, y = data["pos"]
        dest = pyxel.tilemap(tm).data[y : y + 16, x : x + 16]
        dest[:, :] = data["after"]

        self._edit_frame.edit_x = x
        self._edit_frame.edit_y = y
        self._tilemap_number.value = tm