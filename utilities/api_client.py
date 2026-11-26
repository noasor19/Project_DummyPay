from playwright.sync_api import APIRequestContext


class ApiClient:
    def __init__(self, request: APIRequestContext):
        self.request = request

    def get(self, path: str, params=None):
        return self.request.get(path, params=params)

    def post(self, path: str, data: dict):
        return self.request.post(path, data=data)

    def patch(self, path: str, data: dict, params=None):
        return self.request.patch(
            path, data=data, params=params
        )

    def delete(self, path: str, params=None):
        return self.request.delete(path, params=params)