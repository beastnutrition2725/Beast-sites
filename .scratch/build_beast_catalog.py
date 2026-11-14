from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from PIL import Image as PILImage
from pathlib import Path
import csv, zipfile, shutil

root=Path('/work')
out=root/'beast-nutrition-catalog-2026-10-24.pdf'
imgdir=root/'beast-product-images-2026-10-24'
productdir=root/'beast-nutrition-product-assets-2026-10-24'
productdir.mkdir(exist_ok=True)
products=[
 ('01','MuscleTech','Platinum Multivitamin','60 tablets','Tablets','MUSCLETECH'),
 ('02','GAT Sport','Mens Multi+Test','60 tablets','Tablets','GAT-SPORT'),
 ('03','GAT Sport','Testrol Gold ES','60 tablets','Tablets','GAT-SPORT'),
 ('04','GAT Sport','L-Arginine','180 tablets','Tablets','GAT-SPORT'),
 ('05','Vedistry','Shilajit Gold','60 capsules','Capsules','VEDISTRY'),
 ('06','Tatanka Nutrition','Melatonin 3mg','120 capsules','Capsules · 3 mg','TATANKA-NUTRITION'),
 ('07','Tatanka Nutrition','Magnesium Glycinate 600mg','120 capsules','Capsules · 600 mg','TATANKA-NUTRITION'),
 ('08','Tatanka Nutrition','Biotin 10000mcg','60 capsules','Capsules · 10000 mcg','TATANKA-NUTRITION'),
]
# Copy product images with stable ecommerce filenames
for n,brand,name,size,form,slug in products:
 src=imgdir/f'page-{int(n)+2:02d}-image-02.jpg'
 # page 3 corresponds product 01
 dst=productdir/f'{n}-{slug}-{name.lower().replace(" ","-").replace("+","plus")}.jpg'
 shutil.copy2(src,dst)

styles=getSampleStyleSheet()
ink=colors.HexColor('#18212B'); accent=colors.HexColor('#C47B52'); warm=colors.HexColor('#F7F5F0'); sage=colors.HexColor('#87968A'); light=colors.HexColor('#EEF0EC')
styles.add(ParagraphStyle(name='CoverTitle',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=31,leading=36,textColor=ink,alignment=TA_CENTER,spaceAfter=12))
styles.add(ParagraphStyle(name='Sub',parent=styles['Normal'],fontName='Helvetica',fontSize=12,leading=18,textColor=colors.HexColor('#4E5963'),alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Section',parent=styles['Heading1'],fontName='Helvetica-Bold',fontSize=21,leading=26,textColor=ink,spaceAfter=10))
styles.add(ParagraphStyle(name='Brand',parent=styles['Normal'],fontName='Helvetica-Bold',fontSize=9,leading=11,textColor=accent,spaceAfter=4))
styles.add(ParagraphStyle(name='Product',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=18,leading=22,textColor=ink,spaceAfter=4))
styles.add(ParagraphStyle(name='Body2',parent=styles['Normal'],fontName='Helvetica',fontSize=9.5,leading=14,textColor=colors.HexColor('#34404A')))
styles.add(ParagraphStyle(name='Small',parent=styles['Normal'],fontName='Helvetica',fontSize=8,leading=11,textColor=colors.HexColor('#53606A')))
styles.add(ParagraphStyle(name='CenterSmall',parent=styles['Small'],alignment=TA_CENTER))

def footer(canvas,doc):
 canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#D9DDD7')); canvas.line(18*mm,13*mm,192*mm,13*mm)
 canvas.setFont('Helvetica',7.5); canvas.setFillColor(colors.HexColor('#66727B')); canvas.drawString(18*mm,8*mm,'BEAST NUTRITION  |  Fuel Your Beast Mode')
 canvas.drawRightString(192*mm,8*mm,f'{doc.page}')
 canvas.restoreState()

def p(txt,style='Body2'): return Paragraph(txt,styles[style])
def product_card(prod):
 n,brand,name,size,form,slug=prod
 imgpath=productdir/f'{n}-{slug}-{name.lower().replace(" ","-").replace("+","plus")}.jpg'
 im=Image(str(imgpath),width=74*mm,height=68*mm); im.hAlign='CENTER'
 data=[[im],[p(brand.upper(),'Brand')],[p(name,'Product')],[p('Daily health and wellness support supplements.','Body2')], [p(f'<b>Format:</b> {form}<br/><b>Available size:</b> {size}<br/><b>Category:</b> Tablets &amp; Capsules','Small')]]
 t=Table(data,colWidths=[82*mm],rowHeights=[72*mm,None,None,16*mm,22*mm])
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('BOX',(0,0),(-1,-1),0.6,colors.HexColor('#D9DDD7')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'TOP')]))
 return t

