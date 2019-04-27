# Perform necessary imports
from bokeh.io import curdoc
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import Slider, Select, Button
from bokeh.layouts import widgetbox, column, row
import numpy as np
import pandas as pd

housePropertyDataset = pd.read_csv('../house_property_sales.csv')

x = housePropertyDataset['TotalBsmtSF']
y = housePropertyDataset['SalePrice']

def changeArea(attr, old, new):
    scale = slider.value
    new_data = {
        'total_bsmt_SF' : housePropertyDataset.loc[housePropertyDataset['YrSold'] == scale, 'TotalBsmtSF'],
        'sale_price'    : housePropertyDataset.loc[housePropertyDataset['YrSold'] == scale, 'SalePrice']
    }
    source.data = new_data
    plot.title.text = 'Total Basement Area VS Sales Price for the Sales Year %d' % scale

    
def salesCondition(attr, old, new):
    source.data = {
        'total_bsmt_SF' : housePropertyDataset.loc[housePropertyDataset['SaleCondition'] == new, 'TotalBsmtSF'],
        'sale_price' : housePropertyDataset.loc[housePropertyDataset['SaleCondition'] == new, 'SalePrice']
    }

def reset():
    source.data ={'total_bsmt_SF': x, 'sale_price': y}
    
plot = figure(x_axis_label='Total Basement Area (In sqft)', y_axis_label='Sales Price')
source = ColumnDataSource(data={'total_bsmt_SF': x, 'sale_price': y})

# Create a slider: slider
slider = Slider(title='Sales Year', start=2006, end=2010, step=1, value=2006)
slider.on_change('value', changeArea)

select = Select(title="Sales Condition", options=['Normal', 'Abnorml', 'Partial', 'AdjLand', 'Alloca', 'Family'], value='Normal')
select.on_change('value', salesCondition)

button = Button(label='Reset Filters')
button.on_click(reset)

# Add a line to the plot
plot.circle('total_bsmt_SF', 'sale_price', source=source)


# Add slider1 and slider2 to a widgetbox
layout = column(widgetbox(slider, select, button), plot)
# Add the plot to the current document
curdoc().add_root(layout)