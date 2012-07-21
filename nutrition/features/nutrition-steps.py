from lettuce.django import django_url
from lettuce import before, after, world, step
import sys, time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

@step(u'there are ([0-9][0-9]?) topics')
def there_are_count_topics(step, count):
    try:
        elts = world.firefox.find_elements_by_css_selector("div.accordion-group")
        assert len(elts) == int(count), "There %s topics. Expected %s"  % (len(elts), count)
    except:
        time.sleep(1)
        elts = world.firefox.find_elements_by_css_selector("div.accordion-group")
        assert len(elts) == int(count), "There %s topics. Expected %s"  % (len(elts), count)


@step(u'the clock reads ([0-9][0-9]?) seconds')
def the_clock_reads_count_seconds(step, count):
    try:
        elt = world.firefox.find_element_by_id("display_time_text")
        assert elt.text == count, "The clock reads %s seconds. Expected %s seconds" % (elt.text, count)
    except:
        assert False, "Can't find the clock"

@step(u'the patient chart reads "([^"]*)"')
def the_patient_chart_reads_text(step, text):
    elt = world.firefox.find_element_by_id("patient-chart-text")
    assert elt.text == text, "The patient chart reads %s. Expected %s" % (elt.text, text)

