import click
from scraper import Skoler

@click.command(help='Hent skoler fra Undervisningsministeriets hjemmeside og geokod dem.')
@click.argument('kommune')
def main(kommune):
    skoler = Skoler(kommune)
    skoler_kommune = skoler.get_skoledata()

    df = skoler.create_df(skoler_kommune)
    df_med_koordinater = skoler.geokod(df)

    skoler.to_csv(df_med_koordinater)

if __name__ == "__main__":
    main()