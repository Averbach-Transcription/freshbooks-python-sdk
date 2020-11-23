"""
The FreshBooks Python SDK allows you to more easily utilize the [FreshBooks API](https://www.freshbooks.com/api).

- See `freshbooks.client.Client` for instantiating a Client, auth, and resource calls
- See `freshbooks.api.accounting` and `freshbooks.api.projects` for resource methods (`get`, `list`, `create`, etc.)
- See `freshbooks.builders` for list filters, pagination, etc.
"""

from freshbooks.builders.filter import FilterBuilder  # noqa
from freshbooks.builders.paginator import PaginatorBuilder  # noqa
from freshbooks.client import Client  # noqa
from freshbooks.errors import FreshBooksError  # noqa

__pdoc__ = {
    "freshbooks.api.resource": False,
    "freshbooks.builders.paginator.PaginatorBuilder.MIN_PAGE": False,
    "freshbooks.builders.paginator.PaginatorBuilder.MAX_PER_PAGE": False
}
