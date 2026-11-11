FIX FOR THE QUARTO WARNING: Unable to resolve link target: lectures.qmd

Problem: lectures.qmd was inside the extracted RNN_LSTM_Quarto_GitHub_Pages/ folder, not next to your website's index.qmd and _quarto.yml. Quarto also attempted to render the archive's documentation as website pages.

1. MOVE the old extracted RNN_LSTM_Quarto_GitHub_Pages/ folder OUT of your existing website repository folder. Do not delete it if you want to retain the editable teaching source files.
2. Open the existing mzikriya1995.github.io project folder (containing index.qmd, about.qmd, _quarto.yml).
3. Extract THIS ZIP DIRECTLY INTO THAT folder: its lectures.qmd must be adjacent to index.qmd; and slides/rnn-lstm/ must contain index.html, viewer.js, styles.css and assets/.
4. Under project: in your EXISTING _quarto.yml keep type: website and output-dir: docs, and ADD:
     resources:
       - "slides/rnn-lstm/**"
   Under website: navbar: left:, ADD:
     - text: Teaching
       menu:
         - text: Lecture Library
           href: lectures.qmd
         - text: "RNNs and LSTMs: Deep Learning for Sequential Data"
           href: slides/rnn-lstm/index.html
           target: _blank
   Do not add a second project: or navbar: and do not overwrite your existing YAML.
5. In the website root run: quarto render
6. Verify docs/lectures.html and docs/slides/rnn-lstm/index.html exist.
7. Publish: git add -A; git commit -m "Add RNN LSTM lecture"; git push origin main

If quarto preview about.qmd was still running, stop it (Ctrl+C) and restart after fixing the files.
