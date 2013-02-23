# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import client
from lettuce import before, after, world, step
from lettuce.django import django_url
import os
import time

try:
    from lxml import html
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
except:
    pass


@before.harvest
def setup_database(variables):
    try:
        os.remove('lettuce.db')
    except:
        pass  # database doesn't exist yet. that's ok.

    os.system("cp lettuce_base.db lettuce.db")


@before.all
def setup_browser():
    browser = getattr(settings, 'BROWSER', None)
    if browser is None:
        raise Exception('Please configure a browser in settings_test.py')
    elif browser == 'Firefox':
        ff_profile = FirefoxProfile()
        ff_profile.set_preference("webdriver_enable_native_events", False)
        world.browser = webdriver.Firefox(ff_profile)
    elif browser == 'Chrome':
        world.browser = webdriver.Chrome()

    world.client = client.Client()
    world.using_selenium = False

    # Make the browser size at least 1024x768
    world.browser.execute_script("window.moveTo(0, 1); "
                                 "window.resizeTo(1024, 768);")

    # Wait implicitly for 2 seconds
    world.browser.implicitly_wait(5)

    # stash
    world.memory = {}


@after.all
def teardown_browser(total):
    world.browser.quit()


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
    os.system("echo 'delete from quizblock_response;' | sqlite3 lettuce.db")
    os.system("echo 'delete from quizblock_submission;' | sqlite3 lettuce.db")
    os.system("echo 'delete from nutrition_counselingsessionstate_answered;'"
              " | sqlite3 lettuce.db")
    os.system("echo 'delete from nutrition_counselingsessionstate;'"
              " | sqlite3 lettuce.db")


@step(r'I access the url "(.*)"')
def access_url(step, url):
    if world.using_selenium:
        world.browser.get(django_url(url))
    else:
        response = world.client.get(django_url(url))
        world.dom = html.fromstring(response.content)


@step(u'I am at the ([^"]*) page')
def i_am_at_the_name_page(step, name):
    if world.using_selenium:
        # Check the page title
        try:
            title = world.browser.title
            assert title.find(name) > -1, \
                "Page title is %s. Expected something like %s" % (title, name)
        except:
            time.sleep(1)
            title = world.browser.title
            assert title.find(name) > -1, \
                "Page title is %s. Expected something like %s" % (title, name)


@step(u'I am logged in as ([^"]*)')
def i_am_logged_in_as_username(step, username):
    if world.using_selenium:
        world.browser.get(django_url("/accounts/logout/"))
        world.browser.get(django_url("accounts/login/?next=/"))
        username_field = world.browser.find_element_by_id("id_username")
        password_field = world.browser.find_element_by_id("id_password")
        form = world.browser.find_element_by_name("login_local")
        username_field.send_keys(username)
        password_field.send_keys("test")
        form.submit()
        assert username in world.browser.page_source, world.browser.page_source
    else:
        world.client.login(username=username, password='test')


@step(u'I log in with a local account')
def i_log_in_with_a_local_account(step):
    form = world.browser.find_element_by_name("login_local")
    form.submit()


@step(u'I am not logged in')
def i_am_not_logged_in(step):
    if world.using_selenium:
        world.browser.get(django_url("/accounts/logout/"))
    else:
        world.client.logout()


@step(u'I log out')
def i_log_out(step):
    if world.using_selenium:
        world.browser.get(django_url("/accounts/logout/"))
    else:
        response = world.client.get(
            django_url("/accounts/logout/"), follow=True)
        world.response = response
        world.dom = html.fromstring(response.content)


@step(u'There is no ([^"]*) navigation')
def there_is_no_direction_navigation(step, direction):
    try:
        world.browser.find_element_by_id(direction)
        assert False, "%s navigation is available" % direction
    except:
        pass  # expected


@step(u'There is ([^"]*) navigation')
def there_is_direction_navigation(step, direction):
    try:
        world.browser.find_element_by_id(direction)
    except:
        assert False, "Could not find %s navigation" % direction


@step(u'I navigate to the ([^"]*) page')
def i_navigate_to_the_direction_page(step, direction):
    try:
        elt = world.browser.find_element_by_id(direction)
        elt.click()
    except:
        assert False, "Could not find %s navigation" % direction


@step(u'I type "([^"]*)" for ([^"]*)')
def i_type_value_for_field(step, value, field):
    if world.using_selenium:
        selector = "input[name=%s]" % field
        input = world.browser.find_element_by_css_selector(selector)
        assert input is not None, "Cannot locate input field named %s" % field
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
            world.browser.find_element_by_partial_link_text(text)
            assert False, "found the '%s' link" % text
        except:
            pass  # expected


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
            link = world.browser.find_element_by_partial_link_text(text)
            assert link.is_displayed()
        except:
            try:
                time.sleep(1)
                link = world.browser.find_element_by_partial_link_text(text)
                assert link.is_displayed()
            except:
                world.browser.get_screenshot_as_file("/tmp/selenium.png")
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
            link = world.browser.find_element_by_partial_link_text(text)
            assert link.is_displayed()
            link.click()
        except:
            try:
                time.sleep(1)
                link = world.browser.find_element_by_partial_link_text(text)
                assert link.is_displayed()
                link.click()
            except:
                world.browser.get_screenshot_as_file("/tmp/selenium.png")
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
    assert elt is None, "Found button named %s" % value

# For debug purposes. Avoid using.


@step(u'I wait (\d+) second')
def then_i_wait_count_second(step, count):
    n = int(count)
    time.sleep(n)


@step(u'I see "([^"]*)"')
def i_see_text(step, text):
    try:
        assert text in world.browser.page_source, world.browser.page_source
    except:
        time.sleep(1)
        assert text in world.browser.page_source, \
            "I did not see %s in this page" % text


@step(u'I do not see "([^"]*)"')
def i_do_not_see_text(step, text):
    assert text not in world.browser.page_source, world.browser.page_source


@step(u'I\'m told ([^"]*)')
def i_m_told_text(step, text):
    alert = world.browser.switch_to_alert()
    assert alert.text.startswith(text), "Alert text invalid: %s" % alert.text
    alert.accept()

# Local utility functions


def find_button_by_value(value, parent=None):

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

    elts = world.browser.find_elements_by_tag_name("button")
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
