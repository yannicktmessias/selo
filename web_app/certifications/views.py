from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    cert_1 = {
        'id': 1,
        'domain': 'prefeitura.sp.gov.br/',
        'applicant': 'Prefeitura do Cidade de São Paulo',
        'grant_date': '12/02/2019',
        'below_links_count': 0,
        'above_links_count': 13,
        'last_evaluation': '19:42 21/04/2019',
        'link': '',
    }
    cert_2 = {
        'id': 2,
        'domain': 'camarasuzano.sp.gov.br/',
        'applicant': 'Câmara Municipal de Suzano',
        'grant_date': '12/02/2019',
        'below_links_count': 1,
        'above_links_count': 19,
        'last_evaluation': '19:42 21/04/2019',
        'link': '',
    }
    cert_3 = {
        'id': 3,
        'domain': 'samsung.com.br/',
        'applicant': 'Samsung',
        'grant_date': '12/02/2019',
        'below_links_count': 0,
        'above_links_count': 2,
        'last_evaluation': '19:42 21/04/2019',
        'link': '',
    }

    args = {
        'certifications': [cert_1, cert_2, cert_3]
    }

    return render(request, 'home.html', args)
