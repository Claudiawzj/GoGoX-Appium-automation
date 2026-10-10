# GoGoX Appium assignment

Status: Python/Pytest page objects now cover existing-account login and the
Transport booking steps through Review with a HK$20 tip. The integrated booking
test passed on the iPhone: **1 passed in 149.15 seconds from a signed-out account** on 10 October 2026. Fresh-account registration and the demo
recording remain pending; an existing-account run does not complete the assignment.
See GETTING_STARTED.md for the earlier checkpoint results and current run record.

## Selected tools

Python/Pytest, Appium 3.8.0, XCUITest 12.16.0 and pytest-html. Stable Appium and driver
versions were checked against the official npm registry on 10 October 2026. Python
dependency versions are captured in requirements.txt after installation.

## Prerequisites

A Mac with suitable Xcode, connected/trusted iPhone, Developer Mode and Enable UI
Automation enabled, GoGoX installed, Node.js compatible with Appium, and Python.
WebDriverAgent needs signing configured through an Apple account in Xcode. Complete
this setup before attempting the connection test.

The initial connection attempt built WebDriverAgent successfully with Xcode 16.4
and the selected Personal Team. The iPhone refused its launch because developer
trust is required. Complete Settings → General → VPN & Device Management →
Developer App → Trust for that Personal Team account, then retry. The attempt did
not reach the GoGoX foreground assertion and performed no booking actions. The user
then completed trust, and the retry launched GoGoX and passed its foreground check.
The connection test makes no taps and starts no booking.

## Install

Open a terminal in this automation directory:

```sh
npm ci
npm run driver:install
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm run doctor
```

The Appium server and driver are stored inside this project. The Python environment
also stays in this project. Keep generated directories out of the submission ZIP.
requirements.in lists direct Python dependencies; requirements.txt locks the installed
versions, including their dependencies.

## Version control

This project is prepared for GitHub delivery. Only source files, dependency locks and
documentation belong in the repository. Local device/signing configuration, installed
tools and raw test reports are excluded by .gitignore. The existing manual report and
original screenshots remain outside this automation repository.

## Configure

Copy config/device.example.yaml to config/device.local.yaml. Populate the actual
device identifier, verified GoGoX bundle identifier, signing team and unique WDA bundle
identifier during guided setup. Do not guess these values. The local file is excluded
from version control. The server listens on this Mac only.

## Run the first connection check

Start Appium in one terminal:

```sh
npm start
```

In another terminal in the same automation directory:

```sh
.venv/bin/python -m pytest --device tests/test_connection.py --html=reports/connection.html --self-contained-html
```

This launches the configured app and explicitly waits for its foreground state. It
does not tap controls or start a booking. An unconfigured device run fails with the
missing configuration fields. Running without --device skips the device test; a skip
is not proof that automation works.

## Inspect and verify the initial screen

Capture an actual screenshot and UI hierarchy without tapping controls:

```sh
.venv/bin/python -m utils.inspect_screen
```

The helper waits explicitly for visible controls, then saves private evidence under
reports/inspection. It does not assume that the app's foreground state means it has
finished loading. Raw evidence can contain personal information and stays out of Git.

Check the inspected Home Page locators on the actual phone:

```sh
.venv/bin/python -m pytest --device tests/test_home_controls.py --html=reports/home-controls.html --self-contained-html
```

This check expects the English Transport screen with empty From/To fields. It makes
no taps. Do not silently clear an existing draft route to make it pass.

Copy config/data.example.yaml to config/data.local.yaml. Put the registered account's
email/password in the `login` section on your own Mac. Leave `registration` blank
until preparing the final recorded attempt. The local file is ignored by Git.
Registration automation is not implemented yet.

The existing-account login checkpoint requires the English Transport home screen,
empty From/To fields and a signed-out account. It submits login once and verifies
the Transport screen and menu's authenticated state. It fails if already signed in;
sign out in the app before deliberately repeating this checkpoint. No account
creation, password-reset action or booking action is included.

```bash
.venv/bin/python -m pytest tests/test_login.py --device --html=reports/login.html --self-contained-html
```

Use the project's `npm start` command with warning-level Appium logging when entering
credentials. Verbose HTTP/debug logs can contain typed text. Test step logs omit
credential values; raw screen inspections and reports stay private until reviewed.

The route checkpoint requires a signed-in account at the English Transport home
screen. It deliberately replaces both route fields with the configured practice
locations, selects the exact observed search-result names, verifies the saved
addresses and taps Next. It ends at Time and vehicle without choosing pickup time,
rental duration or extras, and never places an order.

```bash
.venv/bin/python -m pytest tests/test_route.py --device --html=reports/route.html --self-contained-html
```

Location selection may return automatically or retain the resolved address in the
editor. The page object waits for the full selected address, taps Done only if the
editor remains after results disappear, then verifies the saved home field. Home field locators
distinguish the pickup and destination cells, and exact result names are external
data so shops inside the mall cannot be silently selected instead.

