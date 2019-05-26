import os
import platform

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from eubmstu.exceptions import EmptyListSubDeps, EmptyListDeps, EmptyListGroups, DepsNotFound, SubDepsNotFound
from eubmstu.settings import BASE_DIR


class getDataEU:

    # Инициализация класса
    # username, password - логин и пароль для входа в ЕУ
    # teacher - является ли пльзователь преподавателем
    # vpn - из како сети происходит вход: из внутренней или внешней
    def __init__(self, username, password, teacher, vpn):
        self.options = webdriver.ChromeOptions()
        if platform.system() == 'Linux':
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'), 0, self.options)
        elif platform.system() == 'Windows':
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver.exe'), 0, self.options)
        self.username = username
        self.password = password
        self.teacher = teacher
        self.vpn = vpn
        if vpn:
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
            if self.vpn:
                self.driver.get("https://webvpn.bmstu.ru/+CSCOE+/logon.html")
                self.driver.find_element(By.NAME, 'username').send_keys(self.username)
                self.driver.find_element(By.NAME, 'password').send_keys(self.password)
                self.driver.find_element(By.NAME, 'Login').click()
                self.driver.execute_script(
                    "parent.doURL('75676763663A2F2F72682E6F7A6667682E6568',[{ 'l' : '4829322D03D1606FB09AE9AF59A271D3', 'n' : 1}],'get',false,'no', false)")
            else:
                self.driver.get("http://eu.bmstu.ru")
            if self.teacher:
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
        except Exception as e:
            print(str(e))
        self.driver.quit()

    # Получение списка семестров
    def getSemesters(self):
        listTerm = []
        self.driver.get(self.linkProgress)
        for term in self.driver.find_elements(By.XPATH, "//ul[@display='none']/li/a"):
            listTerm.append({'name': term.get_attribute('text'), 'link': term.get_attribute('href').split('/')[-2],
                             'session': False})
        code = listTerm[-1]['link']
        if code[-1] == '1':
            code = code[0:-1] + '2'
        else:
            code = str(int(code[0:4]) + 1) + '-01'
        listTerm.append(
            {'name': self.driver.find_element(By.XPATH, "//span[@class='false-link']").text, 'link': code,
             'session': False})
        self.driver.get(self.linkSession)
        self.linkSession = self.driver.current_url
        for term in self.driver.find_elements(By.XPATH, "//ul[@id='term-select']/li/a"):
            link = term.get_attribute('href').split('/')[-1]
            listTerm.append(
                {'name': term.get_attribute('text'), 'link': link, 'session': True})
        code = listTerm[-1]['link']
        code = code[0:12] + str(int(code[12:]) + 1)
        listTerm.append(
            {'name': self.driver.find_element(By.XPATH, "//span[@class='false-link']").text, 'link': code,
             'session': True})
        return listTerm

    # Получение списка факультетов
    def getDepartaments(self):
        listDep = []
        self.driver.get(self.linkProgress)
        deps = self.driver.find_elements(By.XPATH, "//ul[@class='eu-tree-root']/li/span")
        if len(deps) == 0:
            raise EmptyListDeps()
        else:
            for dep in deps:
                if ['ИСОТ', 'ФО', 'ВИ'].count(dep.text.split(' - ')[0]) == 0:
                    listDep.append(
                        {'name': dep.text.split(' - ')[1:], 'code': dep.text.split(' - ')[0]})
            return listDep

    # Получение списка кафедр
    # dep - код факультета
    def getSubDepartaments(self, dep):
        if self.driver.current_url != self.linkProgress:
            self.driver.get(self.linkProgress)
        listSubDep = []
        try:
            subDeps = self.driver.find_elements(By.XPATH,
                                                "//ul[@class='eu-tree-root']/li[%s]/ul/li/span" % self.searchDep(dep))
            if len(subDeps) == 0:
                raise EmptyListSubDeps()
            else:
                for subDep in subDeps:
                    text = subDep.get_attribute("innerHTML").replace('&nbsp;', ' ')
                    listSubDep.append({'name': text.split(' - ')[1], 'code': text.split(' - ')[0]})
        except DepsNotFound:
            pass
        finally:
            return listSubDep

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
        if self.driver.current_url != self.contingent:
            self.driver.get(self.contingent)
        deps = self.driver.find_elements(By.XPATH, "//ul[@class='eu-tree-root']/li/"
                                                   "ul[@class='eu-tree-nodeset']/li/"
                                                   "ul/li[@class='eu-tree-active']/a")
        listLinkDeps = list(map(lambda x:
                                {'link': x.get_attribute('href'),
                                 'dep': x.get_attribute('text').split(' ')[-1]}, deps))
        return listLinkDeps

    # Получение количества студентов на факультете из модуля "Контингент"
    # link - ссылка на факультет
    def getCountStudentsDep(self, link):
        if self.driver.current_url != link:
            self.driver.get(link)
        count = len(self.driver.find_elements(By.XPATH, "//table[@class='students-table']//tbody/tr/td[1]"))
        return count

    # Получение списка студентов на факультете из модуля "Контингент"
    # link - ссылка на факультет
    # number - порядковый номер студента в таблице
    def getStudentDep(self, link, number):
        if self.driver.current_url != link:
            self.driver.get(link)
        student = {'name': self.driver.find_element(By.XPATH,
                                                    "//table[@class='students-table']//tbody/tr[%s]/td[2]" % (
                                                        number)).text,
                   'gradebook': self.driver.find_element(By.XPATH,
                                                         "//table[@class='students-table']//tbody/tr[%s]/td[3]" % (
                                                             number)).text,
                   'group': self.driver.find_element(By.XPATH,
                                                     "//table[@class='students-table']//tbody/tr[%s]/td[4]" % (
                                                         number)).text}
        return student

    # Получение списка предметов в группе
    def getSubject(self):
        subjects = []
        countSubjects = self.getCountSubjectsInGroup()
        for i in range(1, countSubjects + 1):
            subjects.append(
                {'subDep': self.driver.find_element(By.XPATH,
                                                    "//table[@class='standart_table']//tr[%s]/td[6]" % i).text,
                 'subject': self.driver.find_element(By.XPATH,
                                                     "//table[@class='standart_table']//tr[%s]/td[7]/span" % i).text})
        return subjects

    # Получение списка студентов в группе
    def getStudentsInGroup(self, i):
        return {'student': self.driver.find_element(By.XPATH,
                                                    "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[2]" % i).text.split(
            ' ')[0],
                'gradeBook': self.driver.find_element(By.XPATH,
                                                      "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[3]" % i).text}

    # Получение результатов текущей успеваемости группы
    # count - количество предметов у данной группы
    def getProgress(self, i, count):
        progress = []
        for j in range(4, 4 + count):
            progress.append(
                {'subject': self.driver.find_element(By.XPATH,
                                                     "//table[@class='standart_table progress_students vertical_hover table-group']//thead/tr/th[%s]" % j).get_attribute(
                    'title'),
                    'point': self.driver.find_element(By.XPATH,
                                                      "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr[%s]/td[%s]" % (
                                                          i, j)).text})
        return progress

    # Количество предметов у данной группы
    def getCountSubjectsInGroup(self):
        return len(self.driver.find_elements(By.XPATH,
                                             "//div[@class='no-print']//table[@class='standart_table']//tr"))

    # Количество студентов в данной группе
    def getCountStudentsInGroup(self):
        return len(self.driver.find_elements(By.XPATH,
                                             "//table[@class='standart_table progress_students vertical_hover table-group']//tbody/tr/td[1]"))

    # Получение текущей успеваемости группы по студентам и получение предметов у группы (работа функции по флагам)
    # group - код группы
    # semester - код семестра
    # fSubjects, fStudents, fProgress - флаги, показывающие, какие данные нужны)
    def getProgressInGroup(self, group, semester, fSubjects, fStudents, fProgress):
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

    # СЕССИЯ
    # for i, line in enumerate(self.driver.find_elements(By.XPATH,
    #                                                                "//table[@class='eu-table sortable-table']//thead/tr/th")):
    #                 listLine.append(line.text)
    #             listData.append(listLine)
    #
    #             for i, line in enumerate(self.driver.find_elements(By.XPATH,
    #                                                                "//table[@class='eu-table sortable-table']//tbody/tr")):
    #                 listLine = []
    #                 for line in self.driver.find_elements(By.XPATH,
    #                                                       "//table[@class='eu-table sortable-table']//tbody/tr[%d]/td" % (
    #                                                               i + 1)):
    #                     listLine.append(line.text)
    #                 listLine[1] = self.driver.find_element(By.XPATH,
    #                                                        "//table[@class='eu-table sortable-table']//tbody/tr[%d]/td[2]/div/span" % (
    #                                                                i + 1)).text
    #                 listData.append(listLine)

    # выход из системы
    def exit(self):
        try:
            self.driver.quit()
            self.driver = None
        except:
            self.driver.quit()
            self.driver = None
        return True
