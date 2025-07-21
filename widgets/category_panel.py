from dataclasses import dataclass
from typing import Sequence, Callable, Optional, Iterable

import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
from matplotlib import pyplot as plt

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from widgets.save_panel import SavePanel
from utils.textutils import strip_path_until, remove_last_n_parts


def _default_on_select(selected: Sequence[str], df: pd.DataFrame) -> None:
    pass


STRIP_PATH_KEYWORDS = ["rinalm9z", "storage", "users", "home", "VASP_test"]


def clean_path(path: str, strip_val: int) -> str:
    return strip_path_until(
        remove_last_n_parts(path, strip_val),
        anchors=STRIP_PATH_KEYWORDS
    )


@dataclass
class TargetFeature:
    name: str
    extractor: Callable[[pd.Series], np.ndarray]
    is_atom_level: bool = False


class BaseCategoryPanel(widgets.VBox):
    def __init__(
        self,
        df: pd.DataFrame,
        categories: Sequence[str],
        on_select: Optional[Callable[[Sequence[str], pd.DataFrame], None]] = _default_on_select,
        show_save: bool = True,
        name_col: str = 'name'
    ):
        # TODO: should it be copied or rather not?
        self.df = df
        self.categories = categories
        self.on_select = on_select
        self.name_col = name_col

        self.select_widget = widgets.SelectMultiple(
            options=categories,
            value=[],
            rows=max(4, len(categories)),
            description='Categories:',
            layout=widgets.Layout(width='250px')
        )
        self.select_widget.observe(self._on_select_change, names="value")

        self.save_panel = SavePanel(lambda path: self.df.to_pickle(path)) if show_save else None

        children = [self.select_widget]
        if self.save_panel:
            children.append(self.save_panel)

        super().__init__(children=children)

    def _on_select_change(self, change):
        self.on_select(self.get_selected(), self.df)

    def get_selected(self) -> Sequence[str]:
        return list(self.select_widget.value)

    def refresh(self):
        self.on_select(self.get_selected(), self.df)


class CategoryPanel(BaseCategoryPanel):
    def __init__(
        self,
        df: pd.DataFrame,
        categories: Sequence[str],
        target_features: Iterable[TargetFeature],
        show_save: bool = True,
        name_col = 'name'
    ):
        #TODO: add check of presence target_labels in df.columns
        self.target_features = tuple(target_features)
        self.target_labels = [t.name for t in self.target_features]

        super().__init__(df, categories, on_select=self._on_select, show_save=show_save, name_col=name_col)

        self.strip_right = widgets.IntText(
            value=3,
            description='Strip right:',
            layout=widgets.Layout(width='150px')
        )
        self.strip_right.observe(lambda change: self.refresh(), names="value")

        self.output_stats = widgets.Output()
        self.output_plot = widgets.Output()

        controls = widgets.VBox([self.select_widget, self.strip_right])
        if self.save_panel:
            controls.children += (self.save_panel,)

        self.children = [
            widgets.HBox([controls, self.output_stats]),
            self.output_plot
        ]

    def _on_select(self, selected: Sequence[str], df: pd.DataFrame):

        mask = df[selected].any(axis=1)
        filtered_df = df[mask]

        with self.output_stats:
            clear_output()

            if not selected:
                print("No categories selected.")
                return


            result = filtered_df[self.name_col].apply(
                lambda name: clean_path(name, self.strip_right.value)
            ).value_counts()
            print()
            # print numbers for each structure
            print(
                format_compound_table(filtered_df, self.categories)
            )
            print()
            # TODO: decide if format_describe_table is needed
            # print some stats for the cols of interest
            # print(
            #     format_describe_table(filtered_df, self.target_labels)
            # )

            display(result)

        with self.output_plot:
            clear_output()

            n_cats = len(selected)
            n_feats = len(self.target_features)
            fig, axes = plt.subplots(n_cats, n_feats, figsize=(3 * n_feats, 2.5 * n_cats), squeeze=False)

            for i, cat in enumerate(selected):
                cat_df = filtered_df[filtered_df[cat]]
                for j, feature in enumerate(self.target_features):
                    ax = axes[i][j]
                    try:
                        values = feature.extractor(cat_df[feature.name])
                        if values is not None and len(values) > 0:
                            ax.hist(values, bins=80)
                        ax.set_title(f"{cat} – {feature.name}", fontsize=9)
                        ax.set_yscale("log")
                    except Exception as e:
                        ax.set_title(f"{cat} – {feature.name}\n⚠️ {e}", fontsize=8)
                        ax.axis("off")

            plt.tight_layout()
            plt.show()


def format_describe_table(df: pd.DataFrame, cols: Sequence[str], width: int = 8) -> str:
    valid_cols = [c for c in cols if c in df.columns and np.issubdtype(df[c].dtype, np.number)]
    if not valid_cols:
        return "No valid scalar columns to describe."

    stats = df[valid_cols].describe().T
    res = "target prop\t" + "\t".join([f"{c:{width}}" for c in valid_cols])
    for stat in stats.columns:
        row = f"\n{stat}:\t\t" + "\t".join([f"{stats.loc[c, stat]:+4.3e}" for c in valid_cols])
        res += row
    return res

def format_compound_table(df, cats, width=5):
    res = "\t".join([f"{c[:width]:<{width}}" for c in cats])
    res += "\n"
    for c in cats:
        n = df[c].sum()
        res += f"{n:<{width}}\t"
    return res
#
# def strip_name_right(s, n_strip_right=2):
#     return "/".join(s.split("/")[:-n_strip_right])
#
# def strip_name_left(s):
#     #ptrn = r".*?(rinalm9z|storage|users|home)/"
#     ptrn = r".*?(rinalm9z|storage|users|home|VASP_test)/"
#     return re.sub(ptrn, "", s)