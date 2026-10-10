# GoGoX automation — beginner guide

## Our choices

- Device: the same physical iPhone 13 Pro used for Part 1 (user confirmed availability).
- Language/framework: Python/Pytest, the assistant's preferred option for this assignment.
- Mobile automation: Appium with Apple's XCUITest driver.
- Reporting: pytest-html (planned).
- Boundary: finish at review with the $20 tip shown. Never place or confirm an order.

## What the tools do

Python contains the instructions for the test. Pytest runs those instructions and records whether checks pass. Appium receives instructions from Python and sends them to the phone through XCUITest. On a real iPhone, this uses a development-signed helper called WebDriverAgent. Xcode is Apple's software for building and signing that helper.

A locator identifies a particular field or button. We will obtain locators from the actual installed app, rather than guess them from screenshots. A page object groups the actions for a screen. An explicit wait waits until a specific condition is true, such as a button becoming available. An assertion checks an expected result.

## Setup checks — 10 October 2026

| Item | Observed status |
| --- | --- |
| Mac | Apple Silicon, macOS 15.7.4 |
| Xcode | 16.4, selected at /Applications/Xcode.app/Contents/Developer |
| Node.js | 24.14.1; meets current Appium requirements |
| npm | 11.11.0; meets current Appium requirements |
| Python | 3.14.3; project dependencies not installed or verified yet |
| Appium | 3.8.0 installed locally; XCUITest 12.16.0 installed and loaded by server |
| Device | Paired over USB, iOS 26.3 (23D127), Developer Mode enabled; user confirmed Enable UI Automation |
| GoGoX | Installed app confirmed: 7.111.0, bundle identifier hk.gogovan.GoGoVanClient |
| Python tools | Appium-Python-Client 6.0.7, pytest 9.1.1, pytest-html 4.2.0, PyYAML 6.0.3 installed; dependency check passes |

Appium 3.8.0 was verified by querying the official npm registry. The 4.0.0 beta tag is a prerelease. Check the stable tag again when installing if installation happens in a later session.

Xcode 16.4 bundles the iOS 18.5 SDK. Earlier advice that an upgrade was mandatory was too definite. The current XCUITest driver supports Xcode 16, and the actual WebDriverAgent test build succeeded on this Mac. It emitted a deployment-target warning, but the immediate launch failure concerns device trust. Continue with the current toolchain and reassess compatibility only if an actual later failure warrants it.

The initial device-list command timed out while initializing CoreDeviceService in the restricted execution environment. This does not establish that the iPhone is disconnected or defective. No device automation has run.

The user supplied an Xcode Devices and Simulators screenshot showing the iPhone under Connected with no visible warning. Subsequent device discovery independently confirmed USB pairing and Developer Mode. Device identifiers are kept in the ignored local configuration, not in shareable setup notes.

## First connection test — actual result

The first device test was attempted on 10 October 2026. WebDriverAgent built successfully using Xcode 16.4 and the user's selected Personal Team. Launch failed with Xcode error 65; the specific underlying message says the developer certificate/profile has not been explicitly trusted on the phone. This is a setup failure, not an established GoGoX defect. No GoGoX foreground assertion was reached and no booking actions were performed.

Local diagnostics: reports/connection-attempt.html, reports/connection-console.log and reports/appium.log. These can contain device/account metadata; they are ignored by version control and are not submission-ready evidence. Test collection finds one connection test; collection alone is not a successful device run.

### Next phone action: trust the helper's developer certificate

1. On the iPhone, open **Settings → General → VPN & Device Management**.
2. Under **Developer App**, select the entry matching the Apple account used for the Personal Team in Xcode.
3. Tap **Trust** for that developer and confirm the prompt. Depending on iOS wording, the action may be called **Allow & Restart**; follow its on-screen instructions.
4. Keep the phone connected and unlocked, then report that trust is complete. If no developer entry appears, report that rather than trusting a different entry.

This permits the locally signed Appium helper to run. It is separate from Developer Mode. Retry the connection test after the user completes trust; do not claim the first attempt passed.

### Retry after trust — passed

