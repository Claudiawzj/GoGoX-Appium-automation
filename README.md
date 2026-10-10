# GoGoX Appium assignment

Status: initial environment setup and a connection test verified on the iPhone.
After the user trusted the Personal Team certificate, the connection test passed
(1 passed in 22.96 seconds on 10 October 2026). The booking framework, full assignment
run and demo recording are not complete. See GETTING_STARTED.md for the beginner
walkthrough and actual verification records.

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

## Planned structure and safeguards

- pages: inspected locators and actions per screen (not implemented yet).
- tests: test logic and checkpoint assertions.
- utils: reusable helpers and configuration loading.
- config: capabilities and, later, external test data.
- reports: HTML reports, step logs and selected evidence.

The full flow must include registration/login, route, future pickup date/time,
4-hour hourly rental, Van, Basic $10, all requested extras, dummy contacts and $20 tip.
Record the installed app's contact-entry sequence discrepancy. Stop at review; never
place or confirm an order. No order-submission action will be implemented.

Route, registration prerequisites, exact test data and app locators remain unresolved.
Screen recording and submission packaging follow a verified complete automation run.