story=[]
story += [Spacer(1,28*mm),p('BEAST NUTRITION','Brand'),p('TABLETS & CAPSULES','CoverTitle'),p('Fuel Your Beast Mode','Sub'),Spacer(1,12*mm),p('Multivitamins  ·  Test Support  ·  Daily Wellness  ·  Amino Tablets','Sub'),Spacer(1,24*mm)]
cover=Table([[p('<b>100% Genuine</b>  ·  Authentic  ·  Lab-Tested Sports Nutrition','Sub')]],colWidths=[160*mm]); cover.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),light),('BOX',(0,0),(-1,-1),0.5,sage),('TOPPADDING',(0,0),(-1,-1),13),('BOTTOMPADDING',(0,0),(-1,-1),13)])); story += [cover,Spacer(1,22*mm),p('Catalog 2026  ·  Thane, Maharashtra','CenterSmall'),PageBreak()]
story += [p('The collection','Section'),p('A focused selection of tablets and capsules from MuscleTech, GAT Sport, Vedistry, and Tatanka Nutrition. Product availability and prices may change; message Beast Nutrition for the current price list and stock confirmation.','Body2'),Spacer(1,10*mm)]
for i in range(0,8,2):
 story += [Table([[product_card(products[i]),product_card(products[i+1])]],colWidths=[88*mm,88*mm],style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4)])),Spacer(1,7*mm)]
story += [PageBreak(),p('Order & enquiry','Section'),p('Get current pricing, availability, bulk rates, and delivery options directly from Beast Nutrition. Special rates are available for gyms, trainers, and bulk orders.','Body2'),Spacer(1,10*mm)]
contact=[['WHATSAPP / CALL','EMAIL','INSTAGRAM'],['+91 84518 35085\n+91 70218 02796','beastnutrition2725@gmail.com','@BEAST_NUTRITION_HUB']]
t=Table(contact,colWidths=[58*mm]*3,rowHeights=[10*mm,23*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ink),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),8),('BACKGROUND',(0,1),(-1,1),light),('TEXTCOLOR',(0,1),(-1,1),ink),('FONTNAME',(0,1),(-1,1),'Helvetica'),('FONTSIZE',(0,1),(-1,1),9),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),0.5,colors.white),('LEFTPADDING',(0,0),(-1,-1),8)])); story += [t,Spacer(1,12*mm),p('<b>Store address</b><br/>Keshri Niwas, Ground Floor No. 2, Phull Gali,<br/>Kisan Nagar No. 2, Shiv Sena Office Back Side,<br/>Thane (West), Maharashtra - 400604','Body2'),Spacer(1,8*mm),p('<b>Delivery:</b> Home delivery across Thane, Mumbai &amp; Navi Mumbai<br/><b>Payments:</b> UPI (GPay / PhonePe / Paytm)  ·  Cash on Delivery  ·  Bank Transfer','Body2'),Spacer(1,15*mm),p('Important: Images are for representation. Product availability and prices may change. Confirm product details, stock, price, and suitability with Beast Nutrition before purchase. Supplements should be used according to the product label and professional guidance where appropriate.','Small')]

doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=19*mm,title='Beast Nutrition Tablets & Capsules Catalog 2026',author='Beast Nutrition')
doc.build(story,onFirstPage=footer,onLaterPages=footer)

csvpath=root/'beast-nutrition-product-upload-2026-10-24.csv'
with csvpath.open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['sku','brand','product_name','category','description','format','available_size','image_filename','price','stock_status','website_url','whatsapp_order','notes'])
 for n,brand,name,size,form,slug in products:
  fn=f'{n}-{slug}-{name.lower().replace(" ","-").replace("+","plus")}.jpg'
  w.writerow([f'BN-TC-{n}',brand,name,'Tablets & Capsules','Daily health and wellness support supplements.',form,size,fn,'','Confirm stock','[WEBSITE PRODUCT URL]','+91 84518 35085','Price and availability change; confirm before publishing.'])
zip_path=root/'beast-nutrition-product-assets-2026-10-24.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(productdir.glob('*.jpg')): z.write(f,f.name)
print('CREATED',out, out.stat().st_size)
print('CREATED',csvpath, csvpath.stat().st_size)
print('CREATED',zip_path, zip_path.stat().st_size)