The user confirmed certificate trust. Retried the connection test on 10 October 2026:
**1 passed in 22.96 seconds**. The Appium session launched GoGoX 7.111.0 on the connected
iPhone and verified that it was running in the foreground, then ended the session.
No controls were tapped, no account details were entered and no booking was started.
This verifies the Appium connection, not the full assignment flow.

Local evidence: reports/connection-after-trust.html and reports/connection-after-trust.log.
Keep these local until their setup metadata has been reviewed before sharing.
Next: inspect actual GoGoX controls and introduce page objects while resolving the
new-account registration inputs and final route. A complete booking test remains pending.

The assistant installed Appium and the Python tools during the guided setup after
the user confirmed the phone settings. Appium is stored in automation/node_modules/appium,
the iPhone driver in automation/.appium, and Python tools in automation/.venv. The user
performed the phone settings, account/certificate checks and developer trust manually.
For further beginner instructions, distinguish assistant-operated Mac steps from
user-operated phone steps and explain the purpose before proceeding.

## Home Page inspection and first page object — 10 October 2026

The first read-only capture caught the loading screen. Added an explicit wait for
visible interactive controls before taking a usable screen capture. The second
capture showed the English Transport home screen with empty route fields.

Observed locators in GoGoX 7.111.0:

| Control | Accessibility name |
| --- | --- |
| Menu | home__header__navigation_icon__menu |
| Transport service | Transport |
| Empty From field | Where from? |
| Empty To field | Where to? |
| Proceed control | Next |

Created pages/locators/home.py, a shared explicit-wait helper and HomePage read-only
checks. Verified through Appium on the real phone: **1 passed in 3.56 seconds**.
The check confirmed the controls' visibility/uniqueness, selected Transport and the
empty route labels. It performed no taps. Populated route controls and subsequent
screens still need inspection; do not infer their locators from these placeholders.

The user selected email registration and confirmed an unregistered email is
available. Private config/data.local.yaml prepared from the empty example template;
reserve this email for the final recorded full-flow attempt. Credentials can be entered
locally when needed; do not use this email for development signup attempts. Neither
email nor password has been requested in chat. Git
ignore was verified for that local file. No new account has been created yet.

Registration changes the account stored by GoGoX, so treat a fresh email as a one-time
input. We have not verified whether GoGoX allows reusing it after deleting an account.
We will inspect registration screens without submitting, then develop and rehearse
login and booking using an existing account. These rehearsals do not count as the full
assignment run. When the reusable steps are ready, start recording before registration
and run through to review with the $20 tip. If the attempt fails after account creation,
keep the evidence and expect to need another unused email for a new complete attempt.

## Existing-account login checkpoint — 10 October 2026

The user filled the private local file with a registered email and password. The
assistant moved these values from `registration` into a separate `login` section
without displaying them, and left fresh-registration fields blank. Use `login`
for the existing account; keep an unused email for the final recorded attempt.

Inspected guest menu, email and password screens through Appium. Inputs are custom
accessible controls of type Other; typing directly into the focused control works.
No fixed sleeps are used. Added separate locator files and LoginPage/MenuPage objects.

The first device test submitted login successfully but failed its menu check: GoGoX
retains the old sign-in identifier as a disabled control after login. Corrected the
check to require the Personal account avatar/button, absence of Hi guest and no enabled
sign-in control. The Personal button uses a type-specific locator because its label
also appears as static text. Signed out through Settings → Personal → Log out of your
personal account, then reran the complete login checkpoint: **1 passed in 24.24 seconds**.
The phone is now signed in, with its menu open. No new account or booking was created.

Evidence stays local in reports/login-verified.html and reports/login-verified-console.log.
The earlier failure is retained in reports/login.html and reports/login-console.log.
Appium was restarted with warning-level logging before credentials were entered.
Checked the server log and login reports for the exact credential values; none were
present. Private account screen XML remains ignored and is not submission evidence.

The login test expects a signed-out account at the Transport home screen with empty
From/To fields. It does not automatically sign out or retry passwords. To deliberately
repeat it, sign out in the app and return to home first.

User approved IFC Mall → Harbour City and Cross-Harbour Tunnel (Hung Hom) for practice.
These choices are saved in the external data file; matching actual app search results
and implementing route/booking pages are the next steps.

## Route checkpoint — 10 October 2026

