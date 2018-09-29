import pyxel
from pyxel.ui import RadioButton

BUTTON_SIZE = 7


class EditorRadioButton(RadioButton):
    """
    Events:
        __on_change(value)
    """

    def __init__(
        self, parent, x, y, column, row, margin, is_color_button=False, **kwargs
    ):
        super().__init__(
            parent,
            x,
            y,
            BUTTON_SIZE,
            BUTTON_SIZE,
            margin,
            margin,
            column,
            row,
            **kwargs
        )

        self._is_color_button = is_color_button

        self.add_event_handler("draw", self.__on_draw)

    def __on_draw(self):
        if self._is_color_button:
            x = self.x + (self.value % 8) * 8
            y = self.y + (self.value // 8) * 8
            col = 7 if self.value < 6 else 0
            pyxel.text(x + 2, y + 1, "+", col)
        else:
            x = self.x + (self.button_w + self.margin_x) * (self.value % self.column)
            y = self.y + (self.button_h + self.margin_y) * (self.value // self.column)

            pyxel.pal(13, 7)
            pyxel.blt(x, y, 3, x, y + 12, BUTTON_SIZE, BUTTON_SIZE)
            pyxel.pal()