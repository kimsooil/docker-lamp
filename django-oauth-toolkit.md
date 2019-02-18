# Django OAuth Toolkit

This toolkit is used for authentication purposes.


## Getting Started

Documentation loosely based on https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-4-get-your-token-and-use-your-api. However, the setup part is already done, so, documenation starts on https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-3-register-an-application

### Creating an app

Being logged in as an admin, got to */o/applications/* and create an application.

#### Form data

- Name: Choose whichever name you want.
- Client id: [Already filled in - ignore]
- Client secret: [Already filled in - ignore]
- Client type: Confidential
- Authorization grant type: Resource owner password-based
- Redirect uris: For our purpose, we will not use this one, however, one is required, so, put in *http://localhost:8000/*

### Getting a token

Once the app is setup, you can use *simple* token fetching to get a token for a user.

#### Example for postman.

##### Request

POST: */o/token/*

```
{
    'grant_type': 'password',
    'username': '<username>',
    'password': '<password>',
    'client_id': '<Your application client id>',
    'client_secret': '<Your application client secret>'
}
```

##### Respose

```
{
    "access_token": "SuEUwISaQwRWCzdT3Gw9BQ2TrB8P7C",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "5tkPTsNi0gxvb6zoD09ZzFLUnqNoxC"
}
```

### Using a token

Now that you have a token, it is time to use it.

#### Example using postman

##### Request 

GET: */users/api/me/*

###### Headers

```
Authorization: Bearer SuEUwISaQwRWCzdT3Gw9BQ2TrB8P7C
```

##### Response

```
{
    "name": "Admin",
    "email": "admin@example.com",
    "username": "admin"
}
```

### Security notes

For the most part, the */o/applications/* part seems to be 