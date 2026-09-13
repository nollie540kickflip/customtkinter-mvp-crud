from unittest.mock import MagicMock

import pytest

from src.presenter.main_presenter import MainPresenter


@pytest.fixture
def mock_model():
    """UserModelのモック"""
    model = MagicMock()
    # get_allのデフォルトの戻り値を設定
    model.get_all.return_value = [(1, "Taro", "taro@example.com", 20)]
    return model


@pytest.fixture
def mock_view():
    """MainViewのモック"""
    view = MagicMock()
    return view


@pytest.fixture
def presenter(mock_model, mock_view):
    """MainPresenterのテストインスタンス"""
    return MainPresenter(mock_model, mock_view)


def test_refresh_data_on_init(presenter, mock_model, mock_view):
    """初期化時に refresh_data が呼ばれ、Viewにデータが渡されること"""
    mock_model.get_all.assert_called_once()
    mock_view.display_users.assert_called_once_with(
        [(1, "Taro", "taro@example.com", 20)]
    )


def test_handle_add_success(presenter, mock_model, mock_view):
    """入力値が正常な場合、createが呼ばれUIがクリア・更新されること"""
    mock_view.get_inputs.return_value = {
        "id": 0,
        "name": "Hanako",
        "email": "hanako@example.com",
        "age": "25",
    }

    presenter.handle_add()

    mock_model.create.assert_called_once_with("Hanako", "hanako@example.com", 25)
    mock_view.clear_inputs.assert_called_once()
    # 初期化時と合わせて2回呼ばれるはず
    assert mock_model.get_all.call_count == 2


def test_handle_add_validation_error(presenter, mock_model, mock_view):
    """必須項目が空の場合、エラーダイアログが表示されcreateは呼ばれないこと"""
    mock_view.get_inputs.return_value = {
        "id": 0,
        "name": "",
        "email": "hanako@example.com",
        "age": "25",
    }

    presenter.handle_add()

    mock_model.create.assert_not_called()
    mock_view.show_error.assert_called_once_with(
        "入力エラー", "名前とメールアドレスは必須です。"
    )


def test_handle_delete_success(presenter, mock_model, mock_view):
    """削除処理が正しく行われること"""
    mock_view.get_inputs.return_value = {
        "id": 1,
        "name": "Taro",
        "email": "taro@example.com",
        "age": "20",
    }

    presenter.handle_delete()

    mock_model.delete.assert_called_once_with(1)
    mock_view.clear_inputs.assert_called_once()
