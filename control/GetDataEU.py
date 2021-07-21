import os
import platform
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from control.models import Semester
from eubmstu.exceptions import EmptyListSubDeps, EmptyListDeps, EmptyListGroups, DepsNotFound, SubDepsNotFound
from eubmstu.settings import BASE_DIR


class GetDataEU:

    # Инициализация класса
    # username, password - логин и пароль для входа в ЕУ
    def __init__(self, username, password):
        self.options = webdriver.ChromeOptions()
        if platform.system() == 'Linux':
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument("--window-size=720,480")
            # chrome_options.add_argument('--no-sandbox')
            # driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options,
            #                           service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'), 0, self.options)
            self.driver.maximize_window()
        elif platform.system() == 'Windows':
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver.exe'), 0, self.options)
        self.username = username
        self.password = password
        self.isLogin = False
        self.linkProgress = 'https://eu.bmstu.ru/modules/progress3/'
        self.linkSession = 'https://eu.bmstu.ru/modules/session/'
        self.contingent = 'https://eu.bmstu.ru/modules/contingent3/'

    # Авторизация на сайте
    def login(self):
        try:
            self.driver.get("https://USERNAME:PASSWORD@proxy.bmstu.ru:8443/cas/login?service=https%3A%2F%2"
                            "Fproxy.bmstu.ru%3A8443%2Fcas%2Foauth2.0%2FcallbackAuthorize%3Fclient_name%3DCasOAuthCli"
                            "ent%26client_id%3DEU")
            self.driver.find_element_by_id("username").clear()
            self.driver.find_element_by_id("username").send_keys(self.username)
            self.driver.find_element_by_id("password").clear()
            self.driver.find_element_by_id("password").send_keys(self.password)
            self.driver.find_element_by_css_selector("div.row").click()
            self.driver.find_element_by_name("submit").click()
            self.driver.get("https://eu.bmstu.ru/")
            self.isLogin = True
            return True
        except Exception as e:
            print(str(e))
            return False

    # Получение списка семестров
    def getSemesters(self):
        try:
            if self.driver.current_url != self.linkProgress:
                self.driver.get(self.linkProgress)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            listTerm = list(map(lambda x: {'link': x['href'].split('/')[-2], 'name': x.text},
                                soup.find('ul', {'id': 'term-select'}).findAll('a')))
            name = soup.find('span', {'class': 'false-link'}).text
            listTerm.append({'link': name.split(' ')[2].split('-')[0] + '-' + name[-3:-1], 'name': name})
            return listTerm
        except Exception as e:
            return str(e)

    # Получение списка факультетов
    def getDepartaments(self):
        try:
            if self.driver.current_url != self.linkProgress:
                self.driver.get(self.linkProgress)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            listDep = list(map(lambda x: {'name': x.find('span').text.split(' - ')[1].replace('\xa0', ' '),
                                          'code': x.find('span').text.split(' - ')[0]},
                               soup.find('ul', {'class': 'eu-tree-root'}).findAll('li', recursive=False)))

            listDep = list(filter(lambda x: x['code'] != 'ИСОТ' and x['code'] != 'ФО' and x['code'] != 'ВИ', listDep))
            return listDep
        except Exception as e:
            return str(e)

    # Получение списка кафедр
    # dep - код факультета
    def getSubDepartaments(self, dep):
        try:
            if self.driver.current_url != self.linkProgress:
                self.driver.get(self.linkProgress)
            listSubDep = []
            try:
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                departaments = enumerate(list(map(lambda x: x.find('span').text.split(' - ')[0],
                                                  soup.find('ul', {'class': 'eu-tree-root'}).findAll('li',
                                                                                                     recursive=False))))
                number = list(filter(lambda x: x[1] == dep, list(departaments)))[0][0]
                listSubDep = list(map(lambda x: {'name': x.find('span').text.split(' - ')[1].replace('\xa0', ' '),
                                                 'code': x.find('span').text.split(' - ')[0]},
                                      soup.find('ul', {'class': 'eu-tree-root'}).findAll('li', recursive=False)[number]
                                      .find('ul').findAll('li', recursive=False)))
            except DepsNotFound:
                pass
            finally:
                return listSubDep
        except Exception as e:
            print(str(e))
            raise Exception('Ошибка получения списка кафедр факультета %s' % dep)

    # Получение списка групп
    # subDep - код кафедры
    # semester - код семестра
    def getGroups(self, subDep, semester):
        link = self.linkProgress + semester + '/'
        if self.driver.current_url != link:
            self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        groups = list(filter(lambda x: x.find('a').text.find(''.join(subDep.split('-')) + '-') == 0, soup.findAll('li',
                                                                                                                  {
                                                                                                                      'class': 'eu-tree-leaf'})))
        listGroups = list(map(lambda x: {'name': x.find('a').text, 'code': x.find('a')['href'].split('/')[-2],
                                         'levelEducation': x.find('a')['data-stage'], 'isEmpty': x.find('a')['class']},
                              groups))
        return listGroups

    # Получение списка факультетов в модуле "Контингент"
    def getLinkDeps(self):
        try:
            if self.driver.current_url != self.contingent:
                self.driver.get(self.contingent)
            deps = self.driver.find_elements(By.XPATH, "//ul[@class='eu-tree-root']/li/"
                                                       "ul[@class='eu-tree-nodeset']/li/"
                                                       "ul/li[@class='eu-tree-active']/a")
            listLinkDeps = list(map(lambda x:
                                    {'link': x.get_attribute('href'),
                                     'dep': x.get_attribute('text').split(' ')[-1]}, deps))
            return listLinkDeps
        except Exception as e:
            print(str(e))
            return []

    # Получение количества студентов на факультете из модуля "Контингент"
    # link - ссылка на факультет
    def getCountStudentsDep(self, link):
        try:
            if self.driver.current_url != link:
                self.driver.get(link)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            return re.search(r'\d+', soup.find('div', {'id': 'short-stat'}).find('p').text)[0]
        except Exception as e:
            print(str(e))
            return -1

    # Получение списка студентов на факультете из модуля "Контингент"
    # link - ссылка на факультет
    # number - порядковый номер студента в таблице
    def getStudentDep(self, link, number):
        try:
            if self.driver.current_url != link:
                self.driver.get(link)
            student = {'name': re.sub(r'\s+', ' ', self.driver.find_element(By.XPATH,
                                                                            "//table[@class='students-table']//tbody/tr[%s]/td[2]" % (
                                                                                number)).text).strip(),
                       'gradeBook': self.driver.find_element(By.XPATH,
                                                             "//table[@class='students-table']//tbody/tr[%s]/td[3]" % (
                                                                 number)).text
                       }
            return student
        except Exception as e:
            print(str(e))
            return {}

    # Получение списка студентов на факультете из модуля "Контингент"
    # link - ссылка на факультет
    def getStudents(self, link):
        try:
            if self.driver.current_url != link:
                self.driver.get(link)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            students = soup.find('table', {'class': 'students-table'}).find('tbody').findAll('tr')
            return list(
                map(lambda x: {'student': x.findAll('td')[1].text, 'gradeBook': x.findAll('td')[2].text, 'uuid': None},
                    students))
        except Exception as e:
            print(str(e))
            return {}

    # Получение списка предметов в группе
    def getSubject(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            subjects = list(map(lambda x: {'subDep': x.findAll('td')[5].text,
                                           'subject': x.findAll('td')[6].find('span').text},
                                soup.find('div', {'id': 'content'}).find('div', {'class': 'no-print'})
                                .find('table', {'class': 'standart_table'}).findAll('tr')))
            return subjects
        except Exception as e:
            print(str(e))
            return []

    # Получение списка студентов в группе
    def getStudentsInGroup(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            students = list(map(lambda x: {
                'student': x.findAll('td')[1].findAll('span')[1].text.replace('\t', '').replace('\n', '').
                                replace('\xa0', ' '), 'gradeBook': x.findAll('td')[2].text,
                'uuid': x.findAll('td')[1].find('a')['href'].split('/')[-1]}, soup.find('table', {
                'class': 'standart_table progress_students vertical_hover table-group'}).find('tbody').findAll('tr')))
            return students
        except Exception as e:
            print(str(e))
            return []

    # Получение результатов текущей успеваемости группы
    def getProgress(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            nameColumns = list(enumerate(soup.find('table', {'class': 'standart_table progress_students vertical_hover '
                                                                      'table-group'}).find('thead').find('tr')
                                         .findAll('th', {'class': 'headcol-discipline'})))
            formatNameColumns = list(map(lambda x: {'i': x[0] + 3, 'subject': x[1]['title'],
                                                    'type': x[1].text.split('\n')[2],
                                                    'subDep': x[1].find('span').text.split('(')[-1].replace(')', '')},
                                         nameColumns))
            columnSubjects = list(filter(lambda x: x['type'] != 'СЗ' and x['type'] != 'ЛР' and x['type'] != 'КМ',
                                         formatNameColumns))
            progress = list(map(lambda x: list(map(lambda y: {'subject': y['subject'],
                                                              'point': 0 if x.findAll('td')[y['i']].find(
                                                                  'span') is None else
                                                              x.findAll('td')[y['i']].find('span').text},
                                                   columnSubjects)), soup.find('table', {
                'class': 'standart_table progress_students vertical_hover table-group'}).find('tbody').findAll('tr')))

            return {'subjects': columnSubjects, 'progress': progress}
        except Exception as e:
            print(str(e))
            return []

    # Получение текущей успеваемости группы по студентам и получение предметов у группы (работа функции по флагам)
    # group - код группы
    # semester - код семестра
    # fSubjects, fStudents, fProgress - флаги, показывающие, какие данные нужны)
    def getProgressInGroup(self, group, semester, fSubjects, fStudents, fProgress):
        try:
            link = self.linkProgress + semester + '/group/' + group + '/'
            if self.driver.current_url != link:
                self.driver.get(link)
            progress = []
            students = []
            subjects = []
            if fProgress:
                progress = self.getProgress()
            if fSubjects:
                subjects = progress['subjects']
            if fStudents:
                students = self.getStudentsInGroup()
            return {'subjects': subjects, 'students': students, 'progress': progress['progress']}
        except Exception as e:
            print(str(e))
            return []

    # Получение результатов сдачи сессии группой по студентам и получение предметов у группы (работа функции по флагам)
    # group - код группы
    # semester - код семестра
    def getSessionInGroup(self, group, code, isMain):
        try:
            semester = Semester.objects.get(code=code)
            if not isMain:
                link = '%s?session_id=%s' % (self.linkSession, semester.session)
                self.driver.get(link)
            link = '%s/group/%s/' % (self.linkSession, group)
            self.driver.get(link)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            try:
                listSubjects = soup.find('thead').findAll('th')[3:]
            except AttributeError:
                print('В группе %s нет студентов' % group)
                return []

            subjects = list(enumerate(
                map(lambda x: {'subject': x.find('div', {'class': 'vertical-text'}).find('span').text,
                               'subDep': str(x.findAll('div')[1].find('i').parent).split('<br/>')[0].replace('<div>',
                                                                                                             ''),
                               'type_rating': x.findAll('div')[1].find('i').text},
                    listSubjects), 3))
            students = list(map(lambda x: {'uuid': x['student-uuid'],
                                           'student': x.findAll('td')[1].find('div', {'class': 'student-fio'})
                                .find('span').text,
                                           'gradeBook': x.findAll('td')[2].find('span').text},
                                soup.find('tbody').findAll('tr')))
            sessions = list(map(lambda x: list(map(lambda y: {'subject': y[1]['subject'],
                                                              'subDep': y[1]['subDep'],
                                                              'type_rating': y[1]['type_rating'],
                                                              'rating': '' if x.findAll('td')[y[0]].find(
                                                                  'span') is None else x.findAll('td')[y[0]].find(
                                                                  'span').get_text(strip=True)},
                                                   subjects)),
                                soup.find('tbody').findAll('tr')))

            return {'subjects': list(map(lambda x: x[1], subjects)), 'students': students, 'sessions': sessions}
        except Exception as e:
            print(str(e))
            return []

    # выход из системы
    def exit(self):
        try:
            self.driver.quit()
            self.driver = None
            self.display.sendstop()
        except:
            self.driver.quit()
            self.driver = None
            self.display.sendstop()
        return True
