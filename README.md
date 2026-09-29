# Django portfolio

A personal portfolio site: profile, projects, skills, work history, and a contact
form that saves messages to the database and emails you a copy. Everything is
edited through the Django admin — no code changes needed to update your content.

## Run it

```bash
# 1. create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. settings
cp .env.example .env             # Windows: copy .env.example .env

# 4. database
python manage.py makemigrations portfolio
python manage.py migrate

# 5. sample content (optional, but the site looks empty without it)
python manage.py seed_demo

# 6. an admin login
python manage.py createsuperuser

# 7. go
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the site and http://127.0.0.1:8000/admin/ to edit it.

To start from a blank site instead, skip step 5 and fill in Profile yourself.
To wipe the samples later: `python manage.py seed_demo --reset` then delete the rows you don't want.

## What's where

| Path | What it does |
| --- | --- |
| `config/settings.py` | All settings, read from `.env` where it matters |
| `config/urls.py` | Routes `/admin/` and hands everything else to the app |
| `portfolio/models.py` | Profile, Skill, Project, Experience, Education, ContactMessage |
| `portfolio/views.py` | Home, project list, project detail, contact |
| `portfolio/admin.py` | How each model looks in the admin |
| `portfolio/forms.py` | Contact form, with a hidden honeypot field for bots |
| `portfolio/context_processors.py` | Puts `profile` into every template |
| `templates/` | Page templates; `base.html` holds the shared layout |
| `static/css/style.css` | The whole design, in one file |

## Pages

| URL | Template |
| --- | --- |
| `/` | `templates/portfolio/home.html` |
| `/projects/` | `templates/portfolio/project_list.html` |
| `/projects/<slug>/` | `templates/portfolio/project_detail.html` |
| `/contact/` | `templates/portfolio/contact.html` |

## Editing your content

Log into `/admin/` and start with **Profile** — name, headline, bio, email, photo,
résumé PDF, and social links. The sidebar and footer read from it on every page.

Then add **Projects** (tick "is featured" for the ones you want on the home page),
**Skills** (the number 0–100 draws the bar), and **Experience** (leave the end date
empty for your current job; each line of the description becomes a bullet).

Messages from the contact form land under **Messages**. They can't be edited, only
read and marked as read.

## Changing the look

The palette and fonts are CSS variables at the top of `static/css/style.css`:

```css
--paper: #edeaf3;   /* page background */
--ink:   #241e35;   /* text */
--pine:  #2c6a56;   /* buttons, links, skill bars */
--wheat: #d6a140;   /* the "current job" marker */
```

Change those four and the whole site follows. Fonts are loaded in `templates/base.html`.
A dark palette is already defined and switches with the visitor's system setting.

## Deploying

1. Set `DJANGO_DEBUG=False` and a real `DJANGO_SECRET_KEY` in `.env`.
2. Put your domain in `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.
3. `python manage.py collectstatic`
4. Run with `gunicorn config.wsgi` behind nginx, or deploy to Railway, Render,
   Fly.io, or PythonAnywhere — all of them handle this layout as-is.

Uploaded files in `media/` are not served by Django in production. On a small VPS,
point nginx at the folder; on a platform host, use S3 or a similar bucket via
`django-storages`.

SQLite is fine for a portfolio. If you'd rather use Postgres, install `psycopg[binary]`
and swap the `DATABASES` block in `config/settings.py`.
