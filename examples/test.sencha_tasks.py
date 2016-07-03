import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from Component import Component


class TaskCreationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
        self.driver.set_window_size(1920, 1080)

    def test_task_creation(self):
        self.driver.get("http://examples.sencha.com/extjs/6.0.2/examples/classic/simple-tasks/index.html")
        self.driver.execute_script('localStorage.clear();')
        self.driver.set_page_load_timeout(10)

        # Common asserts for page loaded
        WebDriverWait(self.driver, 5).until(lambda d: d.execute_script('return Ext.isReady && !Ext.env.Ready.firing'))
        self.assertTrue("SimpleTasks" in self.driver.title)
        self.assertTrue(self.driver.execute_script('return window.SimpleTasks != undefined'))

        new_task_name = 'Test task from selenium'
        # Filling up new test task fields
        new_task_form = Component(self.driver, 'taskForm')
        WebDriverWait(self.driver, 5).until(lambda d: new_task_form.rendered)

        task_title = new_task_form.down('textfield[emptyText="Add a new task"]')
        task_title.get_element().find_element_by_xpath('.//input').send_keys(new_task_name)

        task_list = new_task_form.down('treepicker')
        task_list.get_element().find_element_by_xpath('.//input').click()
        lists_tree = Component(self.driver, 'treepanel[floating=true]')
        lists_tree.get_element().find_element_by_xpath('.//span[text()="All Lists"]').click()

        task_date = new_task_form.down('datefield')
        task_date_input_el = task_date.get_element().find_element_by_xpath('.//input')
        task_date_input_el.clear()
        task_date_input_el.send_keys('01/01/2017')
        task_date_input_el.send_keys(Keys.ENTER)

        # Checking for newly created task record
        tasks_grid_view = Component(self.driver, 'taskGrid gridview')
        elements = tasks_grid_view.safe_call('all.elements')
        self.assertEquals(len(elements), 1)
        new_task_el = tasks_grid_view.safe_call('all.elements[0]')
        new_task_el.find_element_by_xpath('.//td/div[text()="{0}"]'.format(new_task_name))
        new_task_el.find_element_by_xpath('.//td/div[text()="All Lists"]')

    def tearDown(self):
        self.driver.save_screenshot('teardown.png')
        self.driver.close()
