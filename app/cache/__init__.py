import redis

class CacheServices:

    # We store services in a key value pair
    services = {}
    
    @classmethod
    def create_redis_service(cls, service_key = 'my_cache', host = 'localhost', port = 6379, **kwargs):

        service = redis.StrictRedis(
            host=host, port=port, **kwargs
        )

        cls.services[service_key] = service
        return service

    @classmethod
    def get_redis_service(cls, service_key):

        service = cls.services.get(service_key, None)

        if service is None:
            raise Exception(f'No cache service available for {service_key}')

        return service