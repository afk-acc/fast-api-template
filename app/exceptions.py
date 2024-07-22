from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)

IncorrectEmailOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="неверная почта или пароль"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="токен истек"
)
TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="токен отсутствует"
)
IncorrectTokenException = HTTPException(
    status_code=401, detail="неверный формат токена"
)
UserIsNotPresentException = HTTPException(status_code=404, detail="user not found")
UserIsNotAdminException = HTTPException(status_code=403, detail="user is not admin")
RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Нет осталось свободных мест"
)
ModelNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена"
)
NotPermissionException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Нет соответствующего разрешения для выполнения этого действия"
)
