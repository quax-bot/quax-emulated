# quax-emulated

Runs Maestro flows on [QuaX](https://github.com/Teskann/QuaX) in an Android
emulator, against the mock of X in its `tool/mock_x/`, and records a video of
each flow.

The `emulator` workflow builds QuaX at any ref, then runs
`tool/mock_x/emulator_qa.dart`. The `emulator-output` artefact holds the
videos, Maestro's screenshots and logs, the logcat and the mock's log.

| Input        | Default        |                                            |
|--------------|----------------|--------------------------------------------|
| `repository` | `Teskann/QuaX` | Repository to test, e.g. a fork            |
| `ref`        | `master`       | Branch, tag or commit                      |
| `flows`      | `.maestro`     | Folder or `.yaml` flow, in that repository |
| `flow`       |                | YAML of one flow, run instead of `flows`   |

The ref must have `tool/mock_x/emulator_qa.dart` and a profile manifest that
allows plain HTTP.

Run the flows of a fork's branch:

```bash
gh workflow run emulator.yml -R quax-bot/quax-emulated -f repository=someone/QuaX -f ref=new-flow
```

Reproduce a bug with a flow of your own. GitHub's form takes one line, the API
takes the whole file:

```bash
gh workflow run emulator.yml -R quax-bot/quax-emulated -f ref=master -F flow=@repro.yaml
```

For a before/after video, run the same `flow` on the base branch and on the fix.

## Writing flows

- Flows run in alphabetical order on the same installation, cleared only
  before the first one: each must work alone as well as after the others.
- Start with `launchApp`, then `openLink` with `autoVerify: true`: the app is
  past its onboarding and opens x.com links.
- Maestro finds elements by accessibility label. To subscribe, tap
  `Show menu`, then `Subscribe`. Saving a post and downloading a media have no
  label yet.
- The mock only answers requests recorded in QuaX's `test/fixtures/`.

The APK (per repository and commit), Maestro and the booted emulator are cached,
even when a flow fails.
