# START HERE — Clean RNN/LSTM RevealJS publishing fix

**What this package changes:** It adds a separate source project named `_RNN_LSTM_SOURCE` and a `BUILD_WEBSITE_AND_SLIDES.bat` script. The slideshow source is not rendered by the HTML website. The script renders the website first, renders the slideshow separately as RevealJS, and copies the rendered slideshow to `docs/slides/rnn-lstm/`.

## IMPORTANT — First delete ONLY old RNN/LSTM folders

In your existing website folder (`D:\My persnoal data\website\My Websie\`):

1. **KEEP** `slides/police-bcc/` (WANDA). Keep all website pages, CSS and other files.
2. Delete `slides/rnn-lstm/` if present. This is the old RNN/LSTM source.
3. Delete `docs/slides/rnn-lstm/` if present. This is the old published RNN/LSTM page.
4. Delete the old `_RNN_LSTM_SOURCE/` folder **only if you installed an earlier test version**.
5. If you previously extracted old `RNN_LSTM_...` complete project folders into your website root, move those folders OUTSIDE the website. Keep any backups elsewhere.

Do not delete `slides/` as a whole, the WANDA folder, `docs/` as a whole, or your website's other pages.

## Copy and paste

Extract this ZIP into a temporary folder (not inside your website). Open `COPY_CONTENTS_INTO_YOUR_WEBSITE`. Copy **everything inside that folder**, not the folder itself, into your existing website folder. Replace `_quarto.yml` after backing up your old version. Keep the rest of your website files intact.

After copying, the website folder must contain:

- `_quarto.yml` (this package)
- `BUILD_WEBSITE_AND_SLIDES.bat` (this package)
- `lectures.qmd` (this package)
- `_RNN_LSTM_SOURCE/index.qmd` (editable 99-slide Quarto lecture)
- `_RNN_LSTM_SOURCE/_quarto.yml` (separate Quarto project)
- `_RNN_LSTM_SOURCE/assets/` and `_RNN_LSTM_SOURCE/styles.scss`
- `slides/police-bcc/index.qmd` (your existing WANDA presentation)
- `slides/police-bcc/UFPE_logo.png` and `GEDAI_logo.png` (your existing logos)
- Your original `index.qmd`, `education.qmd`, etc.

## One Windows command — REQUIRED

Use the **Terminal** in RStudio, opened in the website main folder, and run:

```
.\BUILD_WEBSITE_AND_SLIDES.bat
```

**Do not** use RStudio's `Render` button on `_RNN_LSTM_SOURCE/index.qmd` from inside the website. Do not use `quarto render` by itself to publish both: you MUST run the BAT each time because it builds two Quarto projects, then copies the correct presentation into docs.

If the BAT says SUCCESS, open `docs/slides/rnn-lstm/index.html` in Windows. You should see slides with keyboard navigation, not the website navbar or "On this page" sidebar. Then push all changes:

```
git add -A
git commit -m "Publish RNN LSTM RevealJS lecture"
git push origin main
```

## URLs after GitHub Pages deploys

- `https://mzikriya1995.github.io/lectures.html`
- `https://mzikriya1995.github.io/slides/rnn-lstm/index.html`
- `https://mzikriya1995.github.io/slides/police-bcc/index.html`

## Why this avoids the error

Your website `format: html` applies to normal site pages. The lecture is in a separate Quarto project with an independent `_quarto.yml`. Its RevealJS output is copied into the published `docs/` directory **only after** the website render has completed. The original WANDA folder is never changed or deleted by the script.

## If the BAT shows an error

Copy the first `ERROR:` line and the few lines above it. The script intentionally stops before publishing if it cannot find WANDA, logos, Quarto, or the expected RevealJS HTML.

**Important:** Native Quarto is not installed in the packaging environment, so the BAT could not be executed here. Its inputs, YAML parsing and ZIP file structure were validated. If your local RStudio render still fails, the exact BAT error will tell us where.
