# GoGoX Appium assignment

## Non-negotiable stop boundary

Stop at the review screen after adding a HK$20 tip. Never place or confirm an order,
including during exploration, retries, debugging or demo recording. Do not implement
an order-submission action.

## Required automation flow

Automate the same Hong Kong iOS Transport flow as the manual walkthrough:

1. New-account registration and login.
2. Enter From and To locations and proceed.
3. Future pickup date/time, Hourly Rental – 4 hours, Van, and proceed.
4. Cargo Compensation: Basic $10.
5. Three passengers, Premium, Rent a Cart +1, goods longer than 6ft,
   pet-friendly driver, English-speaking driver, Tunnel Preference and Move-to-door.
6. Dummy Order Contact Info and Review Order. In the manually tested app version,
   contact editing occurs after Review Order; preserve and document the actual UI sequence.
7. Add HK$20 tip and stop at review.

Do not silently omit missing options or substitute values. Distinguish verified UI
behavior from proposed implementation. Do not invent locators, screenshots or results.

## Framework requirements

Python/Pytest with Appium and XCUITest. Use Page Object Model with separate locators,
page actions and test logic. Keep pages, tests, utils, config and reports modular.
Externalize capabilities and test data. Use explicit waits rather than fixed sleeps.
Assert meaningful checkpoints, log steps and generate pytest-html reports. Verify the
latest stable Appium release when updating the tooling. Provide setup/run instructions,
assumptions/challenges/improvements, and a recording of a verified complete run.

## Current status — 10 October 2026

- Appium 3.8.0 and XCUITest 12.16.0 installed locally.
- iPhone 13 Pro, iOS 26.3; GoGoX 7.111.0, Hong Kong.
- Xcode 16.4 built and ran WebDriverAgent after Personal Team developer trust.
- Connection test passed: 1 passed in 22.96 seconds. It only launches GoGoX and
  verifies foreground state. It performs no booking actions.
- Full booking test and page objects have not been implemented.
- Registration inputs, final route and runtime test data still need resolution.
- Full-flow recording and submission are pending. GitHub is the preferred delivery.

Local device/account configuration, tool installations and raw reports are excluded
from Git. Do not commit secrets or screenshots containing private account/verification
data. Review evidence before sharing. Never email the submission without a recipient
and explicit send instruction.

The user is learning automation. Explain each step simply and distinguish actions
performed by the assistant on the Mac from actions the user performs on the phone.
