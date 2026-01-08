import argparse
import asyncio
import getpass

from sqlalchemy import select

from src.db.postgres.config import async_session_maker
from src.db.postgres.models import AdminUser
from src.auth.passwords import hash_password


async def cmd_createadmin(username: str, password: str) -> None:
    async with async_session_maker() as session:
        res = await session.execute(select(AdminUser).where(AdminUser.username == username))
        exists = res.scalar_one_or_none()

        if exists:
            raise SystemExit(f"Пользователь'{username}' уже существует")

        session.add(
            AdminUser(
                username=username,
                password_hash=hash_password(password),
                is_active=True,
            )
        )
        await session.commit()

    print(f"Пользователь '{username}' создан")


def prompt_username(value: str | None) -> str:
    if value and value.strip():
        return value.strip()
    return input("Имя пользователя: ").strip()


def prompt_password(value: str | None) -> str:
    if value:
        return value
    p1 = getpass.getpass("Пароль: ")
    p2 = getpass.getpass("Ещё раз пароль: ")
    if p1 != p2:
        raise SystemExit("Пароли не совпадают")
    if not p1:
        raise SystemExit("Пароль не может быть пустым")
    return p1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m src.management")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("createsuperuser", help="Создаёт администратора")
    p.add_argument("--username", "-u", help="Имя пользователя")
    p.add_argument("--password", "-p", help="Пароль")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "createadmin":
        username = prompt_username(args.username)
        password = prompt_password(args.password)
        asyncio.run(cmd_createadmin(username, password))
        return

    raise SystemExit("Неизвестная команда")


if __name__ == "__main__":
    main()
