class OpenCanadaException(Exception):
    ...


class DatasetException(OpenCanadaException):
    ...


class ResourceException(OpenCanadaException):

    def __init__(self, resource_id: str):
        self.resource_id = resource_id


class ResourceDoesNotExistException(ResourceException):
    ...
