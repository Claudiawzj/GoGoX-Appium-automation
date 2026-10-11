# GoGoX Appium automation

Automates the Hong Kong iOS Transport flow using **Python/Pytest**, my preferred
framework for this assignment, with Appium/XCUITest and pytest-html reporting.
Page Object Model separates locators, page actions and test logic; tests use explicit
waits, checkpoint assertions and step logging.

**Stop boundary: end at Review with a HK$20 tip. Never place or confirm an order.**
ReviewPage has no order-submission action.

## Status and coverage

Verified on iPhone 13 Pro, iOS 26.3, GoGoX 7.111.0 (Hong Kong).
The latest recovery booking run passed in **128.66 seconds on 11 October 2026**.
Registration and its automatic sign-in were confirmed across a signup attempt and
recovery; an uninterrupted fresh-account run and demo recording remain pending.
Known promotion dismissal is implemented but has not yet been exercised on-device.

The booking test covers:

1. Existing-account login when signed out, or opt-in new-account registration.
2. IFC Mall → Harbour City; future pickup (Hong Kong date +2 days, 14:00),
   Hourly Rental – 4 hours, and Van.
3. Cargo Compensation: Basic $10; 3 passengers; Premium; Rent a Cart +1;
   goods longer than 6ft; pet-friendly and English-speaking drivers;
   Cross-Harbour Tunnel (Hung Hom); Move-to-door.
4. Review Order, saved dummy contact details, HK$20 tip and summary assertions.

In this app version, contact entry occurs **after Review Order**. Registration mode
verifies automatic sign-in and continues to booking; it does not perform a separate
password login. Route, pickup plan and contact data are externally configured.

## Prerequisites

- Mac with Xcode and an Apple account configured for WebDriverAgent signing.
- Connected, unlocked and trusted iPhone with Developer Mode and Enable UI Automation
  enabled; trust the signed developer app under Settings → General → VPN & Device Management.
- GoGoX installed in the Hong Kong market with the English UI.
- Node.js/npm and Python. Tested with Node 24.14.1, Python 3.14.3 and Xcode 16.4.

Pinned tooling: Appium **3.8.0**, XCUITest **12.16.0**; stable versions were checked
against the official npm registry on 10 October 2026. Python dependencies are locked
in [requirements.txt](requirements.txt).

## Setup

From the cloned repository directory:

```sh
npm ci
npm run driver:install
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm run doctor
```

Create `config/device.local.yaml` from [device.example.yaml](config/device.example.yaml)
and `config/data.local.yaml` from [data.example.yaml](config/data.example.yaml).
Fill the device ID, app bundle ID, signing team and unique WDA bundle ID locally.
Set registered credentials under `login`, unused credentials under `registration`
only for a fresh-account attempt, and dummy details under `booking.contact`.
Keep the two account sections separate. Local configuration is ignored by Git.

## Run

Start Appium in one terminal; reuse an existing server on port 4723:

```sh
npm start
```

Run tests in a second terminal from the repository directory, with the phone connected
and unlocked. First verify the connection (launches GoGoX without tapping controls):

```sh
.venv/bin/python -m pytest tests/test_connection.py --device --html=reports/connection.html --self-contained-html
```

**Repeatable booking practice:** supports signed-in or signed-out starts, using
`login` credentials when needed. Restarts GoGoX, rebuilds the draft and stops at Review.

```sh
.venv/bin/python -m pytest tests/test_transport_booking.py --device --html=reports/transport-booking.html --self-contained-html
```

**Fresh-account demo:** use a different unused registration email, manually sign out
and return to English Transport. Start screen recording **before** running:

```sh
.venv/bin/python -m pytest tests/test_transport_booking.py --device --register --html=reports/full-flow.html --self-contained-html
```

Stop recording when the test finishes. Signup and passwords are submitted once, with
no automatic retries. If account creation occurs before a later failure, that email
is registered; check account state before retrying. A new fresh-account recording
needs another unused email. `--register` requires `--device` and this single test.

Offline checks (no phone required):

```sh
.venv/bin/python -m pytest tests/test_pickup_plan.py tests/test_registration_settings.py
```

Device tests without `--device` are skipped. Run individual checkpoint tests only
from their documented starting screens; they are not a state-independent suite.

## Structure and reports

| Directory | Contents |
| --- | --- |
| `pages/` | Page actions and separate `locators/` modules |
| `tests/` | Booking flow, device checkpoints and offline tests |
| `utils/` | Configuration, pickup planning and screen inspection helpers |
| `config/` | Shareable examples and ignored local capabilities/test data |
| `reports/` | Generated HTML reports, logs and screenshots (ignored) |

The booking test saves `reports/transport-booking-final.png`. Use the project's
warning-level Appium logging; review raw evidence for private data before sharing.
Device/signing values, credentials, installed tools and raw reports are excluded
from Git. The manual report and original evidence are delivered separately.

See [GETTING_STARTED.md](GETTING_STARTED.md) for beginner guidance, checkpoint
results and troubleshooting history.
