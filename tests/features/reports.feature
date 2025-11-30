Feature: Reports Filtering
  As an authenticated user
  I want to filter reports by search and status
  So that I can find relevant reports

  Scenario: Filter reports with active search
    Given I am logged in as an authenticated user
    When I navigate to the reports page
    And I apply a filter with an active search
    Then the results should match both search and filter

  Scenario: Verify intuitive filter interface
    Given I am logged in as an authenticated user
    When I navigate to the reports page
    And I apply a filter with an active search
    Then the filter tags should be visible