from datetime import date
import get_time

today = date.today()
day = today.day
suffix = get_time.get_ordinal_suffix(day)

SITES = [
    ("mrfz-wtable flex-table", "https://arknights.wiki.gg/wiki/Event", "Arknights"),
    (f"lcbtable2", "https://limbuscompany.wiki.gg/wiki/Events", "Limbus Company")
]