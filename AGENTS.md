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

### Transport-to-Review update — 10 October 2026

Integrated test tests/test_transport_booking.py passed on the physical iPhone:
1 passed in 127.54 seconds. Restart preserved the existing account, rebuilt the
approved route, future pickup/four-hour Van and all required extras, saved dummy
contacts, added $20 tip and asserted Review fee breakdown. Phone stopped at Review;
no order placed. Evidence stays ignored under reports/transport-booking*.

LocationPage supports automatic return or settled editor followed by Done; never
confirm before the full selected address is resolved. OrderDetailsPage uses semantic
rows and observed right-edge taps for inaccessible custom controls. Counts checked
immediately, all required fees verified on Review. Contact fields have no IDs;
reacquire by vertical order and verify values before Save plus saved summary. ReviewPage
never clicks the footer. Tunnel Confirm is guarded by the preference-sheet explanation.

Existing-account practice is verified, not fresh registration. Registration/login-to-
booking integration and demo recording remain pending. Reserve unused email for recording.
Earlier status bullets describe past checkpoints; this update is the current handoff.

### Automatic existing-account login — 10 October 2026

User's 22:59 run started signed out. The old booking test assumed prior login and
never invoked LoginPage, so it entered guest Order details and timed out on Cargo
compensation. Read-only inspection confirmed the guest Log in or sign up control and
no Cargo compensation section. This is an automation precondition/integration gap,
not evidence of a GoGoX product defect.

Updated test_transport_booking.py now opens the menu immediately after restart,
waits for a verified guest or Personal-account state, logs in once using the existing
login credentials when guest, verifies Personal account, closes the menu and starts
route entry. An already signed-in account skips password submission. Unknown account
state or failed login stops before booking. Login failures suppress nested frames
that could expose credential arguments. No signup or password retry is performed.

Verified the corrected full test from the actual signed-out state: **1 passed in
149.15 seconds**. Log records guest detection, email/password login, Personal account
confirmation, route, future pickup/four-hour Van, Cargo compensation and required
extras, saved dummy contact, Driver tip $20 and Review fee assertions. Phone ends at
Review; no order placed. Latest transport-booking.html, console log and final screenshot
are from this successful corrected run. Prior failure preserved as
reports/transport-booking-signed-out-failure.html; all reports remain private and ignored.

Same booking command now works after sign out as well as while signed in. Existing
credentials stay under login; registration remains blank for the new-account recording.
Earlier helper-authorization problem did not recur during this run. Its original
trigger is still unestablished; do not attribute it to a disabled UI Automation switch.

### Single startup and Van-card selection — 10 October 2026

User's 23:12 run successfully logged in, then timed out waiting for the Van card's
own card-check marker. Inspection after the failure showed 5.5t Truck selected.
The exact cause of the old label-tap outcome was not established; do not classify
this as a GoGoX product defect. Changed Van action to wait for consecutive equal
whole-card rectangles, tap the Van Cell and retain the scoped check assertion.
A direct check on the current failed screen selected Van and verified its marker.

The booking fixture previously auto-launched GoGoX before the test restarted it.
Added restart_app marker: only the booking session disables autoLaunch; the test
owns one terminate/activate startup. Other checkpoints keep their original launch.

Login code does not paste or use clipboard commands. It uses element.send_keys.
Inspection of the installed helper's value handler and typing category confirms
synthesized text-input events. A visible iOS Paste edit menu does not establish a
Paste action; its exact appearance trigger was not captured. No typing changes made.

Full corrected test passed while already signed in: **1 passed in 134.00 seconds**.
Log confirms session connected without auto-launch, one test-owned startup,
signed-in branch skipped password submission, stable Van card selected/asserted,
all required extras/contact and Driver tip $20 verified, then stop at Review.
No order placed. Earlier signed-out branch verified in the preceding 149.15-second
run; latest failed user run also confirms successful login before its Van timeout.

Latest reports/transport-booking.html, console log and final screenshot are from this
134-second success. Previous user failure saved to reports/transport-booking-van-failure.html;
van-failure and van-card-corrected XML/screenshots remain private under reports/inspection.
All evidence excluded from Git. Same manual test command remains valid.

### Paste-menu investigation and login focus fix — 10 October 2026

Temporarily signed out for a controlled email-field diagnostic using only
focus-check@example.invalid. Dummy address was never submitted: no Next, signup
or login action with it. Initial email screen had keyboard hidden and no Paste menu.
One explicit tap opened keyboard without Paste. Original tap-plus-send_keys sequence
had no menu in its post-action snapshots, so these snapshots do not prove that the
helper made a second tap in the user's earlier run. A deliberate second tap on an
already focused empty email field reproduced the Chinese Paste/AutoFill popup,
confirmed in source and screenshot. send_keys alone on a fresh email screen typed
the dummy address successfully without a separate explicit click.

