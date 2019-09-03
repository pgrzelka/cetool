from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.units import cm

centered = PS(name='centered',
              fontName='Verdana',
              fontSize=16,
              leading=16,
              alignment=1,
              spaceAfter=20)

p = PS(name='p',
       fontName='Verdana',
       fontSize=12,
       leading=10,
       spaceAfter=10)

months = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik",
          "Listopad", "Grudzień"]
days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def build_pdf(form, response):
    pdfmetrics.registerFont(TTFont('Verdana', 'assets/Verdana.ttf'))

    month = form.cleaned_data['month'] - 1
    doc = SimpleDocTemplate(response, rightMargin=1 * cm, leftMargin=1 * cm, topMargin=1 * cm, bottomMargin=0)

    data = [(u"Dzień\nmiesiąca", "Liczba\ngodzin", "Opis")]

    for d in range(1, days_in_month[month] + 1):
        v = form.cleaned_data['day-{}'.format(d)]
        desc = form.cleaned_data['desc-{}'.format(d)]
        data.append(("{}".format(d), v if v and int(v) > 0 else "-", desc))

    data.append(("", 'Suma: {}'.format(form.cleaned_data['hours_sum']), ""))

    table = Table(data=data, colWidths=(70, 70, '*'), spaceBefore=20)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Verdana'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('ALIGN', (0, 1), (1, -1), 'RIGHT'),
        ('BOX', (0, 0), (-1, -2), 0.25, colors.black),
        # ('SPAN', (3, 1), (-1, -2)),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        # ('FONTSIZE', (0, 1), (-1, -2), 12),
        # ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTSIZE', (2, 1), (-1, -1), 8),
        ('INNERGRID', (0, 0), (-1, -2), 0.25, colors.black),
    ]))

    footer = Table(data=[
        ("........................................................",
         "........................................................"),
        ("Podpis wykonawcy", "Podpis zleceniodawcy"),
    ], colWidths='*', spaceBefore=20)

    footer.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Verdana'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    doc.build([
        Paragraph('Ewidencja czasu pracy', centered),
        Paragraph(u"Miesiąc i rok: {} {}".format(months[month], form.cleaned_data['year']), p),
        Paragraph(u"Wykonawca: {}".format(form.cleaned_data['performer']), p),
        table,
        footer
    ])
