import sys
from pathlib import Path
from typing import Callable, Sequence, Mapping, Optional

import pandas as pd
from IPython.core.display_functions import clear_output
from ipywidgets import widgets

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from widgets.category_panel import BaseCategoryPanel

class PlotPanel(BaseCategoryPanel):
    def __init__(
        self,
        df: pd.DataFrame,
        categories: Sequence[str],
        plot_funcs: Mapping[str, Callable[[pd.DataFrame], None]],
        filter_elements: Sequence[widgets.Widget],
        custom_filter_func: Optional[Callable[[pd.DataFrame, Sequence[widgets.Widget]], pd.Series]] = None,
        name_col: str = "name"
    ):
        self.plot_funcs = plot_funcs
        self.active_plot_func = next(iter(self.plot_funcs.values()))
        self.filter_elements = list(filter_elements)
        self.custom_filter_func = custom_filter_func

        self.select_coll = widgets.SelectMultiple(
            options=[("Collinear", True), ("Non-collinear", False)],
            value=[True, False],
            description="Magnetism:",
            layout=widgets.Layout(width='95%')
        )

        self.plot_ddown = widgets.Dropdown(
            description="Plot type:",
            options=list(self.plot_funcs.keys()),
            value=next(iter(self.plot_funcs.keys()))
        )
        self.plot_ddown.observe(self._on_plot_func_change, names="value")

        self.output_plot = widgets.Output()

        super().__init__(df, categories, on_select=self._on_select, show_save=True, name_col=name_col)

        filters_box = widgets.VBox([*self.filter_elements, self.select_coll], layout=widgets.Layout(width='400px'))
        controls = widgets.HBox([self.select_widget, filters_box])
        if self.save_panel:
            controls.children += (self.save_panel,)

        self.children = [
            widgets.HBox([controls]),
            self.plot_ddown,
            self.output_plot
        ]

        self._observe_filters()
        self.refresh()

    def _observe_filters(self):
        for w in [*self.filter_elements, self.select_coll]:
            w.observe(self.refresh, names="value")

    def _on_plot_func_change(self, change):
        self.active_plot_func = self.plot_funcs[change["new"]]
        self.refresh()

    def _on_select(self, selected, df):
        self.refresh()

    def _get_filtered_df(self):
        df = self.df

        if self.custom_filter_func:
            mask = self.custom_filter_func(df, self.filter_elements)
        else:
            # Fallback: assume sliders with 'description' matching df columns
            mask = pd.Series(True, index=df.index)
            for slider in self.filter_elements:
                col = slider.description
                if col in df.columns:
                    mask &= df[col].between(*slider.value)

        if self.select_coll.value:
            mask &= df["if_coll"].isin(self.select_coll.value)

        selected_cats = list(self.select_widget.value)
        if selected_cats:
            mask &= df[selected_cats].any(axis=1)

        return df[mask].drop_duplicates(subset=[self.name_col])

    def refresh(self, *_):
        with self.output_plot:
            clear_output()
            filtered_df = self._get_filtered_df()
            print(f"{len(filtered_df)} rows selected")
            self.active_plot_func(filtered_df)


def make_slider(df, col, label=None, step=0.01):
    return widgets.FloatRangeSlider(
        value=[df[col].min(), df[col].max()],
        min=df[col].min(), max=df[col].max(),
        step=step,
        description=label or col,
        layout=widgets.Layout(width='95%'),
        continuous_update=False
    )