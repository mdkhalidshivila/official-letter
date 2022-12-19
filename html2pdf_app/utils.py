from cgitb import html
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from .models import Bill
from django.conf import settings
# from templates import bill
# import uuid
class Render:
    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        file_name = 'user'

        try:
            with open(str(settings.BASE_DIR) + f'/static/download/{file_name}.pdf', 'wb') as output:
                pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")) , output)

        except Exception as e:
            print(e)

        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        # elif:
        #     return HttpResponse(response.getvalue(), content_type='application/force-download')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

