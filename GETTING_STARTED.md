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
7. Verify the full run, generate an HTML report, and record the demo.
8. Complete the README, assumptions/challenges/improvements note, and ZIP or repository delivery.

The framework will use `pages`, `tests`, `utils`, `config`, and `reports`. No booking test has been implemented yet.

## Details to resolve before the full run

- Current device OS, GoGoX version and Hong Kong market.
- New-account registration data and access to verification, if needed; distinguish any human verification step from automated steps.
- Final From/To locations. IFC Mall → Harbour City is only a proposal, not the retained manual route.
- Exact Tunnel Preference choice. The manual screenshots support Cross-Harbour Tunnel (Hung Hom).
- Dummy contact details and a pickup date/time that remains future at execution.
- Contact entry appears after Review Order in the manually tested version; record and implement the installed app's actual sequence without silently omitting contact entry.

## Official references

- [Appium requirements](https://appium.io/docs/en/latest/quickstart/requirements/)
- [XCUITest system requirements](https://github.com/appium/appium-xcuitest-driver/blob/master/docs/getting-started/system-requirements.md)
- [XCUITest device preparation](https://appium.github.io/appium-xcuitest-driver/latest/getting-started/device-setup/)
- [Apple Xcode system requirements](https://developer.apple.com/xcode/system-requirements)
- [Apple Developer Mode instructions](https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device)
