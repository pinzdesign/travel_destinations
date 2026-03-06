# Travel Destinations SPA

A small Single Page Application (SPA) for viewing and managing travel destinations.
Users can only view destinations, while registered users can log in and add new destinations to the list.

---

## Features

* View travel destinations
* User registration and login
* Add new destinations (registered users only)
* Protected actions based on authentication
* Client-side navigation without full page reloads
* Token-based authentication using local storage
* All CRUD operations implemented

---

## Tech Stack

* Python/Flask/mySQL/Docker
* TypeScript
* HTML/CSS

---

## Installation

clone the repository
```
github clone *repository url*
```

---

## How It Works

I created a simple SPA navigation system. Instead of reloading the page, the client fetches HTML partials and injects them into the main content area.
I am not using mixhtml, as i wanted to develop my own SPA architecture, and play around with fetch etc.
I am sending raw json (instead of form data), and receiving json as response from backend as well.
Authentication is handled with JWT tokens. When a user logs in, the server returns a token that is stored in the browser's local storage. This token is then included in future requests to access protected routes.
I use backend validation with constraints for allowed character amount, as well as checking value for being empty.
I have created a scipt which shows how long ago a destination was added (by using a unix timestamp)
I use mysql JOIN to get a user name, based on relation between destination author id, and user id.

Pages restricted depending on login state:

* Guests cannot add new destinations
* Logged-in users cannot access the signup page

---

## Future Improvements (?)

* Improved UI styling
* Better error handling
* Frontend Form validation
* Use of external api (i can populate a selector with entries from https://restcountries.com/ api, instead of having manually enter country)
* Rating for destinations, right now destinations table have a cell called rating, but it's unused.
* Displaying the amount of destinations created by a certain user (in profile page) by using COUNT in sql query
* Fix saving date for destinations (i can just save it normally as date and then translate it into unix timestamp...duh)

---
