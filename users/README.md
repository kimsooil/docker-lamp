## General

### Django Rest Framework (DRF) API Authentication.

In order to use DRF authentication, use the following path, passing in the *username/password*.

**POST** */users/api/authenticate/*

**Response**

```json
{
    "token": "83f1c9283e0f97bf56b68fb80d7b9b3c986a8132",
    "user_id": 1,
    "email": "email@example.com"
}
```