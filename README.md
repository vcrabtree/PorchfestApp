# PorchfestApp
This is a web application I made for my Advanced Web Programming class at Ithaca College. It utilizes Flask to incorperate a HTML front-end, Python back-end, and SQLite database. There are also additional components such as a Javascript countdown, Google Map API, and AJAX button.

## Pages
- **Home**: This is the first page the user views, it includes a Javascript countdown and a YouTube API
- **Artists**: This page is populated through the database and displays all of the artists contained in the database
- **Artist Page**: This page can be accessed when the user clicks on a specific artist from the artists page, and allows the user to view more information about a particular artist as well as add an artist to their favorites list by utilizing an AJAX button
- **Login**: This page allows a user to login or register for an account
- **Favorite Artists**: This page can be accessed once a user logs in, and displays all of the artists that have the favorite boolean as `true` for a given user
- **Maps**: This page can be accessed once a user logs in, and displays a Google Maps API of Ithaca with markers populated from the database for each porch at Porchfest
- **Band Registration**: This page can be accessed once a user logs in, and allows a user to complete a form and add a band to the database
