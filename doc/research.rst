#################
discodoc research
#################


*********
Discourse
*********

Hard copy rendering
===================
- https://meta.discourse.org/t/format-for-hard-copy-or-pdf-printing/13033
- https://meta.discourse.org/t/pocket-offline-reader-support/17500
- https://meta.discourse.org/t/printer-friendly-css/30899
- https://meta.discourse.org/t/add-a-get-option-to-enable-noscript-view-of-a-page/33823
- https://meta.discourse.org/t/print-long-topic-to-pdf-redux-again/44639
- https://meta.discourse.org/t/making-doi-ready-pdfs-from-discourse/92858
- https://meta.discourse.org/t/converting-links-from-raw-markdown-to-html/102422
- https://meta.discourse.org/t/creating-an-offline-topic-reading-archive/103651

Pagination and more
===================
- https://meta.discourse.org/t/paginating-api-search-results/49066
- https://meta.discourse.org/t/api-to-fetch-topic-by-page/63342/2
- https://meta.discourse.org/t/struggling-with-pagination-within-search-query-json/59558
- https://blog.codinghorror.com/the-end-of-pagination/
- Why not to use infinite scroll on your website
  https://news.ycombinator.com/item?id=7559737

Discourse API
=============
- https://meta.discourse.org/t/discourse-api-documentation/22706
- https://meta.discourse.org/t/api-can-i-authenticate-without-putting-the-key-in-the-url/29425
- https://meta.discourse.org/t/global-rate-limits-and-throttling-in-discourse/78612
- https://meta.discourse.org/t/changing-removing-api-rate-limit-with-category-creation/78611



******
pandoc
******

Misc notes.

::

    # By default, pandoc produces a document fragment. To produce a
    # standalone  document (e.g.  a valid HTML file including <head>
    # and <body>), use the --standalone flag.


    --pdf-engine wkhtmltopdf

    --pdf-engine=PROGRAM

        Use the specified engine when producing PDF output. Valid values are pdflatex, lualatex, xelatex, latexmk, tectonic, wkhtmltopdf, weasyprint, prince, context, and pdfroff. The default is pdflatex. If the engine is not in your PATH, the full path of the engine may be specified here.

    https://pandoc.org/MANUAL.html#option--pdf-engine

    To create a pdf using pandoc, use -t latex|beamer|context|ms|html5
    and specify an output file with .pdf extension (-o filename.pdf).

    pandoc --list-output-formats
