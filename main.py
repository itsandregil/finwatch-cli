import typer

from finwatch.commands import market

app = typer.Typer()
app.add_typer(market.app, name="market")


if __name__ == "__main__":
    app()
