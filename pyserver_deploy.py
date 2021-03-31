from flask import Flask, render_template
import flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start_date= datetime.datetime(2015, 11, 1)
    end_date= datetime.datetime(2016, 3, 10)
    stock_name= "GOOG"

    df= data.DataReader(name= stock_name, data_source= "stooq", 
                        start= start_date, end= end_date)

    def bull_bear(c, o):
        if c > o:
            value= "Bullish"
        elif c < o:
            value= "Bearish"
        else:
            value= "Equal"
        return value

    df["Status"]= [bull_bear(c, o) for c, o in zip(df.Close, df.Open)]
    df["Median"]= (df.Open + df.Close)/2
    df["Height"]= abs(df.Open - df.Close)

    plot= figure(x_axis_type= "datetime", width= 1000, height= 300, sizing_mode= "scale_width")
    plot.title.text= stock_name + " Daily Chart " + "(" + str(start_date) + "-" + str(end_date) + ")"
    plot.grid.grid_line_alpha = 0

    hours_12= 12*60*60*1000

    plot.segment(df.index, df.High, df.index, df.Low, color= "Black")

    plot.rect(df.index[df.Status == "Bullish"], df.Median[df.Status == "Bullish"], 
            hours_12, df.Height[df.Status == "Bullish"], fill_color= "green", line_color= "black")
    plot.rect(df.index[df.Status == "Bearish"], df.Median[df.Status == "Bearish"], 
            hours_12, df.Height[df.Status == "Bearish"], fill_color= "#FF3333", line_color= "black")

    script1, div1 = components(plot)
    cdn_js= CDN.js_files
    
    return render_template("plot.html", plot_script= script1,
                           plot_div= div1, src_js= cdn_js[0])


if (__name__) == ('__main__'):
    app.run(debug=True)