# Little Lemon API

Django REST API project for Little Lemon.

It contains menu items, cart, orders and manager/delivery crew endpoints.
Authentication uses Django tokens with Djoser.

## run

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API routes start with `/api/` and authentication routes are under `/auth/`.

The project does not include a populated database, fixtures, or automatic sample data. After running the migrations, create users through the authentication API and add menu items through the API or Django admin.

For protected routes send the token in the Authorization header:

```
Authorization: Token your_token
```
