class UserLoginsData:
    def __init__(self, user_id, device_type, masked_ip, masked_device_id, locale, app_version):
        if not isinstance(user_id, str) or len(user_id) > 128:
            raise ValueError("user_id should be a string of length less than 128")
        if not isinstance(device_type, str) or len(device_type) > 32:
            raise ValueError("device_type should be a string of length less than 32")
        if not isinstance(masked_ip, str) or len(masked_ip) > 256:
            raise ValueError("masked_ip should be a string of length less than 256")
        if not isinstance(masked_device_id, str) or len(masked_device_id) > 256:
            raise ValueError("masked_device_id should be a string of length less than 256")
        if not isinstance(app_version, int):
            raise TypeError("app_version should be an integer")

        self.user_id = user_id
        self.device_type = device_type
        self.masked_ip = masked_ip
        self.masked_device_id = masked_device_id
        self.locale = locale
        self.app_version = app_version
