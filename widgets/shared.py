import ipywidgets as widgets

def make_slider_float(description, min_val, max_val, step=0.01, value=None):
    return widgets.FloatSlider(
        value=value or min_val,
        min=min_val,
        max=max_val,
        step=step,
        description=description,
        continuous_update=False,
        readout_format='.2f',
        layout=widgets.Layout(width='300px')
    )

def make_select_multiple(options, description='Select'):
    return widgets.SelectMultiple(
        options=options,
        value=options,
        description=description,
        layout=widgets.Layout(width='300px', height='120px')
    )

def make_dropdown(options, description='Choose', value=None):
    return widgets.Dropdown(
        options=options,
        value=value or options[0],
        description=description
    )

def make_checkbox(description, value=True):
    return widgets.Checkbox(
        value=value,
        description=description
    )

def make_button(description, on_click_fn=None):
    btn = widgets.Button(description=description)
    if on_click_fn:
        btn.on_click(on_click_fn)
    return btn
