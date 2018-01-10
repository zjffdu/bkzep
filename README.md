`bkzep` is Python Package for using Bokeh in Apache Zeppelin Notebook.

[![Build Status](https://travis-ci.org/zjffdu/bkzep.svg?branch=master)](https://travis-ci.org/zjffdu/bkzep)

## Prerequisites
* bokeh >= 0.12.7

## How to use
It is very easy to use bkzep. In order to use bokeh in zeppelin. You just need to
add the following 2 lines

```
from bokeh.io import output_notebook
import bkzep
output_notebook(notebook_type='zeppelin')
```

Here's 2 examples:
1. How to show figure in Apache Zeppelin
2. How to show bokeh app in Apache Zeppelin

```
%python

from bokeh.plotting import figure
from bokeh.io import show,output_notebook
import bkzep
output_notebook(notebook_type='zeppelin')

f = figure()
f.line(x=[1,2],y=[3,4])
show(f)
```


```
%python


import pandas as pd
from bokeh.layouts import row, widgetbox
from bokeh.models import Select, Slider
from bokeh.charts import Histogram
from bokeh.io import show, output_notebook
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.plotting import figure, ColumnDataSource
import pandas as pd
import yaml

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook

import bkzep
output_notebook(notebook_type='zeppelin')


def modify_doc(doc):
    data_url = "/Users/jzhang/Downloads/B01_sbe37_all_e20c_77ac_63de.csv"
    df = pd.read_csv(data_url, parse_dates=True, index_col=0)
    df = df.rename(columns={'temperature (celsius)': 'temperature'})
    df.index.name = 'time'

    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25),
                  y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """))




# Set up the Application
handler = FunctionHandler(modify_doc)
app = Application(handler)

doc = app.create_document()
show(app, notebook_url='localhost:8080')

```

## How to publish

```
python setup.py sdist upload -r pypi
```
