### README For Static Files ###

Static files are reserved separately by Flask since they undergo no changes, whereas HTML files are dynamic and fall under the templates folder.

If you are going to modify the web app or link to a style sheet, do so by first placing your .css file into the static/css/ directory, then referencing it in its corresponding HTML file with 

```<link rel="stylesheet" href="{{ url_for('static', filename='css/map_styles.css') }}">```,

replacing "map_styles" with the name of your cascading style sheets file.