import os
import platform
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

from eubmstu.exceptions import EmptyListSubDeps, EmptyListDeps, EmptyListGroups, DepsNotFound, SubDepsNotFound
from eubmstu.settings import BASE_DIR


class GetDataEU:

    # Инициализация класса
    # username, password - логин и пароль для входа в ЕУ
    # teacher - является ли пользователь преподавателем
    # vpn - из какой сети происходит вход: из внутренней или внешней
    def __init__(self, username, password, isTeacher, isVPN):
        self.options = webdriver.ChromeOptions()
        if platform.system() == 'Linux':
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument("--window-size=720,480")
            # chrome_options.add_argument('--no-sandbox')
            # driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options,
            #                           service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
            from pyvirtualdisplay import Display
            self.display = Display(visible=0, size=(1920, 1080))
            self.display.start()
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'), 0, self.options)
        elif platform.system() == 'Windows':
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver.exe'), 0, self.options)
        self.username = username
        self.password = password
        self.isTeacher = isTeacher
        self.isVPN = isVPN
        if isVPN:
            self.linkProgress = 'https://webvpn.bmstu.ru/+CSCO+1h75676763663A2F2F72682E6F7A6667682E6568++/modules/progress3/'
            self.linkSession = 'https://webvpn.bmstu.ru/+CSCO+1h75676763663A2F2F72682E6F7A6667682E6568++/modules/session/'
            self.contingent = 'https://webvpn.bmstu.ru/+CSCO+1h75676763663A2F2F72682E6F7A6667682E6568++/modules/contingent3/'
        else:
            self.linkProgress = 'https://eu.bmstu.ru/modules/progress3/'
            self.linkSession = 'https://eu.bmstu.ru/modules/session/'
            self.contingent = 'https://eu.bmstu.ru/modules/contingent3/'
        self.isLogin = False

    # Авторизация на сайте
    def login(self):
        try:
            if self.isVPN:
                self.driver.get("https://webvpn.bmstu.ru/+CSCOE+/logon.html")
                self.driver.find_element(By.NAME, 'username').send_keys(self.username)
                self.driver.find_element(By.NAME, 'password').send_keys(self.password)
                self.driver.find_element(By.NAME, 'Login').click()
                self.driver.execute_script(
                    "parent.doURL('75676763663A2F2F72682E6F7A6667682E6568',[{ 'l' : '4829322D03D1606FB09AE9AF59A271D3', 'n' : 1}],'get',false,'no', false)")
            else:
                self.driver.get("http://eu.bmstu.ru")
            if self.isTeacher:
                self.driver.get(
                    self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/a[2]").get_attribute(
                        'href'))
                self.driver.find_element(By.NAME, 'login').send_keys(self.username)
                self.driver.find_element(By.NAME, 'password').send_keys(self.password)
                self.driver.find_element(By.NAME, 'send').click()
            else:
                self.driver.get(
                    self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/a[1]").get_attribute(
                        'href'))
                self.driver.find_element(By.NAME, 'username').send_keys(self.username)
                self.driver.find_element(By.NAME, 'password').send_keys(self.password)
                self.driver.find_element(By.NAME, 'submit').click()
            self.isLogin = True
            return True
        except Exception as e:
            print(str(e))
            return False

    # Получение списка семестров
    def getSemesters(self):
        try:
            listTerm = []
            if self.driver.current_url != self.linkProgress:
                self.driver.get(self.linkProgress)
            for term in self.driver.find_elements(By.XPATH, "//ul[@display='none']/li/a"):
                listTerm.append({'name': term.get_attribute('text').strip(),
                                 'link': term.get_attribute('href').split('/')[-2].strip()})
            code = listTerm[-1]['link']
            if code[-1] == '1':
                code = code[0:-1] + '2'
            else:
                code = str(int(code[0:4]) + 1) + '-01'
            listTerm.append(
                {'name': self.driver.find_element(By.XPATH, "//span[@class='false-link']").text.strip(), 'link': code})
            return listTerm
        except Exception as e:
            return str(e)

    # Получение списка факультетов
    def getDepartaments(self):
        try:
            listDep = []
            if self.driver.current_url != self.linkProgress:
                self.driver.get(self.linkProgress)
            deps = self.driver.find_elements(By.XPATH, "//ul[@class='eu-tree-root']/li/span")
            if len(deps) == 0:
                raise EmptyListDeps()
            else:
                for dep in deps:
                    if ['ИСОТ', 'ФО', 'ВИ'].count(dep.text.split(' - ')[0]) == 0:
                        listDep.append(
                            {'name': dep.text.split(' - ')[1:].strip(), 'code': dep.text.split(' - ')[0].strip()})
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
                subDeps = self.driver.find_elements(By.XPATH,
                                                    "//ul[@class='eu-tree-root']/li[%s]/ul/li/span" % self.searchDep(
                                                        dep))
                if len(subDeps) == 0:
                    raise EmptyListSubDeps()
                else:
                    for subDep in subDeps:
                        text = subDep.get_attribute("innerHTML").replace('&nbsp;', ' ')
                        listSubDep.append({'name': text.split(' - ')[1].strip(), 'code': text.split(' - ')[0].strip()})
            except DepsNotFound:
                pass
            finally:
                return listSubDep
        except Exception as e:
            print(str(e))
            raise Exception('Ошибка получения списка кафедр факультета %s' % dep)

    # Получение списка групп
    # dep - код факультета
    # subDep - код кафедры
    # semester - код семестра
    def getGroups(self, dep, subDep, semester):
        link = self.linkProgress + semester + '/'
        if self.driver.current_url != link:
            self.driver.get(link)
        listGroup = []
        groups = self.driver.find_elements(By.XPATH,
                                           "//ul[@class='eu-tree-root']/li[%s]/ul/li[%s]/ul/li/a" % (
                                               self.searchDep(dep), self.searchSubDep(dep, subDep)))
        if len(groups) == 0:
            raise EmptyListGroups()
        else:
            for group in groups:
                listGroup.append(
                    {'name': group.get_attribute('text'), 'code': group.get_attribute('href').split('/')[-2],
                     'levelEducation': group.get_attribute('data-stage'), 'isEmpty': group.get_attribute('class')})
            return listGroup

    # Поиск факультета на странице по коду факультета
    def searchDep(self, code):
        deps = self.driver.find_elements(By.XPATH, "//ul[@class='eu-tree-root']/li/span")
        if len(deps) == 0:
            raise EmptyListDeps()
        else:
            for i, dep in enumerate(deps):
                if dep.text.split(' - ')[0] == code:
                    return str(i + 1)
            raise DepsNotFound()

    # Поиск кафедры по на странице по коду факультета и кафедры
    def searchSubDep(self, dep, code):
        subDeps = self.driver.find_elements(By.XPATH,
                                            "//ul[@class='eu-tree-root']/li[%s]/ul/li/span" % str(self.searchDep(dep)))
        if len(subDeps) == 0:
            raise EmptyListSubDeps()
        else:
            for i, subDep in enumerate(subDeps):
                text = subDep.get_attribute("innerHTML").replace('&nbsp;', ' ')
                if text.split(' - ')[0] == code:
                    return str(i + 1)
            raise SubDepsNotFound()

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
            count = len(self.driver.find_elements(By.XPATH, "//table[@class='students-table']//tbody/tr/td[1]"))
            return count
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
                       'gradebook': self.driver.find_element(By.XPATH,
                                                             "//table[@class='students-table']//tbody/tr[%s]/td[3]" % (
                                                                 number)).text
                       }
            return student
        except Exception as e:
            print(str(e))
            return {}

    # Получение списка предметов в группе
    def getSubject(self):
        try:
            subjects = []
            countSubjects = self.getCountSubjectsInGroup()
            for i in range(1, countSubjects + 1):
                subjects.append(
                    {'subDep': self.driver.find_element(By.XPATH,
                                                        "//table[@class='standart_table']//tr[%s]/td[6]" % i).text,
                     'subject': self.driver.find_element(By.XPATH,
                                                         "//table[@class='standart_table']//tr[%s]/td[7]/span" % i).text})
            return subjects
        except Exception as e:
            print(str(e))
            return []

    # Получение списка студентов в группе
    def getStudentsInGroup(self, i):
        try:
            student = self.driver.find_element(By.XPATH,
                                               "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[2]" % i).text.split(
                ' ')[0]
            gradeBook = self.driver.find_element(By.XPATH,
                                                 "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[3]" % i).text
            return {'student': student,
                    'gradeBook': gradeBook}
        except Exception as e:
            print(str(e))
            return []

    def searchStudents(self, i):
        try:
            student = self.driver.find_element(By.XPATH,
                                               "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[2]//nobr/span[@class='fio_3']" % i + 1).text.split(
                ' ')[0]
            gradeBook = self.driver.find_element(By.XPATH,
                                                 "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[3]" % i).text
            return {'name': student,
                    'gradebook': gradeBook}
        except Exception as e:
            print(str(e))
            return []

    # Получение результатов текущей успеваемости группы
    # count - количество предметов у данной группы
    def getProgress(self, i, count):
        try:
            progress = []
            for j in range(4, 4 + count):
                thead = self.driver.find_element(By.XPATH,
                                                 "//table[@class='standart_table progress_students vertical_hover table-group']//thead/tr/th[%s]" % j)
                row = self.formatProgress((thead.text.split('\n')[-1]).strip(),
                                          re.sub(r'\s+', ' ', thead.get_attribute('title').strip()), i, j)
                if row != []:
                    progress.append(row)
            if len(progress) != count:
                lenThead = len(self.driver.find_elements(By.XPATH,
                                                         "//table[@class='standart_table progress_students vertical_hover table-group']//thead/tr/th"))
                j = lenThead - 3
                subject = self.driver.find_element(By.XPATH,
                                                   "//table[@class='standart_table progress_students vertical_hover table-group']//thead/tr/th[%s]" % j)
                row = self.formatProgress((subject.text.split('\n')[-1]).strip(),
                                          re.sub(r'\s+', ' ', subject.get_attribute('title').strip()), i, j)
                if row != []:
                    progress.append(row)
            return progress
        except Exception as e:
            print(str(e))
            return []

    # Формирование строки текущей успеваемости
    # subject - Название предмета
    # i, j - переменные
    def formatProgress(self, cell, subject, i, j):
        try:
            if (cell != 'КМ' and cell != 'СЗ' and cell != 'ЛР'):
                return {'subject': subject,
                        'point': self.driver.find_element(By.XPATH,
                                                          "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[%s]" % (
                                                              i, j)).text}
            else:
                return []
        except Exception as e:
            print(str(e))
            return []

    # Количество предметов у данной группы
    def getCountSubjectsInGroup(self):
        try:
            return len(self.driver.find_elements(By.XPATH,
                                                 "//div[@class='no-print']//table[@class='standart_table']//tr"))
        except Exception as e:
            print(str(e))
            return -1

    # Количество студентов в данной группе
    def getCountStudentsInGroup(self):
        try:
            return len(self.driver.find_elements(By.XPATH,
                                                 "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr/td[1]"))
        except Exception as e:
            print(str(e))
            return -1

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
            if fSubjects:
                subjects = self.getSubject()
            countSubjects = self.getCountSubjectsInGroup()
            countStudents = self.getCountStudentsInGroup()
            for i in range(1, countStudents + 1):
                if fStudents:
                    students.append(self.getStudentsInGroup(i))
                if fProgress:
                    progress.append(self.getProgress(i, countSubjects))
            return {'subjects': subjects, 'students': students, 'progress': progress}
        except Exception as e:
            print(str(e))
            return []

    # Получение результатов сдачи сессии группой по студентам и получение предметов у группы (работа функции по флагам)
    # group - код группы
    # semester - код семестра
    def getSessionInGroup(self, group, semester):
        try:
            link = '%s?session_id=%s' % (self.linkSession, semester)
            self.driver.get(link)
            link = '%s/group/%s/' % (self.linkSession, group)
            self.driver.get(link)
            sessions = []
            subjects = []
            count = len(self.driver.find_elements(By.XPATH, '//thead/tr/th'))
            for j in range(4, count + 1):
                subjects.append(
                    {'subject': self.driver.find_element(By.XPATH, '//thead/tr[1]/th[%s]/div[1]' % j).text.strip(),
                     'subDep': self.driver.find_element(By.XPATH,
                                                        '//thead/tr[1]/th[%s]/div[2]' % j).text.split('\n')[0].strip(),
                     'type_rating': self.driver.find_element(By.XPATH,
                                                             '//thead/tr[1]/th[%s]/div[2]/i' % j).text.strip()}
                )
            for i, student in enumerate(self.driver.find_elements(By.XPATH, '//tbody/tr')):
                listStudent = {
                    'gradeBook': self.driver.find_element(By.XPATH, '//tbody/tr[%s]/td[3]' % (i + 1)).text.strip(),
                    'session': []}
                for j in range(4, count + 1):
                    listStudent['session'].append(
                        {'numSubject': j - 4,
                         'rating': self.driver.find_element(By.XPATH,
                                                            '//tbody/tr[%s]/td[%s]' % (i + 1, j)).text.strip()})
                sessions.append(listStudent)
            return {'subjects': subjects, 'sessions': sessions}
        except Exception as e:
            print(str(e))
            return []

    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, 10)")

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