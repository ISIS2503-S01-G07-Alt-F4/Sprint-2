
import secrets, base64
print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())
# o hex:
import secrets
print(secrets.token_hex(32))