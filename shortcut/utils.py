

def generate_short_url():
    import random
    import string

    length = 6  # Length of the short URL
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(length))
    
    return short_url