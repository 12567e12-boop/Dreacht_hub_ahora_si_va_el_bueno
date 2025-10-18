# Dreacht Hub - Project TODO

## Project Description
This project is called "Dreacht Hub" and is planned to be the platform for employees of the Dreacht company. For now, it will only include an "app_PDF_maker" application.

The app_PDF_maker will have a main interface that leads to 2 different views:

1. **Recursos (Resources)**: Here, users will have access to a list of downloadable images and PDFs.

2. **Requisiciones (Requisitions)**: This will open an interactive fillable PDF that allows filling fields on PC or phone. The PDF must be fully visible without scroll, zoom, or size modifications (obviously scaling depending on the screen). For now, only the PDF visualization is needed, but consider that on top of the PDF template there should be a form with fields positioned using coordinates or another method (again, not sure if possible and if there are conflicts on other devices), and finally create a new PDF by merging the template and the data in the necessary positions for download.

## Chosen Technology Stack
Chosen: Django backend with Bootstrap 5 for styling and vanilla HTML/CSS/JS frontend using Django Templates.

For Requisitions View:
- Use PDF.js to render the PDF in a canvas for viewing without zoom/scroll.
- Overlay form elements using absolute positioning based on coordinates.
- Use jsPDF to generate the filled PDF by drawing text on the template.
- Backend: Django for serving templates, handling file uploads/downloads, and any server-side logic.

## Project Structure
```
.
├── db.sqlite3
├── manage.py
├── TODO.md
├── app_PDF_maker/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── static/
│   │   ├── css_static/
│   │   ├── js_static/
│   │   └── media/
│   └── templates/
│       └── app_PDF_maker/
│           ├── home.html
│           ├── recursos.html
│           └── requisiciones.html
├── dreacht_hub/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── dreacht_venv/
    ├── pyvenv.cfg
    ├── Include/
    ├── Lib/
    ├── Scripts/
    └── Lib/site-packages/
```

## Main App and Views
- The main Django app is `app_PDF_maker`.
- Views:
  - `home`: Main interface with navigation to Recursos and Requisiciones.
  - `recursos`: Displays a list of downloadable images and PDFs (pending implementation).
  - `requisiciones`: Displays a PDF viewer with an overlay form for filling fields.

## URL Routing
- Root URLs are configured in `dreacht_hub/urls.py` which includes `app_PDF_maker.urls`.
- `app_PDF_maker/urls.py` defines routes for home, recursos, and requisiciones views.

## Templates
- `base.html`: Base template with navbar, container, and footer.
- `home.html`: Main navigation page extending base.html.
- `recursos.html`: Placeholder page for downloadable resources extending base.html.
- `requisiciones.html`: PDF viewer using PDF.js with an overlay div for form fields extending base.html.
- `gafete.html`: Similar to requisiciones.html for gafete view extending base.html.

## Dependencies
- Django
- PDF.js (for PDF rendering)
- jsPDF (for PDF generation)

## Current State and Next Steps
- Basic project structure and routing are set up.
- Views render the corresponding templates.
- PDF viewer implemented with PDF.js in requisiciones.html and gafete.html.
- Created base.html template with navbar, container, and footer; all HTML templates now extend base.html.
- Recursos view content pending implementation.
- Next steps include implementing form overlays, PDF generation, and responsiveness.

## Navbar Color Change Task
- [x] Change navbar class in base.html from 'navbar-light bg-light' to 'navbar-dark bg-dark' for black background with white text.

## Gafetes Container Color Task
- [x] Change the form-container in gafetes.html to bg-dark text-white to match the navbar color.

## Center Form in Card Container Task
- [ ] Center the form vertically and horizontally in the card container in gafetes.html using flexbox.
