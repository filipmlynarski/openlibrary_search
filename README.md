#### How to install:
1. install [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) (please download [version 4.8.2](https://docs.docker.com/desktop/release-notes/#docker-desktop-482)).
2. inside cloned repo, build the container with `docker-compose build`
3. and run the project `docker-compose up`
---

#### Example requests flow to this service using curl
```bash
# search openlibrary by author
curl localhost:8000/search/tolkien/
[
   {
      "key":"/works/OL262758W",
      "title":"The Hobbit",
      "author_key":[
         "OL26320A"
      ],
      "author_name":[
         "J.R.R. Tolkien"
      ]
   },
   ...
]

# save response as CSV file
curl localhost:8000/search.csv/tolkien/ --output search.csv
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 10325  100 10325    0     0   102k      0 --:--:-- --:--:-- --:--:--  101k

# peek CSV contents
head -4 search.csv                                    
author_key,author_name,key,title
['OL26320A'],['J.R.R. Tolkien'],/works/OL262758W,The Hobbit
['OL26320A'],['J.R.R. Tolkien'],/works/OL14933414W,The Fellowship of the Ring
['OL26320A'],['J.R.R. Tolkien'],/works/OL27479W,The Two Towers

# check author searches statistics for specific author_key
curl localhost:8000/author_searches/OL26320A/
{
   "author_key":"OL26320A",
   "author_name":"J.R.R. Tolkien",
   "count":1170
}

# check book searches statistics for specific book key
curl localhost:8000/book_searches/works/OL262758W
{
   "key":"/works/OL262758W",
   "title":"The Hobbit",
   "count":13
}
```

Admin views are available at
- localhost:8000/admin/core/authorsearches/
- localhost:8000/admin/core/booksearches/
