class CustomLogFilter:
    def filter(self, record):
        # Skip Not Found errors for specific paths
        if record.getMessage().startswith("Not Found: /api/tanques/"):
            return False

        if record.getMessage().startswith("Not Found: /favicon.ico"):
            return False

        if record.getMessage().startswith("Not Found: /main/dist/img/user3-128x128.jpg"):
            return False

        if record.getMessage().startswith("Not Found: /main/dist/img/user1-160x160.jpg"):
            return False
        return True