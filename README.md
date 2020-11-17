# FreshBooks Python SDK

The FreshBooks Python SDK allows you to more easily utilize the [FreshBooks API](https://www.freshbooks.com/api).

## Installation

TBD when in pypi.

## Usage

### Configuring the API client

You can create an instance of the API client in one of two ways:

- By providing your application's OAuth2 `client_id` and `client_secret` and following through the auth flow, which when complete will return an access token
- Or if you already have a valid access token, you can instanciate the client directly using that token, however token refresh flows will not function without the application id and secret.

```python
from freshbooks import Client

freshBooksClient = FreshBooksClient(
    client_id=<your application id>,
    client_secret=<your application secret>,
    redirect_uri=<your redirect uri>
)
```

and then proceed with the auth flow (see below).

Or

```python
from freshbooks import Client

freshBooksClient = FreshBooksClient(access_token=<a valid token>)
```

#### Authoization flow

TODO: Not yet written.

### Making API Calls

Each resource in the client has provides calls for `get`, `list`, `create`, `update` and `delete` calls. Please note that some API resources are scoped to a FreshBooks `account_id` while others are scoped to a `business_id`. In general these fall along the lines of accounting resources vs projects/time tracking resources, but that is not precise.

```python
client = freshBooksClient.clients.get(account_id, client_user_id)
project = freshBooksClient.projects.get(business_id, project_id)
```

#### Get and List

API calls with a single resouce return a `Result` object with the returned data accessible via attributes. The raw json-parsed dictionary can also be accessed via the `data` attribute.

```python
client = freshBooksClient.clients.get(account_id, client_user_id)

assert client.organization == "FreshBooks"
assert client.userid == user_id

assert client.data["organization"] == "FreshBooks"
assert client.data["userid"] == user_id
```

API calls with returning a list of resources return a `ListResult` object. The resources in the list can be accessed by index and iterated over. Similarly, the raw dictionary can be accessed via the `data` attribute.

```python
clients = freshBooksClient.clients.list(account_id)

assert clients[0].organization == "FreshBooks"

assert clients.data["clients"][0]["organization"] == "FreshBooks"

for client in clients:
    assert client.organization == "FreshBooks"
    assert client.data["organization"] == "FreshBooks"
```

#### Create and Update

API calls to create and update take a dictionary of the resource data. A successful call will return a `Result` object as if a `get` call.

Create:

```python
payload = {"email": "john.doe@abcorp.com"}
new_client = FreshBooksClient.clients.create(account_id, payload)

client_id = new_client.userid
```

Update:

```python
payload = {"email": "john.doe@abcorp.ca"}
client = FreshBooksClient.clients.update(account_id, client_id, payload)

assert client.email == "john.doe@abcorp.ca"
```

#### Pagination, Filters, and Includes

`list` calls take a list of builder objects that can be used to paginate, filter, and include
optional data in the response. See [FreshBooks API - Parameters](https://www.freshbooks.com/api/parameters) documentation.

##### Pagination

Pagination results are included in `list` responses in the `pages` attribute:

```python
>>> clients.pages
PageResult(page=1, pages=1, per_page=30, total=6)

>>> clients.pages.total
6
```

To make change a paginated call, first build a `PaginatorBuilder` object that can be passed into the `list` method.

```python
>>> from freshbooks import PaginatorBuilder

>>> paginator = PaginatorBuilder(2, 4)
>>> paginator
PaginatorBuilder(page=2, per_page=4)

>>> clients = freshBooksClient.clients.list(account_id, builders=[paginator])
>>> clients.pages
PageResult(page=2, pages=3, per_page=4, total=9)
```

`PaginatorBuilder` has methods `page` and `per_page` to return or set the values. When setting the values the calls can be chained.

```python
>>> paginator = PaginatorBuilder(1, 3)
>>> paginator
PaginatorBuilder(page=1, per_page=3)

>>> paginator.page()
1

>>> paginator.page(2).per_page(4)
>>> paginator
PaginatorBuilder(page=2, per_page=4)
```

##### Filters

To filter which results are return by `list` method calls, construct a `FilterBuilder` and pass that
in the list of builders to the `list` method.

```python
>>> from freshbooks import FilterBuilder

>>> filter = FilterBuilder()
>>> filter.equals("userid", 123)

>>> clients = freshBooksClient.clients.list(account_id, builders=[filter])
```

Filters can be builts with the methods: `equals`, `in_list`, `like`, `between`, and `boolean`,
which can be chained together.

```python
>>> f = FilterBuilder()
>>> f.like("email_like", "@freshbooks.com")
FilterBuilder(&search[email_like]=@freshbooks.com)

>>> f = FilterBuilder()
>>> f.in_list("clientids", [123, 456]).boolean("active", False)
FilterBuilder(&search[clientids][]=123&search[clientids][]=456&active=False)

>>> f = FilterBuilder()
>>> f.boolean("active", False).in_list("clientids", [123, 456])
FilterBuilder(&active=False&search[clientids][]=123&search[clientids][]=456)

>>> f = FilterBuilder()
>>> f.between("amount", [1, 10])
FilterBuilder(&search[amount_min]=1&search[amount_max]=10)

>>> f = FilterBuilder()
>>> f.between("start_date", date.today())
FilterBuilder(&search[start_date]=2020-11-21)
```

##### Includes

## Development

### Testing

To run all tests:

```bash
make test
```

To run a single test with pytest:

```bash
py.test path/to/test/file.py
py.test path/to/test/file.py::TestClass::test_case
```

### Documentations

You can generate the documentation via:

```bash
make generate-docs
```
