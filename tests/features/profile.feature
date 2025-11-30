Feature: Profile Management
  As an authenticated user
  I want to view and edit my profile
  So that I can manage my personal information

  Scenario: View profile with basic information
    Given I am logged in as an authenticated user
    When I navigate to the profile page
    Then I should see my name, role, and email
    And I can click the "Edit Profile" button to go to the edit page

  Scenario: Update profile picture successfully
    Given I am logged in as an authenticated user
    When I navigate to the profile edit page
    And I upload a valid image and save changes
    Then I should see a success message
    And my profile should show the updated image