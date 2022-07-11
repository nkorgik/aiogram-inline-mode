import click

from inline_mode_urls.handlers.handlers import register_handlers
from inline_mode_urls.utils.main import dp

@click.group()
def cli():
    register_handlers(dp)


@cli.command()
@click.option('--skip_updates', is_flag=False, default=True, help='It allows you to skip all updates')
def polling(skip_updates):
    from aiogram import executor

    async def on_startup(_):
        print('Your bot has been started successfully!')

    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           skip_updates=skip_updates)


if __name__ == "__main__":
    cli()
