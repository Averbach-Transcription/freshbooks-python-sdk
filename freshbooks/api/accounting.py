from freshbooks.errors import FailedRequest, FreshBooksError
from freshbooks.api.resource import HttpVerbs, Resource
from freshbooks.models import Result, ListResult
from decimal import Decimal


class AccountingResource(Resource):

    def __init__(self, base_url, access_token, accounting_path, single_name, list_name):
        super().__init__(base_url, access_token)
        self.accounting_path = accounting_path
        self.single_name = single_name
        self.list_name = list_name

    def _get_url(self, account_id, resource_id=None):
        if resource_id:
            return "{}/accounting/account/{}/{}/{}".format(
                self.base_url, account_id, self.accounting_path, resource_id)
        return "{}/accounting/account/{}/{}".format(self.base_url, account_id, self.accounting_path)

    def _extract_error(self, errors):
        if not errors:
            return "Unknown error", None

        if isinstance(errors, list):
            return errors[0]["message"], int(errors[0]["errno"])

        return errors["message"], int(errors["errno"])

    def _request(self, url, method, data=None):
        response = self._send_request(url, method, data)

        status = response.status_code
        if status == 200 and method == HttpVerbs.HEAD:
            # no content returned from a HEAD
            return

        try:
            content = response.json(parse_float=Decimal)
        except ValueError:
            raise FailedRequest(status, "Failed to parse response", raw_response=response.text)

        if "response" not in content:
            raise FailedRequest("Returned an unexpected response", raw_response=response.text)

        response = content["response"]
        if status >= 400:
            message, code = self._extract_error(response["errors"])
            raise FreshBooksError(status, message, error_code=code, raw_response=content)
        try:
            return response["result"]
        except KeyError:
            return response

    def get(self, account_id, resource_id):
        data = self._request(self._get_url(account_id, resource_id), HttpVerbs.GET)
        return Result(self.single_name, data)

    def list(self, account_id):
        data = self._request(self._get_url(account_id), HttpVerbs.GET)
        return ListResult(self.list_name, self.single_name, data)

    def create(self, account_id):
        pass

    def update(self, account_id, resource_id):
        pass

    def delete(self, account_id, resource_id):
        pass
