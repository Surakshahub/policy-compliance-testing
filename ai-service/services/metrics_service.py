class MetricsService:

    request_count = 0
    cache_hits = 0
    fallback_count = 0
    total_response_time = 0

    @staticmethod
    def add_request(response_time):

        MetricsService.request_count += 1
        MetricsService.total_response_time += response_time

    @staticmethod
    def add_cache_hit():

        MetricsService.cache_hits += 1

    @staticmethod
    def add_fallback():

        MetricsService.fallback_count += 1

    @staticmethod
    def get_metrics():

        avg_response = 0

        if MetricsService.request_count > 0:

            avg_response = round(
                MetricsService.total_response_time /
                MetricsService.request_count,
                3
            )

        return {
            "request_count": MetricsService.request_count,
            "cache_hits": MetricsService.cache_hits,
            "fallback_count": MetricsService.fallback_count,
            "average_response_time": avg_response
        }