"""
    Python Selenium add-on to work with Ext JS framework components.
    Ext JS: https://www.sencha.com/products/extjs/
    Component Query: http://docs.sencha.com/extjs/5.1.3/Ext.ComponentQuery.html
    Queryable mixin: http://docs.sencha.com/extjs/5.1.3/Ext.mixin.Queryable.html

    Component object represents in Python part of Queryable mixin methods from Ext JS framework.
    Usage:
        To start with, you have to initialize a Component with webdriver and component query (CQ).
        CQ have to uniquely determine your component. Otherwise first of all fitting components will be used.


    Tested on Python 3.4 and ExtJS 5 and 6.
    Copyright (c) 2016 by Lobov Konstantin (lobovke@gmail.com).
    License: MIT
"""

from selenium.webdriver.remote.webelement import WebElement


class Component:
    _driver = None
    _cq = None
    _return_element_template = "return Ext.ComponentQuery.query('{cq}')[0].el.dom"
    _component_template = "Ext.ComponentQuery.query('{cq}')[0]"
    _children_ids_template = """
        var self = {self_cq_template};
        var children_cmp = self.query('{children_cq}');
        var children_ids = [];
        Ext.Array.each(children_cmp, function(child_cmp){{
            children_ids.push(child_cmp.getId());
        }});
        return children_ids
        """

    def __init__(self, driver, component_query):
        """
        :param driver: Selenium webdriver to work with
        :param component_query: str ExtJS component query
        """
        self._driver = driver
        self._cq = component_query

    def get_element(self):
        """
        WebElement representation of component's dom
        :rtype: WebElement
        """
        return self._driver.execute_script(self._return_element_template.format(cq=self._cq))

    def get_cmp(self):
        """
        String representing JS code to return component itself
        :rtype: str
        """
        return self._component_template.format(cq=self._cq)

    def get_id(self):
        """
        Returns id of dom element (same as id of ExtJS component).
        If component is not defined or unavailable, returns None.
        :rtype: str
        """
        return self.safe_call('getId()')

    def down(self, component_query):
        """
        Get component, representing descendant of current Component by relative query.
        :param component_query: str component query for Component, descendant to current
        :return: Component
        """
        return Component(self._driver, '{0} {1}'.format(self._cq, component_query))

    def child(self, component_query):
        """
        Get component, representing direct child of current Component by relative query.
        :param component_query: str component query for direct child of current Component
        :return: Component
        """
        return Component(self._driver, '{0} > {1}'.format(self._cq, component_query))

    def parent(self, component_query):
        """
        Get any level parent of current component by query
        :param component_query: str component query for parent relative to current Component
        :return: Component
        """
        return Component(self._driver, '{0} ^ {1}'.format(self._cq, component_query))

    def children(self, children_cq='*'):
        """
        :param children_cq: str children filtering component query
        :rtype: list[Component]
        """
        cq = self._children_ids_template.format(self_cq_template=self.get_cmp(), children_cq=children_cq)
        children_ids = self._driver.execute_script(cq)
        child_components = []
        for child_id in children_ids:
            child_components.append(Component(self._driver, '[id={id}]'.format(id=child_id)))
        return child_components

    def call(self, callee):
        """
        Execute arbitrary method or retrieve component's property
        NB: Be careful, do not retrieve complex JS objects like components - possible recursive stack overflow
        :param callee: str string representation of method(with brackets) or property of a component
        :rtype:
        """
        code = 'return {cmp}.{callee};'.format(cmp=self.get_cmp(), callee=callee)
        return self._driver.execute_script(code)

    def safe_call(self, callee):
        """
        Execute arbitrary method or retrieve component's property with fallback to None in case of JS runtime error.
        NB: Be careful, do not retrieve complex JS objects like components - possible maximum call stack size exceed
        :param callee: str string representation of method(with brackets) or property of a component
        :rtype:
        """
        code = """
        try {{
            return {cmp}.{callee};
        }} catch(e) {{
            return null;
        }}
        """.format(cmp=self.get_cmp(), callee=callee)
        return self._driver.execute_script(code)

    def __getattr__(self, item):
        """
        Hook any non-class property access and transit it to JS
        """
        return self.safe_call(item)