The time/vehicle checkpoint starts at Time and vehicle with the approved route
already saved. It selects a pickup two days ahead at 14:00 in Hong Kong time,
four-hour rental and Van, verifies all three and taps Next. It ends at Order details
with Cargo compensation visible. It does not select Basic or any extras yet.

```bash
.venv/bin/python -m pytest tests/test_time_vehicle.py --device --html=reports/time-vehicle.html --self-contained-html
.venv/bin/python -m pytest tests/test_pickup_plan.py
```

`booking.pickup.days_ahead` and `time_24h` externalize the pickup plan. The date is
recalculated for each run in Asia/Hong_Kong, and invalid/past-day or non-ten-minute
slots fail rather than use ASAP. Device selectors require the English UI. iOS picker
times use a narrow nonbreaking space before am/pm; the picker action supplies that
exact format, while assertions normalize spacing. Van is verified using the check
mark inside its own card, not a check mark anywhere on screen.

The time/vehicle page's Next button has a shared internal ID containing review_order.
Its action is scoped to the Time and vehicle title and verified selections. Do not
reuse it as a generic footer action or order-submission command.

Run checkpoint tests individually in their stated starting screens. They are not
yet a complete suite with automated state setup; do not run all device tests as
proof of the full assignment flow. To repeat the route checkpoint after it passes,
tap Back from Time and vehicle to return to home.
To repeat the time/vehicle checkpoint, tap Back from Order details to Time and vehicle.

Reserve the unused email for the final recorded full-flow attempt. During development,
inspect registration without submitting it and exercise login/booking with an existing
test account. Start recording before creating the new account. Existing-account runs
verify reusable steps but do not satisfy the required new-account registration step.
Do not automatically retry signup after successful creation or an uncertain submission
outcome. A repeat of the complete fresh-registration flow may require another unused
email; GoGoX email reuse and deletion behavior have not been verified.

## Structure and safeguards

- pages: Home, menu/login, location, pickup/time/vehicle, order details and review actions; separate locator modules.
- tests: test logic and checkpoint assertions.
- utils: reusable helpers and configuration loading.
- config: capabilities and external login/route test data.
- reports: HTML reports, step logs and selected evidence.

The full flow must include registration/login, route, future pickup date/time,
4-hour hourly rental, Van, Basic $10, all requested extras, dummy contacts and $20 tip.
Record the installed app's contact-entry sequence discrepancy. Stop at review; never
place or confirm an order. No order-submission action will be implemented.

The user approved IFC Mall → Harbour City and Cross-Harbour Tunnel (Hung Hom) for
practice. The mall results at Finance Street and Canton Road have been inspected.
Remaining test data and booking locators still need inspection. Registration
prerequisites and implementation remain pending.
Rehearse the reusable steps first, then record the complete fresh-registration attempt
from its start. Review the recording and results before submission packaging.

## Run the booking practice from Transport

Keep the iPhone connected and unlocked with Appium running. The test checks the
account menu, logs in once using config/data.local.yaml login credentials if it finds
a guest, and verifies the Personal account before booking. It skips password entry
when already signed in. Populate booking.contact in the private data file with dummy details. This
test restarts GoGoX without resetting account data, verifies that the account is signed in,
enters the approved route, sets
future pickup/four-hour Van, selects all required extras, saves contacts on Review,
adds HK$20 tip, verifies the fee breakdown, captures evidence and stops.

```sh
.venv/bin/python -m pytest tests/test_transport_booking.py --device --html=reports/transport-booking.html --self-contained-html
```

The custom plus and checkbox controls expose no accessible identifiers or selected
state. Their taps are anchored to the inspected semantic row at its right edge.
Passenger/cart counts are checked immediately; required extras and prices are
verified in the Review fee breakdown, including Driver tip $20 and Basic $10.
The unchecked toggles require a fresh draft; restart provides that observed initial
state and passenger/cart guards reject an already edited draft. Do not resume this
method halfway through selected extras. Raw screenshots/reports remain local.

In this app version, Order contact info is edited after Review Order. Its three
unnamed fields are identified by vertical order (name, phone, optional extension),
reacquired after each edit and verified before Save. The saved contact summary is
also asserted. Contact Save and tunnel-sheet Confirm are guarded by their sheet
content. The footer shares the same identifier on Next, Review and Place order;
only the first two are implemented, with the corresponding page guard. ReviewPage
has no footer click or submission method.

### Signed-out start

The booking test now supports both signed-out and signed-in starts. Use the same
command above. Existing login data stays under login in the ignored private file;
registration remains separate and blank for the future new-account recording.
Unknown menu state or failed login stops the test before booking. The password is
submitted once; no automatic password retries. A signed-out booking attempt before
this fix reached guest Order details without Cargo compensation and timed out.
