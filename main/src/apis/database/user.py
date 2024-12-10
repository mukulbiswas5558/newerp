from fastapi import HTTPException
from tools.database import Db
from main.src.apis.models.user import User, UserCredentials,CreateUser,UpdateUser
from datetime import datetime
from tools.token import create_access_token, create_refresh_token,get_password_hash
async def get_an_user_from_database(userid: int = None):
    db = await Db()

    result = await db.fetchrow("SELECT name, username, role FROM users WHERE id = $1", userid)

    db.close()

    if not userid:
        raise HTTPException(status_code=404, detail="User not found")

    return User(**result)


async def get_all_users_from_database():
    db = await Db()
    result = await db.fetch("SELECT id,name, username, role FROM users")
    db.close()
    return [User(**user) for user in result]

async def verify_user(username):
    db = await Db()
    result = await db.fetchrow("SELECT id, username, password FROM users WHERE username = $1", username)
    await db.close()  # Don't forget to close the database connection
    return result


async def create_user_service(user: CreateUser):
    # Initialize database connection
    db = await Db()

    # Check if the username already exists in the database
    query_check = "SELECT id FROM users WHERE username = $1"
    existing_user = await db.fetchrow(query_check, user.username)

    # If the username exists, raise an exception
    if existing_user:
        return {"message": "Username already exists. Please login."}

    # Hash the password using the method in CreateUser model
    hashed_password = get_password_hash(user.password)

    # Insert the new user into the database with hashed password
    query = """
    INSERT INTO users (name, username, password, role) 
    VALUES ($1, $2, $3, $4) 
    RETURNING id, name, username, role;
    """
    result = await db.fetchrow(query, user.name, user.username, hashed_password, user.role)
    if not result:
        raise HTTPException(status_code=500, detail="User registration failed.")

    # Prepare user data for token creation
    user_data = {
        "id": result["id"],
        "username": result["username"],
        "role": result["role"]
    }

    # Create access and refresh tokens
    access_token = create_access_token(data=user_data)
    refresh_token = create_refresh_token(data=user_data)
     
    db.close()
    # Return user details along with the tokens
    return {
        "user": dict(result),
        "access_token": access_token,
        "refresh_token": refresh_token
    }

async def update_user_service(username: str, user_data: UpdateUser):
    try:
        db = await Db()  # Initialize database connection
        query = """
        UPDATE users
        SET phone = $1, department = $2, shift_information = $3, employee_type = $4, 
            job_position = $5, reporting_manager = $6, work_location = $7, work_type = $8, 
            salary = $9, company = $10, bank_name = $11, branch = $12, bank_address = $13, 
            bank_code_1 = $14, bank_code_2 = $15, account_number = $16, bank_country = $17, 
            address_line_1 = $18, address_line_2 = $19, city = $20, district = $21, 
            state = $22, country = $23, postal_code = $24, updated_at = CURRENT_TIMESTAMP
        WHERE username = $25
        RETURNING id, username, phone, department, shift_information, employee_type, job_position, 
                  reporting_manager, work_location, work_type, salary, company, bank_name, branch, 
                  bank_address, bank_code_1, bank_code_2, account_number, bank_country, address_line_1, 
                  address_line_2, city, district, state, country, postal_code, updated_at;
        """
        values = [
            user_data.phone, user_data.department, user_data.shift_information, user_data.employee_type,
            user_data.job_position, user_data.reporting_manager, user_data.work_location, user_data.work_type,
            user_data.salary, user_data.company, user_data.bank_name, user_data.branch, user_data.bank_address,
            user_data.bank_code_1, user_data.bank_code_2, user_data.account_number, user_data.bank_country,
            user_data.address_line_1, user_data.address_line_2, user_data.city, user_data.district,
            user_data.state, user_data.country, user_data.postal_code, username
        ]

        async with db.transaction():
            updated_user = await db.fetchrow(query, *values)  # Correct asyncpg method

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found or update failed.")

        return {
            "message": "User updated successfully.",
            "user": dict(updated_user)  # Convert Record object to dict
        }

    except Exception as e:
        print(f"Error while updating user: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the user.")