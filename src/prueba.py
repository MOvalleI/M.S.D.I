import hashlib

def hased_passwd(passwd):
    h = hashlib.new("SHA256")
    h.update(passwd.encode())

    return h.hexdigest()

print("Passwd: admin")
print(f"hash: {hased_passwd("123")}")

