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
        The patient chart reads "Initial data for the patient chart."

        Finished using Selenium
