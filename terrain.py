# -*- coding: utf-8 -*-
from lettuce.django import django_url
from lettuce import before, after, world, step
from django.test import client
import sys, os, time
from selenium.webdriver.common.keys import Keys

import time
try:
    from lxml import html
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.keys import Keys
    import selenium
except:
    pass

@before.harvest
def setup_database(variables):
    try:
        os.remove('lettuce.db')
    except:
        pass #database doesn't exist yet. that's ok.

    os.system("cp lettuce_base.db lettuce.db")

@before.all
def setup_browser():
    ff_profile = FirefoxProfile() 
    ff_profile.set_preference("webdriver_enable_native_events", False) 
    world.firefox = webdriver.Firefox(ff_profile)
    world.client = client.Client()
    world.using_selenium = False
    
    # Make the browser size at least 1024x768
    world.firefox.execute_script("window.moveTo(0, 1); window.resizeTo(1024, 768);");
    
@after.all
def teardown_browser(total):
    world.firefox.quit()

@step(u'Using selenium')
def using_selenium(step):
    world.using_selenium = True

@step(u'Finished using selenium')
def finished_selenium(step):
    world.using_selenium = False

@before.each_scenario
def clear_selenium(step):
    world.using_selenium = False
    
    os.system("echo 'delete from main_userprofile;' | sqlite3 lettuce.db")
    os.system("echo 'delete from main_uservisited;' | sqlite3 lettuce.db")
    os.system("echo 'delete from quizblock_response cascade;' | sqlite3 lettuce.db")
    os.system("echo 'delete from quizblock_submission cascade;' | sqlite3 lettuce.db")
    
@step(r'I access the url "(.*)"')
def access_url(step, url):
    if world.using_selenium:
        world.firefox.get(django_url(url))
    else:
        response = world.client.get(django_url(url))
        world.dom = html.fromstring(response.content)
        
@step(u'my browser resolution is ([^"]*) x ([^"]*)')
def my_browser_resolution_is_width_x_height(step, width, height):
    cmd = "window.moveTo(0, 1); window.resizeTo(%s, %s);" % (width, height)
    world.firefox.execute_script(cmd);


@step(u'I am at the ([^"]*) page')
def i_am_at_the_name_page(step, name):
    if world.using_selenium:
        # Check the page title
        try:
            title = world.firefox.title
            assert title.find(name) > -1, "Page title is %s. Expected something like %s" % (title, name)
        except:
            time.sleep(1)
            title = world.firefox.title
            assert title.find(name) > -1, "Page title is %s. Expected something like %s" % (title, name)

@step(u'When I log in with a local account')
def when_i_log_in_with_a_local_account(step):
    form = world.firefox.find_element_by_name("login_local")
    form.submit()


@step(u'I am ([^"]*) in ([^"]*)')
def i_logged_in(step, username):
    if world.using_selenium:
        world.firefox.get(django_url("/accounts/logout/"))
        world.firefox.get(django_url("accounts/login/?next=/"))
        username_field = world.firefox.find_element_by_id("id_username")
        password_field = world.firefox.find_element_by_id("id_password")
        form = world.firefox.find_element_by_name("login_local")
        username_field.send_keys(username)
        password_field.send_keys("test")
        form.submit()
        title = world.firefox.title
        assert username in world.firefox.page_source, world.firefox.page_source

        step.given('I am at the Welcome page')
    else:
        world.client.login(username=username,password='test')

@step(u'I am not logged in')
def i_am_not_logged_in(step):
    if world.using_selenium:
        world.firefox.get(django_url("/accounts/logout/"))
    else:
        world.client.logout()
        
@step(u'I log out')
def i_log_out(step):
    if world.using_selenium:
        world.firefox.get(django_url("/accounts/logout/"))
    else:
        response = world.client.get(django_url("/accounts/logout/"),follow=True)
        world.response = response
        world.dom = html.fromstring(response.content)


@step(u'I type "([^"]*)" for ([^"]*)')
def i_type_value_for_field(step, value, field):
    if world.using_selenium:
        selector = "input[name=%s]" % field
        input = world.firefox.find_element_by_css_selector(selector)
        assert input != None, "Cannot locate input field named %s" % field
        input.send_keys(value)
    
@step(u'I click the ([^"]*) button')
def i_click_the_value_button(step, value):
    if world.using_selenium:
        elt = find_button_by_value(value)
        assert elt, "Cannot locate button named %s" % value
        elt.click()
        
