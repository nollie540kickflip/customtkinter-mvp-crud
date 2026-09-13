import os
import tempfile
from collections.abc import Generator

import pytest

from src.model.database import init_db
from src.model.user_model import UserModel


@pytest.fixture
def model() -> Generator[UserModel]:
    """テスト用の一時ファイルDBを使用するUserModelのフィクスチャ"""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    init_db(db_path)
    yield UserModel(db_path)

    # テスト後にファイルを削除
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_and_get_all(model: UserModel) -> None:
    """ユーザーの作成と全件取得のテスト"""
    model.create("Taro", "taro@example.com", 20)
    model.create("Hanako", "hanako@example.com", 25)

    users = model.get_all()
    # 降順で取得されるはずなので、Hanakoが先頭、Taroが次になる
    assert len(users) == 2
    assert users[0][1] == "Hanako"
    assert users[1][1] == "Taro"


def test_update(model: UserModel) -> None:
    """ユーザー情報の更新テスト"""
    model.create("Taro", "taro@example.com", 20)
    users = model.get_all()
    user_id = users[0][0]

    model.update(user_id, "Taro Updated", "taro_new@example.com", 21)

    updated_users = model.get_all()
    assert updated_users[0][1] == "Taro Updated"
    assert updated_users[0][2] == "taro_new@example.com"
    assert updated_users[0][3] == 21


def test_delete(model: UserModel) -> None:
    """ユーザー情報の削除テスト"""
    model.create("Taro", "taro@example.com", 20)
    users = model.get_all()
    assert len(users) == 1

    user_id = users[0][0]
    model.delete(user_id)

    users_after_delete = model.get_all()
    assert len(users_after_delete) == 0
