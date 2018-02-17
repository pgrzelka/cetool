from django.http import HttpResponse
from django.views.generic.edit import FormView

from ecp.forms import EcpForm
from ecp.pdf import build_pdf


class EcpView(FormView):
    template_name = 'ecp.html'
    form_class = EcpForm
    success_url = '/ecp/'

    def form_invalid(self, form):
        print("invalid")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ecp-{}-{}.pdf"'.format(form.cleaned_data['month'],
                                                                                        form.cleaned_data['year'])
        build_pdf(form, response)
        return response

        # return super().form_valid(form)