The user confirmed the registered credentials are for login. The saved local file
had reverted to the old registration-only layout; the cause was not established.
Restored `login` with existing credentials, empty `registration`, and approved booking
choices. The file was queued to reopen in Codex. If an editor shows the old layout,
reload it before saving to avoid overwriting the saved configuration again.

Inspected location search on the signed-in phone. The input is a native TextView.
IFC search includes multiple mall/shop entries; the exact chosen result is
`ifc mall, Finance Street, Central, Hong Kong`. The destination result is
`Harbour City, Canton Road, Tsim Sha Tsui, Hong Kong`. Both are external test data.

Selection returns to home automatically. During inspection, an early Done tap
interrupted destination persistence. Corrected the action to wait for the selected
full address in its home field without tapping Done. This is an automation timing
correction; it does not establish a separate GoGoX defect. Home route fields use the
first/second native table cells so pickup/destination are checked independently.

Created LocationPage, route actions in HomePage, exact-result data loader and a
read-only TimeVehiclePage checkpoint. Shared waits ignore transient stale elements
while preserving the uniqueness check. Device test selected both locations, verified
their full addresses and tapped Next: **1 passed in 22.94 seconds**. Evidence:
reports/route.html and reports/route-console.log, kept local and ignored by Git.

The phone is signed in at Time and vehicle. Future date/time, four-hour hourly rental
and Van selection actions are the next implementation step. Inspection showed Today
10 Oct, ASAP and Hourly rental: No; these defaults do not satisfy the assignment.
Van appeared selected, but a required explicit selection/assertion still needs code.
No order was placed and no new account was created.

Checkpoint tests require their documented starting screens and are run individually.
The route test deliberately replaces both route fields; to repeat it, return to home
using Back. The full new-account-to-review flow and recording remain incomplete.

## Future pickup, four-hour rental and Van checkpoint — 10 October 2026

Observed two native wheels for pickup date/time and one for hourly rental. Native
time values use a narrow nonbreaking space before am/pm; the first plain-space attempt
did not select 14:00. Supplied the exact native format and verified the wheel values
and saved summary. This is an automation formatting correction, not an app defect.

External configuration now includes pickup.days_ahead: 2, time_24h: "14:00",
rental_hours: 4 and vehicle: Van. Each run calculates its future date in Hong Kong
time, so it remains reusable. On this run the selected pickup was **12 October 2026,
2:00 PM HKT**. App confirmed **4 hours** and the check mark within the **Van** card.
The code verifies all selections before tapping Next from this specific page.

Created PickupPage, expanded TimeVehiclePage and a read-only OrderDetailsPage endpoint,
with separate locator files. Device checkpoint **1 passed in 20.84 seconds**, ending
at Order details with Cargo compensation visible. No Basic/extras/contact/tip actions
occurred. The phone is now on Order details; no order was placed or new account created.
Evidence: reports/time-vehicle.html and reports/time-vehicle-console.log, kept local.

Ten independent calendar/configuration checks passed, covering year rollover, leap
year, converting UTC to Hong Kong before choosing the date, invalid configuration
and iOS spacing. These tests run without the device and do not prove the full flow.

To repeat this device checkpoint, tap Back to Time and vehicle. Login, route and
time/vehicle checkpoint tests still have separate starting-screen requirements.
Next: inspect/select Basic $10 and all required extras. Full registration-to-review
automation, $20 tip, demo recording and submission remain incomplete.

## First task: connect the phone

1. Connect the iPhone to this Mac with a USB data cable.
2. Unlock the phone. If prompted, tap **Trust** and enter the passcode on the phone.
3. Open **Xcode** on the Mac. Choose **Window → Devices and Simulators**.
4. Select the iPhone under **Devices**. Note whether it is ready, preparing, unpaired, or reporting an unsupported OS. Report the message as shown.

After a compatible Xcode can pair with the device, enable **Settings → Privacy & Security → Developer Mode** on the phone. Follow the restart and confirmation prompts. If the option is absent, initiate pairing in Xcode first. The XCUITest setup also requires **Settings → Developer → Enable UI Automation**. We will check these together after the connection step.

## How we will build the assignment

