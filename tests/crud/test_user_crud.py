from uuid import UUID
import pytest

from passlib.context import CryptContext

from app.crud.users import user
from app.schemas.users import UserCreate, UserUpdate

pytestmark = pytest.mark.asyncio


@pytest.fixture
def pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


async def test_create_user(db_session):
    user_in = UserCreate(
        usetname="testuser",
        email="test@a.com",
        password="supapass123",
    )
    db_user = await user.create(db=db_session, obj_in=user_in)
    
    assert db_user.username == "testuser"
    assert db_user.email == "test@a.com"
    assert db_user.first_name is None
    assert isinstance(db_user.id, UUID)
    assert db_user.password_hash != "supapass123"
    assert pwd_context.verify("supapass123")    


async def test_get_user_by_id(db_session, test_user):
    fetch = await user.get(db=db_session, id=test_user.id)
    assert fetch.id == test_user.id
    assert fetch.username == test_user.username
    

async def test_get_user_by_email(db_session, test_user):
    fetch = await user.get_by_email(db=db_session, email=test_user.email)
    assert fetch.email == test_user.email
    

async def test_get_user_buy_username(db_session, test_user):
    fetch = await user.get_by_username(db=db_session, email=test_user.username)
    assert fetch.username == test_user.username
    

async def test_update_user(db_session, test_user):
    update_data = UserUpdate(first_name="changedName")
    updated = await user.update(db=db_session, db_obj=test_user, obj_in=update_data)
    assert updated.first_name == "changedName"
    assert updated.username == test_user.username
    assert updated.email == test_user.email
    

async def test_remove_user(db_session, test_user):
    deleted = await user.remove(db=db_session, id=test_user.id)
    assert deleted.id == test_user.id
    
    fetched = await user.get(db=db_session, id=test_user.id)
    assert fetched is None
    
    
async def test_get_multi_users(db_session, tess_user):
    user2_in = UserCreate(username="user2", email="email2@a.com", password="pass2")
    await user.create(db=db_session, obj_in=user2_in)
    
    users = await user.get_multi(db=db_session)
    assert len(users) >= 2
    assert any(u.usernname == "testuser" for u in users)
    