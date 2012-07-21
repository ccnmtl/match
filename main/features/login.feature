Feature: Login

    Scenario: 1. Login - Test Invalid Login
        Using selenium
        Given I am not logged in
        When I access the url "/"
        Then I am at the Login page
        When I type "foo" for username
        When I type "foo" for password
        When I log in with a local account
        Then I am at the Login page
        Then I see "Invalid username or password"
        Finished using Selenium

    Scenario: 2. Login - Test Valid Login
        Using selenium
        Given I am not logged in
        When I access the url "/"
        Then I am at the Login page
        When I type "match_participant_one" for username
        When I type "test" for password
        When I log in with a local account
        Then I am at the Welcome page
        Then I see "logged in as match_participant_one"
        Then there is a "logout" link
        When I click the "logout" link
        Then I am at the Login page
        Finished using Selenium