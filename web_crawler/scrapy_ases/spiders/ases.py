# -*- coding: utf-8 -*-
from scrapy import Spider, Selector, FormRequest
from ..django_adapter import (
    active_pages,
    page_has_report_today,
    update_page_url,
    save_report_to_database,

    reports_path,
)
from datetime import datetime
import os

class AsesSpider(Spider):
    name = 'ases'
    start_url = 'http://asesweb.governoeletronico.gov.br/ases/'
    start_urls = [start_url]

    def parse(self, response):
        for page in active_pages():
            if page_has_report_today(page):
                continue
            yield FormRequest(
                url = self.start_url + 'avaliar',
                callback = self.parse_report,
                formdata = {
                    'mark': 'true',
                    'content': 'true',
                    'presentation': 'true',
                    'multimedia': 'true',
                    'form': 'true',
                    'behavior': 'true',
                    'url': page.url.strip(),
                    'executar': 'Executar',
                },
                meta = {
                    'page': page,
                }
            )
    
    def parse_report(self, response):
        body_sel = Selector(response)
        
        url = ''
        date_time = ''
        grade = ''
        
        intro = body_sel.xpath("//div[@class='tile --NOVALUE--']//text()").extract()
        for text in intro:
            if url == '1':
                url = text.strip()
            if date_time == '1':
                date_time = text.strip()
                break
            if text == 'Página:':
                url = '1'
            if text == 'Data/Hora:':
                date_time = '1'
        grade = body_sel.xpath("//div[@id='webaxscore']//span//text()").extract()

        page = response.meta['page']

        if len(grade) == 0:
            diagnosis = body_sel.xpath("//div[@id='errorDesc']//div[@class='alert alert-error']//p//text()").extract()
            if len(diagnosis) == 0:
                self.logger.error("URL inválida: '" + str(response.meta['page'].url) + "'")

            else:
                diagnosis = "\nDiagnóstico do Ases: '" + str(diagnosis[0]) + "'"
                self.logger.error("Falha ao avaliar '" + str(response.meta['page'].url) + "'" + diagnosis)

        else:
            update_page_url(page, url)

            date = date_time.split(' ')[0].split('/')
            time = date_time.split(' ')[1].split(':')
            date_time = datetime(
                int(date[2]),
                int(date[1]),
                int(date[0]), 
                int(time[0]),
                int(time[1]),
                int(time[2]),
            )
            grade = int(grade[0].split('%')[0].split(',')[0])
            
            save_report_to_database(page, grade, date_time)
            
            chave = body_sel.xpath("//form[@action='relatorioavaliacao']//input[@name='chaveAvaliacao']//@value").extract()[0]
            
            yield FormRequest(
                url = self.start_url + 'relatorioavaliacao',
                callback = self.save_report_to_pdf,
                formdata = {
                    'tiporel': '4',
                    'chaveAvaliacao': chave,
                    'executar': 'Executar'
                },
                meta = {
                    'page': page,
                    'date_time': date_time,
                }
            )
    
    def save_report_to_pdf(self, response):
        page = response.meta['page']
        date_time = str(response.meta['date_time']).replace(' ', '_')
        
        applicant_cpf_cnpj = page.certification.applicant.cpf_cnpj
        applicant_path = os.path.join(reports_path, applicant_cpf_cnpj)

        if not applicant_cpf_cnpj in os.listdir(reports_path):
            os.mkdir(applicant_path)

        certification_sei_number = page.certification.sei_number
        certification_path = os.path.join(applicant_path, certification_sei_number)

        if not certification_sei_number in os.listdir(applicant_path):
            os.mkdir(certification_path)

        cleaned_url = page.url.replace('/', ",-'")
        url_path = os.path.join(certification_path, cleaned_url)

        if not cleaned_url in os.listdir(certification_path):
            os.mkdir(url_path)
            
        pdf_path = os.path.join(url_path, date_time + '.pdf')
        with open(pdf_path, 'wb') as pdf:
            pdf.write(response.body)
