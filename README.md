# Description
This is a python 🐍 flask 🌶️ kata 🥋 project to practice, learning and improve knowledge. This is an application for songs 🎼🎶

# Made with
[![Python](https://img.shields.io/badge/python-2b5b84?style=for-the-badge&logo=python&logoColor=white&labelColor=000000)]()
[![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white&labelColor=000000)]()

## Postman 👩🏻‍🚀 pre-script

* If you want to try the application with postman you can add script for authenticate an specific user and use the token for all request

```js
const SONGS_API_BASE_URL = pm.environment.get('SONGS_API_BASE_URL');
const username = pm.environment.get('DEFAULT_USERNAME');
const password = pm.environment.get('DEFAULT_PASSWORD');

const options = {
    url: `${SONGS_API_BASE_URL}/login`,
    method: 'POST',
    header: {
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            "username": username,
            "password": password
        })
    }
}

pm.sendRequest(options, function (error, response) {
    var jsonData = response.json();
    if (error) {
        console.log(error);
    }
    else {
        pm.environment.set('SONGS_API_TOKEN', jsonData.accessToken)
    }
})
```