Feature: Temperature conversion
  Scenario: Convert celsius to fahrenheit
    Given a celsius temperature of 0
    When converted to fahrenheit
    Then the result should be 32
