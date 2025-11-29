from proper import errors

from ..router import router
from .base import BaseController


class PublicController(BaseController):
    # Uncomment to add a home page
    # @router.get("")
    # def index(self):
    #     pass

    @router.error(errors.NotFound)
    @router.get("_not_found")
    def not_found(self):
        pass

    @router.error(Exception)
    @router.get("_error")
    def error(self):
        pass
