from fpdf import FPDF
from PIL import Image

def gen_pdf(av_str, data_start, data_end,data_level):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Automated Report", ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "Data sources: investing.com, finviz.com", ln = 1, align = 'C')
    pdf.cell(200, 10, txt = '', ln = 1)
    pdf.cell(200, 10, txt = '', ln = 1)
    data_stroke = 'Timeframe: '+str(data_start)+' - '+str(data_end)
    pdf.cell(200, 10, txt = data_stroke, ln = 1)
    text_stroke = 'Average price: '+str(av_str)
    pdf.cell(200, 10, txt = text_stroke, ln = 1)
    high_stroke = 'Main changes in price were: '+str(data_level)
    pdf.cell(200, 10, txt = high_stroke, ln = 1)
    pdf.cell(200, 10, txt = "Generated graph:", ln = 1, align = 'C')
    pdf.image('fig/fig.png', x=50, y=90, w=120,h=80)

    im = Image.open('fig/fig_finviz.jpg')
    im_rotate = im.rotate(90, expand=True)
    im_rotate = im.rotate(90, expand=True)
    im_rotate = im.rotate(90, expand=True)
    im_rotate.save('fig/fig_finviz2.png', quality=95)
    im.close()
    pdf.add_page()
    pdf.image('fig/fig_finviz2.png', x=30, y=10, w=120,h=200)

    pdf.output("GFG.pdf") 
