Feature: Login

    Scenario: 1. Verify Initial Setup
        Using selenium
        Given I am logged in as match_participant_one
        Then I am at the Welcome page

        When I click the "Module 2: Nutrition" link
        Then I am at the Introduction page

        There is no previous navigation
        There is next navigation

        When I navigate to the next page
        Then I am at the Counseling Session page
        There are 7 topics
        The clock reads 10 seconds
        The patient chart is empty

        Finished using Selenium

    Scenario: 2. Verify Basic Functionality
        Using selenium
        Given I am logged in as match_participant_one
        When I click the "Module 2: Nutrition" link
        When I navigate to the next page
        Then I am at the Counseling Session page
        There are 7 topics

        When I discuss "Topic One"
        Then all topics are disabled
        Then I wait 1 second
        Then the clock reads 9 seconds

        When I close the discussion
        The patient chart contains "Initial Data For The Patient Chart."
        The patient chart contains "summary text one"
        The patient chart contains "summary reply two"

        And "Topic One" is disabled
        And "Topic Two" is enabled
        And "Topic Three" is enabled
        And "Topic Four" is enabled
        And "Topic Five" is enabled
        And "Topic Overtime" is enabled
        And "Topic Undertime" is enabled

        When I navigate to the previous page
        When I navigate to the next page

        Then there are 7 topics
        Then the clock reads 9 seconds
        The patient chart contains "Initial Data For The Patient Chart."
        The patient chart contains "summary text one"
        The patient chart contains "summary reply two"

        And "Topic One" is disabled
        And "Topic Two" is enabled
        And "Topic Three" is enabled
        And "Topic Four" is enabled
        And "Topic Five" is enabled
        And "Topic Overtime" is enabled
        And "Topic Undertime" is enabled

        Finished using Selenium

    Scenario: 3. Countdown to zero, topics disable based on available time
        Using selenium
        Given I am logged in as match_participant_one
        When I click the "Module 2: Nutrition" link
        When I navigate to the next page
        Then I am at the Counseling Session page
        There are 7 topics
        There is no next navigation
        There is not a "Counseling Session Two" link

        When I discuss "Topic Five"
        Then I wait 7 seconds
        Then the clock reads 5 seconds
        Then I close the discussion

        When I discuss "Topic Four"
        Then I wait 6 seconds
        Then the clock reads 1 seconds
        Then I close the discussion

        And "Topic One" is enabled
        And "Topic Two" is disabled
        And "Topic Three" is disabled
        And "Topic Overtime" is disabled
        And "Topic Undertime" is disabled

        When I discuss "Topic One"
        Then I wait 2 second
        Then the clock reads 0 seconds
        Then I close the discussion

        The patient chart contains "Initial Data For The Patient Chart."
        The patient chart contains "summary text one"
        The patient chart contains "summary reply two"
        The patient chart contains "summary text four"
        The patient chart contains "summary reply four"
        The patient chart contains "summary text five"
        The patient chart contains "summary reply five"

        Then all topics are disabled
        Then I see "You've run out of time!"
        Then there is next navigation
        There is a "Counseling Session Two" link

        When I navigate to the previous page
        When I navigate to the next page

        There are 7 topics
        Then all topics are disabled
        Then I see "You've run out of time!"
        Then there is next navigation
        There is a "Counseling Session Two" link
        Then the clock reads 0 seconds

        Finished using Selenium

    Scenario: 4. Countdown to negative, topics disable based on available time
        Using selenium
        Given I am logged in as match_participant_one
        When I click the "Module 2: Nutrition" link
        When I navigate to the next page
        Then I am at the Counseling Session page
        There are 7 topics
        There is no next navigation
        There is not a "Counseling Session Two" link
        The clock reads 10 seconds

        When I discuss "Topic Five"
        Then I wait 7 seconds
        Then the clock reads 5 seconds
        Then I close the discussion

        When I discuss "Topic Three"
        Then I wait 5 seconds
        Then the clock reads 2 seconds
        Then I close the discussion

        And "Topic One" is enabled
        And "Topic Two" is enabled
        And "Topic Three" is disabled
        And "Topic Four" is disabled
        And "Topic Five" is disabled
        And "Topic Overtime" is enabled
        And "Topic Undertime" is disabled

        When I discuss "Topic Overtime"
        Then I wait 7 seconds
        Then the clock reads -3 seconds
        Then I close the discussion

        The patient chart contains "Initial Data For The Patient Chart."
        The patient chart contains "summary text three"
        The patient chart contains "summary reply three"
        The patient chart contains "summary text five"
        The patient chart contains "summary reply five"
        The patient chart contains "summary text overtime"
        The patient chart contains "summary reply overtime"

        Then all topics are disabled
        Then I see "You've run out of time!"
        Then there is next navigation
        There is a "Counseling Session Two" link

        When I navigate to the previous page
        When I navigate to the next page

        There are 7 topics
        Then all topics are disabled
        Then I see "You've run out of time!"
        There is next navigation
        There is a "Counseling Session Two" link
        The clock reads -3 seconds

        Finished using Selenium

    Scenario: 5. Answer all the questions, still have time left on the clock
        Using selenium
        Given I am logged in as match_participant_one
        When I click the "Module 2: Nutrition" link
        When I navigate to the next page
        Then I am at the Counseling Session page
        There are 7 topics

        When I discuss "Topic Five"
        Then I wait 7 seconds
        Then the clock reads 5 seconds
        Then I close the discussion

        When I discuss "Topic Overtime"
        Then I wait 5 seconds
        Then the clock reads 0 seconds
        Then I close the discussion

        The patient chart contains "Initial Data For The Patient Chart."
        The patient chart contains "summary text five"
        The patient chart contains "summary reply five"
        The patient chart contains "summary text overtime"
        The patient chart contains "summary reply overtime"

        When I navigate to the next page
        Then I am at the Counseling Session Two page
        There are 2 topics
        The clock reads 5 seconds
        The patient chart contains "Initial Data For The Patient Chart."
        The patient chart contains "summary text five"
        The patient chart contains "summary reply five"
        The patient chart contains "summary text overtime"
        The patient chart contains "summary reply overtime"

        When I discuss "Topic One"
        Then I wait 2 seconds
        Then the clock reads 4 seconds
        Then I close the discussion

        The patient chart contains "Initial Data For Second Counseling Session."
        The patient chart contains "summary text one"
        The patient chart contains "summary reply one"

        When I discuss "Topic Two"
        Then I wait 4 seconds
        Then the clock reads 2 seconds
        Then I close the discussion

        The patient chart contains "Initial Data For Second Counseling Session."
        The patient chart contains "summary text one"
        The patient chart contains "summary reply one"
        The patient chart contains "summary text two"
        The patient chart contains "summary reply two"

        Then all topics are disabled
        Then I see "You've completed your session!"

        When I navigate to the previous page
        When I navigate to the next page

        Then all topics are disabled
        Then I see "You've completed your session!"

        Finished using Selenium