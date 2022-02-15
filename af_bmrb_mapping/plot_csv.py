import csv
import plotly.express as px
import sys



def plot_csv(csv_file,atm,outpath):
    res=[]
    atom=[]
    exp=[]
    pred=[]
    method=[]
    info=[]
    out_file = '{}/{}'.format(outpath,atm)
    with open(csv_file) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row[2] in [atm]:
                res.append(row[1])
                atom.append(row[2])
                pred.append(float(row[3]))
                exp.append(float(row[4]))
                method.append(row[5])
                info.append('{}-{}'.format(row[6],row[7]))

    fig = px.scatter(x=pred,y=exp,color=method,labels={'x':'Predicted','y':'Observed'})
    min_x=min([min(pred),min(exp)])
    max_x= max([max(pred),max(exp)])

    fig.add_shape(type="line",
                  x0=min_x, y0=min_x, x1=max_x, y1=max_x,
                  line=dict(
                      color="LightSeaGreen",
                      width=4,
                      dash="dashdot",
                  )
                  )
    # fig.update_layout({"xaxis" + str(i + 1): dict(matches=None) for i in range(6)})
    # fig.update_layout({"yaxis" + str(i + 1): dict(matches=None, scaleanchor="x", scaleratio=1) for i in range(4)})
    #
    # fig.show()
    fig.update_xaxes(range=[min_x-1,max_x+1])
    fig.update_yaxes(range=[min_x-1, max_x+1])
    #fig.update_xaxes(fixedrange=True)
    fig.write_html('{}.html'.format(out_file))
    fig.write_image('{}.jpg'.format(out_file),width = 800,height=800)
    fig.write_image('{}.pdf'.format(out_file),width = 800,height=800)


if __name__ == "__main__":
    fname = sys.argv[1]
    out_dir = sys.argv[2]
    atm = sys.argv[3]
    plot_csv(fname,atm,out_dir)