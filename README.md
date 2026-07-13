# Django + Git Learning Log — Quick Reference

## 🖥️ Command Cheatsheet

```bash
# One-time machine setup
git config --global user.name "YourName"
git config --global user.email "your@email.com"

# Per-project setup
mkdir myProject
cd myProject
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac / Linux
pip install django
django-admin startproject myProject .
python manage.py runserver
python manage.py startapp myapp

# File creation (Windows terminals)
touch file.py                   # Linux / Mac / Git Bash
New-Item file.py                # PowerShell
type nul > file.py              # Command Prompt (cmd)

# Git initialisation
git init
New-Item .gitignore             # Windows
touch .gitignore                # Mac / Linux
git add .
git commit -m "Initial project setup"

# GitHub connection
git remote add origin https://github.com/YourUsername/YourRepo.git
git push -u origin main

# Django database & admin setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Ongoing development workflow (repeat)
git status
git add .
git commit -m "Describe what you did"
git push
git log
git pull
```

---

## 📚 Concepts Learned (1-2 liners)

### Git & GitHub
- **`git init`** only creates a local repo — it has zero awareness of GitHub or "origin" until you explicitly link it.
- **`git remote add origin <url>`** just saves the GitHub address as a contact named "origin" — it doesn't push anything yet.
- **`git push -u origin main`** is the first push AND sets up tracking, so future pushes can just be `git push`. Needed once per new repo/project.
- **`cls`** only clears the terminal *display*, not command history — press **Up arrow** or use `Get-History` (PowerShell) / **F7** (cmd) to recall old commands.
- Terminal **output/results** (like a commit message shown after running it) are lost once cleared — but `git log` retrieves that same commit message permanently from Git's own storage, no terminal history needed.

### Django Structure & "Registration" Pattern
- **`INSTALLED_APPS`** is Django's official registry — an app's folder can physically exist but Django won't load its models/templates/admin unless it's listed here.
- **Creating a model in `models.py`** doesn't make it appear in the admin panel — you must explicitly register it in `admin.py`.
- **Core transferable rule:** *"Existence ≠ Awareness"* — creating something doesn't automatically plug it into the parent system; it must be explicitly registered (seen in `INSTALLED_APPS`, `admin.py`, and beyond — imports, routes, plugins, DI containers, etc. all follow this same pattern).

### Django Templates
- **`{% if data.x %}`** checks truthy/falsy — Django templates fail *silently* (no crash) if a variable is missing or empty, unlike raw Python.
- **`{{ variable }}`** does NOT check truthy/falsy — it just prints the variable's text form. An empty dict `{}` is "falsy" for `{% if %}` but still prints as literal text `{}` inside `{{ }}`.
- **Core transferable rule:** *"Checking if something is meaningful" (`{% if %}`) and "showing what something literally is" (`{{ }}`) are two separate jobs* — same split exists in JS (`{value && <Comp/>}` vs `{value}`), SQL (`NULL` vs `''` vs `0`), and JSON APIs.

### Forms & `action` Attribute
- **`action=""`** means "submit back to whatever URL the browser is currently on" — safest default for same-page forms.
- **`action="filename.html"`** is WRONG — the browser only understands **URLs**, never template/file names. Template files and URL routes are two independent systems connected only via `urls.py`.
- **`action="/"`** correctly submits to the root URL if `urls.py` maps `""` to your view.

### CSRF & Security
- **CSRF (Cross-Site Request Forgery)** = a malicious site tricks your browser into sending a forged request to another site using your saved login cookies.
- **`{% csrf_token %}`** embeds a secret token Django checks on submission — an attacker's forged request can't replicate it.
- CSRF protection applies only to **"unsafe" methods** (POST/PUT/PATCH/DELETE) — GET is assumed safe/read-only under REST convention, which is *why* GET is exempt.

### REST API Principles
- **REST** = an architectural style (a set of conventions), not a framework or technology.
- **6 constraints:** Client-Server separation, Statelessness, Cacheability, Uniform Interface (resource-based URLs, HTTP verbs matching actions, self-descriptive messages, HATEOAS), Layered System, Code on Demand (optional, rarely used).
- **"RESTful" code indicators:** noun-based URLs (`/users/5` not `/getUser`), correct HTTP verbs, no server-side session dependency for core logic, proper status codes (200/201/404/400).
- **Alternatives to REST:** GraphQL (client picks exact fields), gRPC (fast, internal microservices), tRPC (TypeScript-native), SOAP (legacy/enterprise).

### Browser Behavior (Not Django!)
- **"Confirm Form Resubmission" dialog** is a **Chrome-native** popup, not Django or JS-coded — triggered when refreshing/navigating back to a page that was originally loaded via POST.
- **Fix (industry standard): PRG pattern (Post → Redirect → Get)** — after processing POST, redirect to a GET URL instead of returning HTML directly, so refreshing never resubmits.

### Python: APIs, JSON, and Requests
- **`urllib.request.urlopen(url)`** dials/connects to a URL; **`.read()`** is a separate step that reads the raw response bytes.
- **`json.loads()`** parses a string/bytes already in memory; **`json.load()`** parses directly from a file-like object — the "s" suffix distinguishes them.
- **`requests.get(url)`** merges "dial + read" into one call; `.json()` remains a separate (but cleaner) parsing step — same underlying work, less boilerplate.
- **Universal 3-step API pattern (any language):** (1) build the request → (2) send & get raw response → (3) parse raw response into usable data.
- **OpenWeatherMap Geocoding API:** country/state codes in `q=` are optional refinements, not required — city name alone works fine.

---

## 🐛 Errors Encountered & Fixes

| Error / Confusion | Root Cause | Fix |
|---|---|---|
| New app not recognized by Django | App not added to `INSTALLED_APPS` | Add `'appname'` to `INSTALLED_APPS` list in `settings.py` |
| Model not visible in admin panel | Model not registered | Register model in `admin.py` |
| `{{ city }}` printed `{}` instead of nothing | Confused truthy-check (`{% if %}`) with raw printing (`{{ }}`) | Understand `{{ }}` always prints a variable's text form, even if "empty" |
| Form submission going to wrong/broken URL | Used `action="index.html"` (a file name) instead of a URL | Use `action=""` (same page) or a valid URL path like `/` |
| "Confirm Form Resubmission" popup on refresh | Browser re-warns about resubmitting POST data | Use PRG pattern — redirect after POST instead of rendering directly |
| Thought country code was mandatory in Geocoding API | Misread `{state code},{country code}` in docs as required fields | They're optional; city name alone (`q=London`) works |
| Coordinates showing squished together (e.g., `-0.187.4`) | Empty string `''` used as separator when concatenating `lon` + `lat` | Use a real separator like `', '` between the two values |

---

*Generated as a personal learning log — designed for quick review, not exhaustive reference.*
