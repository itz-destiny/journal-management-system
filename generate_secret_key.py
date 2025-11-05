from django.core.management.utils import get_random_secret_key

# Generate a new secret key
secret_key = get_random_secret_key()

# Print the key
print("\nYour new Django secret key is:\n")
print(secret_key)
print("\nAdd this to your .env file as:\n")
print(f"DJANGO_SECRET_KEY={secret_key}\n")




