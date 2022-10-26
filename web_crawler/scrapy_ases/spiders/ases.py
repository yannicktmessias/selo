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
from urllib import request
from urllib.error import HTTPError, URLError
from urllib import parse
import chardet
import os
import time

class AsesSpider(Spider):
    name = 'ases'
    start_url = 'http://localhost:8080/ases/'
    start_urls = [start_url]

    def parse(self, response):
        for page in active_pages():
            if page_has_report_today(page):
                continue

            total_memory, used_memory = map(int, os.popen('free -t -m').readlines()[-1].split()[1:3])
            if used_memory/total_memory > 0.8:
                self.logger.error("System out of memory ("+str(used_memory)+" / "+str(total_memory)+").\nRestarting Tomcat7... ")
                os.system('sudo systemctl restart tomcat7')
                time.sleep(60)
                last_tomcat_log = os.popen('journalctl -u tomcat7 | tail -1').readlines()[0]
                if 'Started' not in last_tomcat_log:
                    self.logger.error("Tomcat failed to restart.")

            last_tomcat_log = os.popen('journalctl -u tomcat7 | tail -1').readlines()[0]
            if 'Invalid' in last_tomcat_log:
                self.logger.error("Tomcat found a problem.\nRestarting Tomcat7... ")
                os.system('sudo systemctl restart tomcat7')
                time.sleep(60)
                last_tomcat_log = os.popen('journalctl -u tomcat7 | tail -1').readlines()[0]
                if 'Started' not in last_tomcat_log:
                    self.logger.error("Tomcat failed to restart.")

            url = page.url.replace(' ', '')

            # in case url is not ascii
            scheme, netloc, path, query, fragment = parse.urlsplit(url)
            path = parse.quote(path)
            url = parse.urlunsplit((scheme, netloc, path, query, fragment))

            try:
                url_request = request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'})
                with request.urlopen(url_request, timeout=30) as url_response:
                    raw_source_code = url_response.read()
            except HTTPError as error:
                self.logger.error("HTTP Status " + str(error.status) + ": '" + str(url) + "' " + str(error.reason))
                continue
            except URLError as error:
                self.logger.error("URL inválida: '" + str(url) + "', " + str(error.reason))
                continue
            except TimeoutError:
                self.logger.error("Request timed out")
                continue
            encoding = chardet.detect(raw_source_code)['encoding']
            try:
                source_code = raw_source_code.decode(encoding)
            except:
                source_code = raw_source_code.decode('utf-8')

            yield FormRequest(
                url = self.start_url + 'avaliar-codigo',
                callback = self.parse_report,
                formdata = {
                    'mark': 'true',
                    'content': 'true',
                    'presentation': 'true',
                    'multimedia': 'true',
                    'form': 'true',
                    'behavior': 'true',
                    'html': source_code,
                    'executar': 'Executar',
                },
                meta = {
                    'page': page,
                    'source_code': True,
                }
            )
            '''
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
                    'url': page.url.replace(' ', ''),
                    'executar': 'Executar',
                },
                meta = {
                    'page': page,
                    'source_code': False,
                }
            )
            '''

    def parse_report(self, response):
        body_sel = Selector(response)
        
        url = ''
        date_time = ''
        grade = ''
        
        intro = body_sel.xpath("//div[@class='tile --NOVALUE--']//text()").extract()
        for text in intro:
            if url == '1':
                url = text.replace(' ', '')
            if date_time == '1':
                date_time = text.strip()
                break
            if text == 'Página:':
                url = '1'
            if text == 'Data/Hora:':
                date_time = '1'
        grade = body_sel.xpath("//div[@id='webaxscore']//span//text()").extract()

        page = response.meta['page']

        if url == '':
            url = page.url.replace(' ', '')

        if len(grade) == 0 or grade[0] == '%':
            diagnosis = body_sel.xpath("//div[@id='errorDesc']//div[@class='alert alert-error']//p//text()").extract()
            if len(diagnosis) == 0:
                if response.meta['source_code']:
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
                            'url': url,
                            'executar': 'Executar',
                        },
                        meta = {
                            'page': page,
                            'source_code': False,
                        }
                    )
                else:
                    diagnosis = "\nURL inválida"
                    self.logger.error("Falha ao avaliar '" + str(url) + "'" + diagnosis)

            else:
                diagnosis = "\nDiagnóstico do Ases: '" + str(diagnosis[0]) + "'"
                self.logger.error("Falha ao avaliar '" + str(url) + "'" + diagnosis)

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
            grade = grade[0].split('%')[0].replace(',', '.')
            if grade != '':
                grade = int(float(grade))
            else:
                grade = 0
            
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