@step(u'there is not an? "([^"]*)" link')
def there_is_not_a_text_link(step, text):
    if not world.using_selenium:
        for a in world.dom.cssselect("a"):
            if a.text:
                if text.strip().lower() in a.text.strip().lower():
                    href = a.attrib['href']
                    response = world.client.get(django_url(href))
                    world.dom = html.fromstring(response.content)
                    assert False, "found the '%s' link" % text
    else:
        try:
            link = world.firefox.find_element_by_partial_link_text(text)
            assert False, "found the '%s' link" % text
        except:
            pass # expected             
        
@step(u'there is an? "([^"]*)" link')
def there_is_a_text_link(step, text):
    if not world.using_selenium:
        for a in world.dom.cssselect("a"):
            if a.text:
                if text.strip().lower() in a.text.strip().lower():
                    href = a.attrib['href']
                    response = world.client.get(django_url(href))
                    world.dom = html.fromstring(response.content)
                    return
        assert False, "could not find the '%s' link" % text
    else:
        try:
            link = world.firefox.find_element_by_partial_link_text(text)
            assert link.is_displayed()
        except:
            try:
                time.sleep(1)
                link = world.firefox.find_element_by_partial_link_text(text)
                assert link.is_displayed()
            except:
                world.firefox.get_screenshot_as_file("/tmp/selenium.png")
                assert False, link.location      
        
        
@step(u'I click the "([^"]*)" link')
def i_click_the_link(step, text):
    if not world.using_selenium:
        for a in world.dom.cssselect("a"):
            if a.text:
                if text.strip().lower() in a.text.strip().lower():
                    href = a.attrib['href']
                    response = world.client.get(django_url(href))
                    world.dom = html.fromstring(response.content)
                    return
        assert False, "could not find the '%s' link" % text
    else:
        try:
            link = world.firefox.find_element_by_partial_link_text(text)
            assert link.is_displayed()
            link.click()
        except:
            try:
                time.sleep(1)
                link = world.firefox.find_element_by_partial_link_text(text)
                assert link.is_displayed()
                link.click()
            except:
                world.firefox.get_screenshot_as_file("/tmp/selenium.png")
                assert False, link.location      

@step(u'there is an? ([^"]*) button')
def there_is_a_value_button(step, value):
    try:
        elt = find_button_by_value(value)
        assert elt, "Cannot locate button named %s" % value
    except:
        time.sleep(1)
        elt = find_button_by_value(value)
        assert elt, "Cannot locate button named %s" % value

@step(u'there is not an? ([^"]*) button')
def there_is_not_a_value_button(step, value):
    elt = find_button_by_value(value)
    assert elt == None, "Found button named %s" % value

# For debug purposes. Avoid using.
@step(u'I wait (\d+) second')
def then_i_wait_count_second(step, count):
    n = int(count)
    time.sleep(n)
    
@step(u'I see "([^"]*)"')
def i_see_text(step, text):
    try:
        assert text in world.firefox.page_source, world.firefox.page_source
    except:
        time.sleep(1)
        assert text in world.firefox.page_source, "I did not see %s in this page" % text
    
@step(u'I do not see "([^"]*)"')
def i_do_not_see_text(step, text):
    assert text not in world.firefox.page_source, world.firefox.page_source

@step(u'I\'m told ([^"]*)')
def i_m_told_text(step, text):
    alert = world.firefox.switch_to_alert()
    assert alert.text.startswith(text), "Alert text invalid: %s" % alert.text
    alert.accept()

# Local utility functions
def find_button_by_value(value, parent = None):
    
    if not parent:
        parent = world.firefox
    
    elts = parent.find_elements_by_css_selector("input[type=submit]")
    for e in elts:
        if e.get_attribute("value") == value:
            return e
    
    elts = parent.find_elements_by_css_selector("input[type=button]")
    for e in elts:
        if e.get_attribute("value") == value:
            return e
        
    elts = world.firefox.find_elements_by_tag_name("button")
    for e in elts:
        if e.get_attribute("type") == "button" and e.text == value:
            return e    
        
    # try the links too
    elts = parent.find_elements_by_tag_name("a")
    for e in elts:
        if e.text and e.text.strip() == value:
            return e
        
    return None

world.find_button_by_value = find_button_by_value