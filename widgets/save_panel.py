from typing import Callable, Optional
import ipywidgets as widgets
from IPython.display import display

class SavePanel(widgets.VBox):
    def __init__(
        self,
        on_save: Callable[[str], None],
    ):
        self.text = widgets.Text(
            description="file path:",
            placeholder="...new_dataframe.pckl",
            layout=widgets.Layout(width="70%")
        )
        self.button = widgets.Button(description="Save")
        self.output = widgets.Label()
        self.widget = widgets.VBox([widgets.HBox([self.text, self.button]), self.output])

        self._on_save = on_save

        super().__init__([widgets.HBox([self.text, self.button]), self.output])

        self.button.on_click(self._handle_click)

    def _handle_click(self, b: Optional[widgets.Button]) -> None:
        try:
            self._on_save(self.text.value)
            self.output.value = '✅ Saved successfully.'
        except Exception as e:
            self.output.value = f'❌ Save Error: {e}'

    def display(self) -> widgets.Widget:
        return self.widget

    def set_path(self, path: str) -> None:
        self.text.value = path

    def get_path(self) -> str:
        return self.text.value

    def trigger_save(self) -> None:
        self._handle_click(None)

    # magic method for rendering
    def _ipython_display_(self):
        display(self.widget)


