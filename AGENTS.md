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
- Read-only Home Page object and separately stored locators implemented and verified:
  one home-control test passed in 3.56 seconds, without taps or data entry.
- Email chosen for new-account registration; user can use an unregistered email.
  Fresh registration code/data remain pending. Existing credentials are provided locally
  under login, not registration; both registration credential fields remain empty.
- Existing-account LoginPage/MenuPage and separate locators implemented. Complete
  signed-out-to-signed-in checkpoint passed: 1 passed in 24.24 seconds. First attempt
  logged in but failed an incorrect menu assertion; GoGoX retains a disabled sign-in
  control. Corrected and verified on a deliberate retry after sign out.
- Phone currently signed in at Order details with Cargo compensation visible.
  Never automatically retry passwords.
  Login test requires signed-out Transport home with empty route fields.
- User approved IFC Mall → Harbour City and Cross-Harbour Tunnel (Hung Hom) for practice;
  exact mall search results inspected and saved in external data. Route checkpoint
  passed: 1 passed in 22.94 seconds, ending at Time and vehicle. Full result names:
  ifc mall, Finance Street, Central, Hong Kong; Harbour City, Canton Road, Tsim Sha Tsui, Hong Kong.
- LocationPage selects exact results and waits for automatic home return/persisted
  field value. Do not tap Done after selecting a result: an early tap interrupted
  destination persistence during inspection. Do not call this a confirmed app bug.
- Native home table's first/second Cell TextViews are pickup/destination. Search has
  one TextView. Route test intentionally replaces fields; login/home-control tests
  still require their documented empty-route/signed-out state. Run checkpoints separately.
- Local file was found with old registration-only layout after the user's screenshot;
  restored registered credentials to login and left registration empty. Cause unknown;
  reload stale editor content before saving. Do not print credentials.
- Reserve the unused email for the final recorded full-flow attempt. Inspect registration
  without submitting it; develop reusable login/booking steps using an existing account.
  Start recording before account creation. Do not automatically retry signup after a
  successful creation or an uncertain submission outcome. An existing-account run does
  not satisfy the assignment's new-account checkpoint. A fresh full-flow retry may need
  another unused email; GoGoX email reuse/deletion behavior has not been verified.
- Future pickup, 4-hour rental and explicit Van action/assertion verified: 1 passed
  in 20.84 seconds. Plan uses Hong Kong date plus two days at 14:00 (12 October 2026
  for this run), calculated each execution. Calendar/configuration tests: 10 passed.
- Time wheel requires narrow nonbreaking space before am/pm for actual selection.
  Normalize UI spacing for assertions, and verify both wheel values and saved summary.
  Plain-space input did not change the time during inspection; this is not an app bug.
- PickupPage and TimeVehiclePage configure and verify all settings, then Next to
  Order details. Van check mark is scoped to its own Cell, not a global check image.
  The Next footer ID contains review_order but must only be used in verified Time
  and vehicle context. No generic footer or order-submission action is implemented.
- OrderDetailsPage currently only confirms title, Cargo compensation and Basic
  markers. No compensation/extra selection actions yet. Next: Basic $10 and required extras.
- Full booking test, other booking page objects and new registration remain pending.
- Appium server restarted with warning-level logging (exec session 25011). Verify
  readiness before reuse. Typed credentials were absent from checked login reports
  and server log; raw private screen inspections must remain ignored.
- Full-flow recording and submission are pending. GitHub is the preferred delivery.

Local device/account configuration, tool installations and raw reports are excluded
from Git. Do not commit secrets or screenshots containing private account/verification
data. Review evidence before sharing. Never email the submission without a recipient
and explicit send instruction.

The user is learning automation. Explain each step simply and distinguish actions
performed by the assistant on the Mac from actions the user performs on the phone.
