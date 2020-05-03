class NoGuildError(Exception):
    # DMチャンネルだった場合のエラー
    pass

class PermissionNotFound(Exception):
    # 権限がないエラー
    pass

