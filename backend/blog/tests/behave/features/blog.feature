Feature: Article

  Scenario: Add new comment
    Given An url
    When I create profile
      And log in
      And create article
      And create comment "Good article!"
    Then I should see "Good article!" in page
