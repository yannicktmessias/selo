from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.template.loader import render_to_string

from applicants.models import Applicant, LegalRepresentative
from certifications.models import Certification, Page, EvaluationReport
from certifications.views import get_past_days, get_past_reports

def send_bad_evaluation_alerts():
    today = datetime.now().date()
    for certification in Certification.objects.all():
        bad_evaluations = {}
        for page in Page.objects.filter(certification=certification):
            page_reports = EvaluationReport.objects.filter(page=page)
            today_page_report = page_reports.filter(
                creation_date_time__year=today.year,
                creation_date_time__month=today.month,
                creation_date_time__day=today.day,
            )
            if today_page_report:
                today_page_report = today_page_report[0]
                if not today_page_report.succeed():
                    bad_evaluations[page.url] = today_page_report.grade
            else:
                bad_evaluations[page.url] = '-1'
        
        if len(bad_evaluations) > 0:
            subject='O nível de Acessibilidade do seu site caiu!'

            message = ''
            message += 'Prezado(a),\n\n'
            message += 'Enviamos esta notificação referente ao Selo de Acessibilidade Digital concedido ao requerente {{ applicant.name }} pela Secretaria Municipal da Pessoa com Deficiência.\n\n'
            message += 'Identificamos que a(s) URL(s) abaixo está(ão) com nota abaixo de 95% no avaliador automático:\n\n'
            for i, url in enumerate(bad_evaluations.keys()):
                if bad_evaluations[url] != '-1':
                    message += str(i+1)+'. '+url+' - '+str(bad_evaluations[url])+'%\n\n'
                else:
                    message += str(i+1)+'. '+url+' - Página inacessível\n\n'
            message += 'Solicitamos as providências para a manutenção da acessibilidade digital da(s) página(s) acima citada(s).\n\n'
            message += 'Contamos com seu compromisso de manter uma web mais acessível.\n\n'
            message += 'Não responda este email, caso tenha dúvidas envie para acessibilidadedigital@prefeitura.sp.gov.br.\n\n'
            message += 'Atenciosamente,\n\n'
            message += 'Departamento de Acessibilidade Digital e Comunicação Inclusiva - DADCI\n'
            message += 'Secretaria Municipal da Pessoas com Deficiencia - SMPED\n'
            message += 'Comissão Permanente de Acessibilidade - CPA Digital\n'
            message += 'Robô de Avaliação Automática de Sites\n'

            args = {
                'applicant': certification.applicant,
                'urls': bad_evaluations.keys(), 
                'grade': bad_evaluations
            }
            html_message = render_to_string('mail/bad_evaluations_alert_inlined.html', args)

            receivers = [certification.applicant.email]
            legal_representative = LegalRepresentative.objects.filter(applicant_represented=certification.applicant)
            if legal_representative:
                legal_representative = legal_representative[0]
                receivers.append(legal_representative.email)
            receivers.append('acessibilidadedigital@prefeitura.sp.gov.br')

            send_mail(
                subject, 
                message, 
                'selo.smped@prefeitura.sp.gov.br', 
                receivers, 
                html_message=html_message, 
                fail_silently=False, 
            )

def send_weekly_evaluation_reports():
    for certification in Certification.objects.all():
        pages = Page.objects.filter(certification=certification)
        if not pages:
            continue
        dates = get_past_days(7)
        reports = get_past_reports(pages, dates)
        
        subject='Relatório semanal do robô'
        
        message = ''

        args = {
            'applicant': certification.applicant,
            'pages': pages,
            'dates': dates,
            'reports': reports,
        }
        html_message = render_to_string('mail/weekly_evaluation_report_inlined.html', args)

        receivers = [certification.applicant.email]
        legal_representative = LegalRepresentative.objects.filter(applicant_represented=certification.applicant)
        if legal_representative:
            legal_representative = legal_representative[0]
            receivers.append(legal_representative.email)

        send_mail(
            subject, 
            message, 
            'selo.smped@prefeitura.sp.gov.br', 
            receivers, 
            html_message=html_message, 
            fail_silently=False, 
        )

def start():
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(send_bad_evaluation_alerts, 'cron', hour=10, max_instances=1)
    scheduler1.start()

    scheduler2 = BackgroundScheduler()
    scheduler2.add_job(send_weekly_evaluation_reports, 'cron', day_of_week='sun', hour=12, max_instances=1)
    scheduler2.start()

if __name__ == '__main__' :
    send_bad_evaluation_alerts()
    send_weekly_evaluation_reports()