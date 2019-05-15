import os
import platform
from telnetlib import EC

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from eubmstu.exceptions import EmptyListSubDeps, EmptyListDeps, EmptyListGroups, DepsNotFound, SubDepsNotFound
from eubmstu.settings import BASE_DIR


class getDataEU:
    # Инициализация класса
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
        if self.vpn:
            self.driver.get("https://webvpn.bmstu.ru/+CSCOE+/logon.html")
            self.driver.find_element(By.NAME, 'username').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password)
            self.driver.find_element(By.NAME, 'Login').click()
            # element = WebDriverWait(self.driver, 30).until(
            #     EC.title_is("BMSTU Remote Access"))
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
            # element = WebDriverWait(self.driver, 30).until(
            #     EC.title_is('НОЦ "ЭУ" Авторизация'))
            self.driver.get(
                self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/a[1]").get_attribute(
                    'href'))
            self.driver.find_element(By.NAME, 'username').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password)
            self.driver.find_element(By.NAME, 'submit').click()
        # WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, 'workarea')))
        self.isLogin = True
        # except Exception as e:
        #     print(str(e))
        # self.driver.quit()

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

    def getGroups(self, dep, subDep, semester):
        link = self.linkProgress + semester + '/'
        if self.driver.current_url != link:
            self.driver.get(link)
        listGroup = []
        # try:
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
        # except DepsNotFound:
        #     print('Не найден факультет')
        # except SubDepsNotFound:
        #     print('Не найдена кафедра')

    def searchDep(self, code):
        deps = self.driver.find_elements(By.XPATH, "//ul[@class='eu-tree-root']/li/span")
        if len(deps) == 0:
            raise EmptyListDeps()
        else:
            for i, dep in enumerate(deps):
                if dep.text.split(' - ')[0] == code:
                    return str(i + 1)
            raise DepsNotFound()

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

    def getCountStudentsDep(self, link):
        if self.driver.current_url != link:
            self.driver.get(link)
        count = len(self.driver.find_elements(By.XPATH, "//table[@class='students-table']//tbody/tr/td[1]"))
        return count

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

    def getSubject(self, group, session):
        link = self.linkProgress + session + '/group/' + group
        if self.driver.current_url != link:
            self.driver.get(link)



    def exit(self):
        try:
            self.driver.quit()
            self.driver = None
        except:
            self.driver.quit()
            self.driver = None
        return True
