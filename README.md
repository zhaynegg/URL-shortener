# URL-shortener
A simple program to shorten long URLs into compact, shareable links. 
Checkout the site here: https://www.gettinyurl.my/
## Tech Stack
The project is developed using:
- **Python/Django**
- HTML templates (for basic UI)

## Features
- **User authentication** is handled via Supabase, allowing users to register, log in, and manage their URLs securely.
- **URL shortening** is done using a combination of:
  - `xxhash` unique hash for each long URL
  - `base62` create human-readable urls
 

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/zhaynegg/URL-shortener.git
```
### 2. In the folder create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure the project
- You will need to create a project in supabase. In the project itself you will be able to enter the API keys folder. There are your anon and service role keys. Also the program uses profile table to store the usernames of users. You need to create table profile(id:uuid, username:varchar). RLS can be turned off. In other case run these sql commands:
```bash
create policy "Enable read access for all users"
on "public"."profile"
as PERMISSIVE
for SELECT
to authenticated
using (
  true
);
```
```bash
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profile (id, username)
  values (
    new.id, 
    new.raw_user_meta_data->>'username'
  );
  return new;
end;
$$ language plpgsql security definer;
```
- Do not forget to create your own Secret key and write down in .env file.
### 5. Apply database migrations
```bash
python3 manage.py migrate
```
### 6. Lastly, start the development server
```bash
python3 manage.py runserver
```
The server will be available at your localhost
