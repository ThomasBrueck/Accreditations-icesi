Feature: Comments Management
  As an authenticated user
  I want to create, edit, and delete comments on factors
  So that I can contribute to factor discussions

  Scenario: Create a comment on a factor
    Given I am logged in as an authenticated user
    When I navigate to the factor comments creation page
    And I create a new comment
    Then I should see a success message for comment creation
    And the comment should appear with pending status

  Scenario: Edit an existing comment
    Given I am logged in as an authenticated user
    When I navigate to the factor comments creation page
    And I create a new comment
    And I navigate to the edit page for the comment
    And I update the comment
    Then I should see a success message for comment update
    And the comment should show the updated content

  Scenario: Delete a comment as author and attempt as non-author
    Given I am logged in as an authenticated user
    When I navigate to the factor comments creation page
    And I create a new comment
    And I delete the comment as the author
    Then I should see a success message for comment deletion
    And the comment should no longer appear
    Given I am logged in as a different authenticated user
    When I attempt to delete the comment
    Then I should see an error message for unauthorized deletion

  Scenario: Approve a comment as admin
    Given I am logged in as an authenticated user
    When I navigate to the factor comments creation page
    And I create a new comment
    And I navigate to the comment review page
    And I approve the comment
    Then I should see a success message for comment approval
    And the comment should have approved status

  Scenario: Disapprove a comment with justification as admin
    Given I am logged in as an authenticated user
    When I navigate to the factor comments creation page
    And I create a new comment
    And I navigate to the comment review page
    And I disapprove the comment with justification
    Then I should see a success message for comment disapproval
    And the comment should have not approved status

  Scenario: View justification for disapproved comment
    Given I am logged in as an authenticated user
    When I navigate to the factor comments creation page
    And I create a new comment
    And I navigate to the comment review page
    And I disapprove the comment with justification
    Given I am logged in as a different authenticated user
    When I navigate to the comment justification page
    Then I should see the justification text