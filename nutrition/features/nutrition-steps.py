from lettuce import world, step
import time


@step(u'there are ([0-9][0-9]?) topics')
def there_are_count_topics(step, count):
    try:
        elts = world.browser.find_elements_by_css_selector(
            "div.accordion-group")
        assert len(elts) == int(
            count), "There %s topics. Expected %s" % (len(elts), count)
    except:
        time.sleep(1)
        elts = world.browser.find_elements_by_css_selector(
            "div.accordion-group")
        assert len(elts) == int(
            count), "There %s topics. Expected %s" % (len(elts), count)


@step(u'the clock reads ([^"]*) seconds?')
def the_clock_reads_count_seconds(step, count):
    try:
        elt = world.browser.find_element_by_css_selector(
            "span.display_time_text")
    except:
        assert False, "Can't find the clock"

    assert elt.text == count, \
        "The clock reads %s seconds. Expected %s seconds" % (elt.text, count)


@step(u'the patient chart is empty')
def the_patient_chart_is_empty(step):
    elt = world.browser.find_element_by_id("patient-chart-text")
    try:
        assert elt.text == "", \
            "The patient chart reads %s. No text expected" % (elt.text)
    except:
        time.sleep(1)
        assert elt.text == "", \
            "The patient chart reads %s. No text expected" % (elt.text)


@step(u'the patient chart contains "([^"]*)"')
def the_patient_chart_contains_text(step, text):
    elt = world.browser.find_element_by_id("patient-chart-text")
    try:
        assert elt.text.find(text) > -1, \
            "The patient chart reads %s. Expected %s" % (elt.text, text)
    except:
        time.sleep(1)
        assert elt.text.find(text) > -1, \
            "The patient chart reads %s. Expected %s" % (elt.text, text)


@step(u'I discuss "([^"]*)"')
def i_discuss_topic(step, topic):
    elts = world.browser.find_elements_by_css_selector("div.accordion-heading")
    for e in elts:
        div = e.find_element_by_css_selector("div.discuss")
        if div.text.find(topic) > -1:
            btn = e.find_element_by_css_selector('.btn.discuss')
            btn.click()
            return

    assert False, "Unable to find %s discussion" % topic


@step(u'all topics are disabled')
def all_topics_are_disabled(step):
    elts = world.browser.find_elements_by_css_selector(".btn.discuss")
    for e in elts:
        value = e.get_attribute('disabled')
        disabled = value == "disabled" or value == "true"
        assert disabled, \
            "%s is %s. Expected all discussion buttons should be disabled." \
            % (e.text, e.get_attribute('disabled'))


@step(u'"([^"]*)" is disabled')
def topic_is_disabled(step, topic):
    elts = world.browser.find_elements_by_css_selector("div.accordion-heading")
    for e in elts:
        div = e.find_element_by_css_selector("div.discuss")
        if div.text.find(topic) > -1:
            btn = e.find_element_by_css_selector('.btn.discuss')
            assert btn.get_attribute('disabled') == "true", \
                "%s is %s. Expected this button to be enabled" % (
                btn.text, btn.get_attribute('disabled'))
            return

    assert False, "Could not find %s" % topic


@step(u'"([^"]*)" is enabled')
def topic_is_enabled(step, topic):
    elts = world.browser.find_elements_by_css_selector("div.accordion-heading")
    for e in elts:
        div = e.find_element_by_css_selector("div.discuss")
        if div.text.find(topic) > -1:
            btn = e.find_element_by_css_selector('.btn.discuss')
            value = btn.get_attribute('disabled')
            enabled = value == "false" or value is None
            assert enabled, "%s is %s. Expected this button to be enabled" % (
                btn.text, btn.get_attribute('disabled'))
            return

    assert False, "Could not find %s" % topic


@step(u'I close the discussion')
def i_close_the_discussion(step):
    elts = world.browser.find_elements_by_css_selector(".btn.complete")
    for e in elts:
        if e.is_displayed() and e.is_enabled():
            # There's only one at any given time
            e.click()