Installed WDA's fb_typeText calls fb_prepareForTextInputWithSnapshot, which taps if
it cannot detect input focus. This provides a possible additional tap in the old
path, but that internal branch was not recorded in the earlier user run. The
controlled result supports the extra-focus-tap explanation without asserting an
unobserved exact old sequence. No clipboard or Paste command was used.

Removed field.click and the preceding keyboard wait from LoginPage._type_private.
send_keys now owns focus; an explicit keyboard check follows typing. Existing secret-
suppression behavior remains. Verified both existing email/password entry and Personal
account confirmation: tests/test_login.py **1 passed in 21.59 seconds**. Restored the
user's registered account after the experiment; no account created, booking or order
submission. This was a login-only check, not another full booking run/demo video.

Private evidence: reports/inspection/focus-second-explicit-tap.png/.xml,
focus-typing-without-explicit-tap.png/.xml, initial/first-tap/post-typing captures and
focus-comparison.json. Login report reports/login-single-focus.html and console log
remain ignored. All credential checks passed before committing. Current task's
next step remains fresh-registration implementation and full assignment recording.

### Contact-entry focus fix — 10 October 2026

Removed the explicit contact-field tap before clear/send_keys. Existing content is
cleared only when it differs from the requested value and is nonempty; fields are
reacquired after clearing. Empty optional extension is left untouched. Appium now
owns input focus, matching the login fix. Per-field, combined-value and saved-contact
summary assertions remain. The old contact path had an extra focus action, but its
exact popup trigger was not recorded. No clipboard/Paste action is used.

Connected-iPhone booking test passed: **1 passed in 125.67 seconds**. Already signed
in; route, future pickup, four-hour Van, required extras, saved dummy contact and
HK$20 tip all verified. Stopped at Review; no order placed. This verifies retained
values and successful completion, not absence of every transient edit menu.
Latest private report: reports/transport-booking.html; console log and final screenshot
are from this run. No recording or registration performed. Phone remains at Review.
Fresh-registration implementation and full assignment recording remain pending.

### Registration recording preparation — 11 October 2026

User filled registration email/password privately and requested code changes only;
explicitly leave phone execution and screen recording to the user. Both registration
and existing-login credentials are present; no values printed. Prepared uncommitted
registration credential loader, --register option and Settings/Profile sign-out helper
using cached observed locators. These drafts are not yet integrated into the booking
test: do not instruct the user to run --register until integration is complete.

Registration form evidence is missing. Asked user to sign out, enter the unused email,
tap Next and report the title, fields and submit label, stopping before account creation.
Need that information to finish registration locators/actions without inventing controls.
No device session, account creation, pytest execution, recording or GitHub push performed.
Existing booking test still performs existing-account login only. Preserve both private
credential sections and stop at Review with HK$20 tip. Next: integrate registration,
explicit logout/login and existing booking flow; perform offline checks only, then give
user the recording command with --register. No automation execution by the assistant.

### New-account recording mode implemented — 11 October 2026

User supplied signup screenshot: “Sign up for a Hong Kong account”, Name (Optional),
Password, two already-selected checkboxes and Sign up. Implemented RegistrationPage
and separate locators from that screenshot plus existing login control conventions.
Native signup identifiers remain unverified; password and submit use guarded semantic
predicates/visible labels with unique visible matching. Optional name stays blank;
checkboxes stay untouched. Signup is submitted once, followed by Transport/Personal
account assertions, Settings → Personal → Profile sign out, guest assertion, and one
login using the new registration credentials. Existing login data is never overwritten.

The same test now accepts --register, restricted during collection to this single test
with --device. It requires a signed-out start and rejects a registration address matching
existing login. Without --register, existing booking/login behavior is retained. No
signup or password retries and no order-submission method. Stop at Review with HK$20.
Private registration fields validate without printing values. No device session/run was
performed, per the user's explicit request. Six offline credential-separation tests
passed; the new command collects one device test; an incorrect --register target is
rejected during collection. Initial offline fixture omitted method: email; corrected
that fixture, all six pass. No fresh-account success or recording claimed.

User recording command (Appium already running):
.venv/bin/python -m pytest tests/test_transport_booking.py --device --register --html=reports/full-flow.html --self-contained-html
Return from the unsubmitted form to English Transport while signed out, connect/unlock
phone, start recording, then execute. Signup consumes the email only if creation occurs;
a later booking failure does not make it unused again. Check app/account state before
repeating --register. A further complete registration recording may need another unused
email; a repeatable booking can use the now-registered credentials under login without
--register. User owns the first device verification and video recording. Existing
125.67-second booking report remains unchanged. Next: inspect user's full-flow report
and recording; address any actual failure, then prepare final delivery notes/packaging.
