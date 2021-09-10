# FakeCommerce
An ecommerce site with a non refreshing frontend and a Backend REST API

- Frontend
  - HTML
  - XHR requests using XMLHttpRequest to prevent webpage refreshing when fetching posts
- Backend RESTful API server
  - Implements a number of commands
    - GET/: returns an html homepage
    - GET/items: gets all item listings for sale
    - GET/item/item_id: gets the listing details for 1 item
    - DELETE/item/item_id: Removes an item from being listed for sale
    - POST/item: lists an item for sale
  - Server is implemented using sockets   
