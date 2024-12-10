from decouple import AutoConfig

env = AutoConfig()

DATABASE_URL = env("DATABASE_URL")

# Ensure these are integers
ACCESS_TOKEN_EXPIRE_MINUTES = int(env("ACCESS_TOKEN_EXPIRE_MINUTES", 15))  # Default to 15 if not set
REFRESH_TOKEN_EXPIRE_MINUTES = int(env("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))  # Default to 1440 minutes (1 day) if not set

# JWT secret keys (use default if not set)
JWT_SECRET_KEY = env("JWT_SECRET_KEY", "default_access_secret")
JWT_REFRESH_SECRET_KEY = env("JWT_REFRESH_SECRET_KEY", "default_refresh_secret")

# Algorithm (HS256 is a common default)
ALGORITHM = env("ALGORITHM", "HS256")





git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mukulbiswas5558/newAuthFast.git
git push -u origin main


# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30
# REFRESH_TOKEN_EXPIRE_MINUTES=10080
# JWT_SECRET_KEY=your_access_secret_key
# JWT_REFRESH_SECRET_KEY=your_refresh_secret_key
# DATABASE_URL=postgresql://postgres:password@localhost/test