1. Establish compatible Xcode, trusted connection and device settings.
2. Install the stable Appium server, compatible XCUITest driver, and Python dependencies in the project.
3. Configure and sign WebDriverAgent using an Apple account in Xcode. Credentials stay in Apple's interface; do not paste passwords into chat.
4. Run a small connection test that opens GoGoX without booking anything.
5. Inspect real controls and implement one screen at a time.
6. Assemble the registration/login and Transport flow, asserting the required selections and stopping at review with the $20 tip.
7. Rehearse reusable steps with an existing account. Start recording before the fresh
   registration attempt, then verify the full run and generate an HTML report.
8. Complete the README, assumptions/challenges/improvements note, and ZIP or repository delivery.

The framework will use `pages`, `tests`, `utils`, `config`, and `reports`. No booking test has been implemented yet.

## Details to resolve before the full run

- Current device OS, GoGoX version and Hong Kong market.
- New-account registration data and access to verification, if needed; distinguish any human verification step from automated steps.
- Reuse the observed exact mall results for the user-approved practice route IFC Mall
  → Harbour City. This was not retained as the final route from manual exploration.
- Implement the approved Cross-Harbour Tunnel (Hung Hom) choice; availability still needs inspection.
- Dummy contact details and a pickup date/time that remains future at execution.
- Contact entry appears after Review Order in the manually tested version; record and implement the installed app's actual sequence without silently omitting contact entry.

## Official references

- [Appium requirements](https://appium.io/docs/en/latest/quickstart/requirements/)
- [XCUITest system requirements](https://github.com/appium/appium-xcuitest-driver/blob/master/docs/getting-started/system-requirements.md)
- [XCUITest device preparation](https://appium.github.io/appium-xcuitest-driver/latest/getting-started/device-setup/)
- [Apple Xcode system requirements](https://developer.apple.com/xcode/system-requirements)
- [Apple Developer Mode instructions](https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device)

## Transport-to-Review booking practice — 10 October 2026

The assistant restarted GoGoX on the connected iPhone and ran the approved booking
steps using the already registered account. The combined test passed: **1 passed
in 127.54 seconds**. It entered IFC Mall → Harbour City, selected 12 October 2026
at 14:00 HKT, four-hour rental and Van, then Basic $10, three passengers, Premium
Van, one cart, goods longer than 6 ft, pet-friendly and English-speaking drivers,
Cross-Harbour Tunnel (Hung Hom), and Move door-to-door. Dummy contact details were
saved on Review; Driver tip $20 and the required fee rows were asserted. It stopped
on Review without tapping Place order.

The route editor sometimes keeps the resolved address until Done. The earlier
restart attempt timed out waiting for automatic return. LocationPage now handles
both observed paths, waiting until the full address is resolved and search results
have disappeared before tapping Done when needed, then checking the saved home field.

An exploratory contact-save attempt left the phone field empty and displayed the
app's valid eight-digit Hong Kong number message. No defect is established by that
attempt. The implemented contact action reacquires unnamed fields after each edit,
checks all three values before Save, and verifies the saved contact summary. The
successful test used the dummy name Automation Test, phone 90000000 and blank optional
extension. These are draft inputs, not a verified reachable contact.

The custom checkboxes have no accessible selected-state values. Taps use each
observed semantic row's right-edge control; the review breakdown then verifies
that required services were retained. Cart +1 is checked on Order details and
appears as Borrow a trolley on Review. Move door-to-door adds Quote; actual pricing
is not replaced with an invented fixed total. Screenshots were also visually inspected.

Local evidence: reports/transport-booking.html, reports/transport-booking-console.log
and reports/transport-booking-final.png. Raw inspection images/XML stay in the ignored
reports/inspection directory; one exploratory capture includes a personal notification
banner and must not be shared. The final test screenshot has been checked separately.

To repeat, keep Appium running and the phone connected, unlocked and signed in.
Run the booking-practice command in README. It restarts the app and rebuilds the draft.
Do not run all checkpoint tests together: their individual starting screens differ.

Next: implement new-account registration, connect it with login and the verified
booking steps, then record the assignment run from before account creation. The
unused email remains reserved; this practice did not create a new account and does
not replace the assignment's registration checkpoint. No demo video was recorded.
