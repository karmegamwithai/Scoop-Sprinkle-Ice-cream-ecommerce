# 🍦 Scoop & Sprinkle — Ice Cream E-commerce (Django + Supabase)

A full ice-cream shop web app where **Supabase (hosted Postgres) is the database**.
One Supabase project is used, with a separate **table** for every data type:
`users`, `products`, `orders`.

Theme: white & pink 🎀

## 1. Project structure

See the folder tree — Django apps are split by feature:

- `apps/home` — landing page
- `apps/accounts` — customer register/login/logout/profile (stored in the `users` table)
- `apps/products` — product catalog (stored in the `products` table)
- `apps/cart` — session-based shopping cart (no table needed, lives in the browser session)
- `apps/orders` — checkout & order history (stored in the `orders` table)
- `apps/dashboard` — admin area to add/edit/delete products, view users & orders
- `services/supabase_client.py` — the single place that talks to Supabase (via `supabase-py`)

## 2. Supabase setup

1. Create a free project at [supabase.com](https://supabase.com).
2. Open the **SQL Editor** in your Supabase project and run:

```sql
create table users (
  id bigint generated always as identity primary key,
  username text unique not null,
  email text unique not null,
  password text not null,          -- Django-hashed password, never plain text
  phone text,
  address text,
  created_at timestamptz default now()
);

create table products (
  id bigint generated always as identity primary key,
  name text not null,
  description text,
  price numeric(10,2) not null,
  flavor text,
  category text,
  stock integer default 0,
  image_url text,
  created_at timestamptz default now()
);

create table orders (
  id bigint generated always as identity primary key,
  user_id bigint references users(id),
  username text,
  items jsonb not null default '[]',   -- line items: [{product_id, name, price, quantity}, ...]
  total_amount numeric(10,2) not null,
  address text,
  phone text,
  status text default 'Pending',
  created_at timestamptz default now()
);
```

3. Go to **Project Settings → API** and copy:
   - **Project URL** → `.env` as `SUPABASE_URL`
   - **service_role key** (secret, server-side only) → `.env` as `SUPABASE_KEY`

   > ⚠️ Use the **service_role** key, not the `anon` key, since Django (not the
   > browser) is what talks to Supabase here. Never expose the service_role
   > key to a frontend/browser context.

4. This project **disables Row Level Security (RLS) enforcement from Django's
   side** by using the service_role key, which bypasses RLS. If you'd rather
   turn RLS on for extra safety, keep it enabled — the service_role key still
   bypasses it by design, so no policies are required for the app to work.

## 3. Install & run

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Visit:
- Store front: http://127.0.0.1:8000/
- Admin dashboard: http://127.0.0.1:8000/dashboard/login/
  (credentials come from `.env` → `ADMIN_USERNAME` / `ADMIN_PASSWORD`)

## 4. Notes

- This project does **not** use Django's ORM for the shop data — it doesn't
  define any Django `models.py`. `services/supabase_client.py` reads & writes
  rows directly to Supabase via REST (through `supabase-py`).
- Django's `db.sqlite3` (created by `manage.py migrate`) is only used internally
  for sessions if you keep the default session engine; you can switch to
  cookie/cache-based sessions if you want zero local SQL database at all.
- Passwords are hashed with Django's `make_password` / `check_password`
  before being written to the `users` table — Supabase never sees plaintext
  passwords.
- Order line items are stored as native `jsonb` in the `orders.items` column,
  so `supabase-py` returns them as ready-to-use Python lists/dicts — no manual
  JSON parsing needed.
