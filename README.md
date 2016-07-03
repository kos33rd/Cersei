# Cersei - Python Selenium add-on to work with Ext JS components
---
### A lightweight helper class to aid testing and working with Ext JS components in more natural way. Represents part of Queryable mixin methods from Ext JS framework
* Selenium: http://selenium-python.readthedocs.io/
* Ext JS: https://www.sencha.com/products/extjs/
* Component Query: http://docs.sencha.com/extjs/5.1.3/Ext.ComponentQuery.html
* Queryable mixin: http://docs.sencha.com/extjs/5.1.3/Ext.mixin.Queryable.html


## Usage
To start with, you have to initialize a Component with webdriver and component query (CQ):
```python
	from cersei.Component import Component
    form = Component(self.driver, 'loginForm')
```
Note: CQ have to uniquely determine your component. Otherwise first of all fitting components will be used.

You can use various methods like `up` and `child` to traverse through components:
```python
    email_field = form.down('textfield[emptyText="Enter your email"]')
    form_panel = form.up('panel')
    submit_button = form.child('button[text="Submit"]')
```

You could also use eval-like syntax with `call` and `safe_call` to execute arbitrary method or retrieve component's property:
```python
    form_body_el = form.call('body')
    form_visibility = form.call('isVisible()')
    
    # safe_call with fallback to None in case of JS runtime error
    submit_btn_el = form.safe_call('buttons[0].getEl()')
```

You could switch from component to it's WebElement representation with `get_element` at any time:
```python
    email_field = form.down('textfield[emptyText="Enter your email"]')
    input = email_field.get_element().find_element_by_xpath('.//input')
    input.click()
    input.send_keys('lobovke@gmail.com')
```

Handy `get_id` method:
```python
    # Waiting for component to be created
    WebDriverWait(self.driver, 5).until(lambda d: email_field.get_id() is not None)
    
    # Waiting for component to become visible
    WebDriverWait(self.driver, 5).until(
        expected_conditions.visibility_of_element_located((By.ID, email_field.get_id()))
    )
```

Also you could get access to any of JS Component's properties right from Python:
```python
    # Read 'rendered' property right from javascript object properties
    WebDriverWait(self.driver, 5).until(lambda d: form.rendered)
```
NB: Method calls is not supported. Also possible browser-side call stack error on heavy or deep-linked objects. Be careful and use `safe_call` in case of troubles.

## Compatibility
* Library tested with `Python 3.4` and `Ext JS 5.*` and `6.*`. There is no python-3-specific code so feel free to make an experiments.
