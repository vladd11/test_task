from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import RequestFingerprinterProtocol


class URLDupeFilter(RFPDupeFilter):
    def __init__(
            self,
            path: str | None = None,
            debug: bool = False,
            *,
            fingerprinter: RequestFingerprinterProtocol | None = None,
    ) -> None:
        self.requested = set()
        RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        if request.url in self.requested:
            return True
        self.requested.add(request.url)
        return False
