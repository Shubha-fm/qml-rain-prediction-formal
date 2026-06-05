# Upload and Deploy Guide

## Upload to GitHub

```bash
git init
git add .
git commit -m "Initial commit: QML rain prediction with formal verification"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qml-rain-prediction-formal.git
git push -u origin main
```

## Deploy Website

1. Open the repository on GitHub.
2. Go to Settings.
3. Go to Pages.
4. Select Deploy from a branch.
5. Select branch `main` and folder `/web`.
6. Save.

Your website link will be:

```text
https://YOUR_USERNAME.github.io/qml-rain-prediction-formal/
```
