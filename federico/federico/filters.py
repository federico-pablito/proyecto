class CustomLogFilter:
    def filter(self, record):
        # Skip GET requests
        if getattr(record, 'request_method', '') == 'GET':
            return False

        # Skip Not Found errors for specific paths
        if record.getMessage().startswith("Not Found: /api/tanques/"):
            return False

        if record.getMessage().startswith("Not Found: /favicon.ico"):
            return False

        return True