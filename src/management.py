import argparse
import asyncio
import getpass

from src.runtime import postgres_uow_factory
from src.services.admin_user_service import AdminUserService


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

    p = sub.add_parser("createadmin", help="Создаёт администратора")
    p.add_argument("--username", "-u", help="Имя пользователя")
    p.add_argument("--password", "-p", help="Пароль")
    return parser


async def run_createadmin(username: str, password: str) -> None:
    service = AdminUserService(postgres_uow_factory)
    try:
        user = await service.create_admin(username, password)
    except RuntimeError as e:
        raise SystemExit(str(e))
    except ValueError as e:
        raise SystemExit(str(e))

    print(f"Пользователь '{user.username}' создан")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "createadmin":
        username = prompt_username(args.username)
        password = prompt_password(args.password)
        asyncio.run(run_createadmin(username, password))
        return

    raise SystemExit("Неизвестная команда")


if __name__ == "__main__":
    main()
