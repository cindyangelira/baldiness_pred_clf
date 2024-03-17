import pandas as pd
import os
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

class MissingDataViewer():
    def __init__(self, df:pd.DataFrame):
        self.df = df
        self.dropdown = widgets.Dropdown(
            options = df.columns,
            value = df.columns[0],
            description = 'Column:'
        )
        self.output = widgets.Output(layout={"overflow": "scroll", "height": "200px", "width": "100%"})
        self.button = widgets.Button(description = 'Download')
        self.dropdown.observe(self.on_change)
        self.button.on_click(self.click)

    def on_change(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            column = change['new']
            with self.output:
                clear_output(wait = True)
                df_nan = self.df[self.df[column].isna()]
                html = (
                    df_nan.style.set_table_attributes('style="overflow:auto; height:200px; width:100%"').to_html()
                )
                display(HTML(html))

    def click(self, button):
        path = 'data/output'
        if not os.path.exists(path):
            os.makedirs(path)
        column = self.dropdown.value
        self.df[self.df[column].isna()].to_csv(os.path.join(path, f'missing_{column}.csv'), index = False)

    def show(self):
        display(self.dropdown, self.output, self.button)