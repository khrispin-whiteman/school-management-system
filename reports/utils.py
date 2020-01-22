from django.template.loader import get_template
from io import BytesIO
import xhtml2pdf.pisa as pisa

def render_to_pdf(template_src, content_dict={}):
    template = get_template(template_src)
    html = template.render(content_dict)
    results = BytesIO()
    pdf = pisa.pisaDocument()
