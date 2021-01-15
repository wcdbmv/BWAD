Feature: Article

  Scenario: Add new comment
    Given My account
      And exists article
    When I create comment "Good article!"
    Then I should see "Good article!" in page
