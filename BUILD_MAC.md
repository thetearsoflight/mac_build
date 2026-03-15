# macOS App Build (from Windows)

This project includes a GitHub Actions workflow that builds a native macOS `.app` using PyInstaller.

## What this solves

You can develop on Windows, then let GitHub-hosted macOS runners build the macOS app for you.

## Files

- `.github/workflows/build-macos-app.yml`: automation workflow
- Output artifact: `XiaohongshuLineHelper-macOS.zip`

## How to use

1. Push your code to GitHub.
2. Open GitHub repository page.
3. Go to **Actions**.
4. Run workflow: **Build macOS App**.
5. Wait for the run to finish.
6. Download artifact `XiaohongshuLineHelper-macOS`.
7. Unzip to get `XiaohongshuLineHelper.app`.

## Trigger options

- Manual run: `workflow_dispatch`
- Auto run on tags: push tag like `v1.0.0`

## Local macOS equivalent command

If you later use a real Mac, the workflow internally runs:

```bash
pyinstaller --noconfirm --clean --windowed --name XiaohongshuLineHelper add_blank_lines_gui.py
```

## Notes for distribution

- Unsigned app may show a security warning on first launch.
- For public distribution, add Apple code signing and notarization.
