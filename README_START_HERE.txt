WANDA PRESENTATION — WEBSITE UPDATE (WINRAR-COMPATIBLE ZIP)
===========================================================

PURPOSE
The homepage displays a styled "Presentation at WANDA" box immediately after
Muhammad Zikriya's profile details, BEFORE the "Research Area" heading.
It is NOT a site-wide announcement banner.

FILES INCLUDED
  _quarto.yml                   Updated website configuration and Research dropdown
  index.qmd                     Homepage with WANDA box (profile details preserved)
  wanda-card.css                Green/burgundy card style; keeps your styles.css
  research.qmd                  Existing research projects plus Conferences section
  conferences.qmd               Dedicated Conferences page
  slides/police-bcc/index.qmd   RevealJS conference presentation
  slides/police-bcc/UFPE_logo.png
  slides/police-bcc/GEDAI_logo.png

INSTALLATION
1. Back up your existing website folder or commit any unsaved changes.
2. Extract this ZIP with WinRAR or 7-Zip.
3. Copy the extracted contents into your existing website project folder
   (the same folder containing _quarto.yml). Allow merging of 'slides'.
   Do NOT delete or overwrite your other pages, styles.css, images or brand files.
4. Since index.qmd and research.qmd are replacements, if you have made further
   changes to them locally, merge those changes rather than overwrite.
5. Keep your existing images/my pic.jpg, styles.css, brand assets and other pages.
6. In your website project's terminal run: quarto render
7. Verify:
   docs/index.html
   docs/conferences.html
   docs/slides/police-bcc/index.html
8. Publish with:
   git add _quarto.yml index.qmd research.qmd conferences.qmd wanda-card.css slides docs
   git commit -m "Add WANDA presentation card and Conferences links"
   git push origin main

EXPECTED URLS AFTER GITHUB PAGES DEPLOYMENT
Home: https://mzikriya1995.github.io/
Conferences: https://mzikriya1995.github.io/conferences.html
Slides: https://mzikriya1995.github.io/slides/police-bcc/
Research: https://mzikriya1995.github.io/research.html

NOTE
This ZIP is a website update, not a complete replacement of your repository.
It intentionally does not include the existing profile photo, styles.css,
brand files or other existing pages. It works alongside them.
A .zip archive can be extracted directly by WinRAR; it is not a native .rar file.
