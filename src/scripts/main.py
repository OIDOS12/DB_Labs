# main.py
from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from database import get_connection
from models import UserInDB, UserCreate, UserUpdate, DataInDB, DataCreate, DataUpdate

app = FastAPI(
    title="My API",
    description="API for managing users and data",
    version="1.0.0"
)

# ---------------------- USERS ----------------------

@app.get("/user", response_model=List[UserInDB], tags=["Users"])
async def get_all_users():
    """
    Отримати всіх користувачів
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


@app.get("/user/{user_id}", response_model=UserInDB, tags=["Users"])
async def get_user_by_id(user_id: int):
    """
    Отримати користувача за ID
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/user", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def add_user(user: UserCreate):
    """
    Додати нового користувача
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO user (firstname, password, lastname, email, login)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (
            user.firstname,
            user.password,
            user.lastname,
            user.email,
            user.login
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": f"User {user.firstname} {user.lastname} successfully added"}


@app.put("/user/{user_id}", response_model=dict, tags=["Users"])
async def update_user(user_id: int, user_update: UserUpdate):
    """
    Оновити інформацію про користувача
    """
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []
    update_data = user_update.model_dump(exclude_unset=True) # Use model_dump to get only provided fields

    for key, value in update_data.items():
        fields.append(f"{key} = %s")
        values.append(value)

    if not fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update")

    values.append(user_id)
    query = f"UPDATE user SET {', '.join(fields)} WHERE user_id = %s"
    try:
        cursor.execute(query, values)
        conn.commit()
        updated_rows = cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    if updated_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await get_user_by_id(user_id)


@app.delete("/user/{user_id}", response_model=dict, tags=["Users"])
async def delete_user(user_id: int):
    """
    Видалити користувача
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    if deleted_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": f"User with id {user_id} deleted"}


# ---------------------- DATA ----------------------

@app.get("/data", response_model=List[DataInDB], tags=["Data"])
async def get_all_data():
    """
    Отримати всі записи data
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.get("/data/{data_id}", response_model=DataInDB, tags=["Data"])
async def get_data_by_id(data_id: int):
    """
    Отримати data по ID
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data where data_id = %s", (data_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

@app.post("/data", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Data"])
async def add_data(data_item: DataCreate):
    """
    Додати новий запис data
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO data (category_id, description, createdAt, updatedAt, content, format, name)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (
            data_item.category_id,
            data_item.description,
            data_item.createdAt.isoformat(), # Convert datetime to ISO format string for database
            data_item.updatedAt.isoformat(),
            data_item.content,
            data_item.format,
            data_item.name
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Data added"}


@app.put("/data/{data_id}", response_model=dict, tags=["Data"])
async def update_data(data_id: int, data_update: DataUpdate):
    """
    Оновити запис data за ID
    """
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []
    update_data_dict = data_update.model_dump(exclude_unset=True)

    for key, value in update_data_dict.items():
        # Handle datetime objects for database insertion
        if isinstance(value, datetime):
            value = value.isoformat()
        fields.append(f"{key} = %s")
        values.append(value)

    if not fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update")

    values.append(data_id)
    query = f"UPDATE data SET {', '.join(fields)} WHERE data_id = %s"
    try:
        cursor.execute(query, values)
        conn.commit()
        updated_rows = cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    if updated_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return await get_data_by_id(data_id)


@app.delete("/data/{data_id}", response_model=dict, tags=["Data"])
async def delete_data(data_id: int):
    """
    Видалити запис data за ID
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM data WHERE data_id = %s", (data_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    if deleted_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return {"message": f"Data with id {data_id} deleted"}
