#!/usr/bin/env python3
"""Generate menu HTML and translation JSON for Czarne Mleko."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def item(key, pl_name, pl_price, pl_desc, en_name, en_price, en_desc):
    return {
        "key": key,
        "pl": {"name": pl_name, "price": pl_price, "desc": pl_desc},
        "en": {"name": en_name, "price": en_price, "desc": en_desc},
    }


def note(key, pl_text, en_text):
    return {"key": key, "note": True, "pl": pl_text, "en": en_text}


def item_html(it):
    if it.get("note"):
        k = it["key"]
        return f"""                <li class="menu-item menu-item--note">
                  <p class="menu-item-desc" data-i18n="menu.{k}">{it["pl"]}</p>
                </li>"""
    k = it["key"]
    pl = it["pl"]
    price = (
        f'\n                    <span class="menu-item-price" data-i18n="menu.{k}.price">{pl["price"]}</span>'
        if pl["price"]
        else ""
    )
    desc = (
        f'\n                  <p class="menu-item-desc" data-i18n="menu.{k}.desc">{pl["desc"]}</p>'
        if pl.get("desc")
        else ""
    )
    return f"""                <li class="menu-item">
                  <div class="menu-item-head">
                    <span class="menu-item-name" data-i18n="menu.{k}.name">{pl["name"]}</span>{price}
                  </div>{desc}
                </li>"""


def sub(i18n, text):
    return f'              <h4 class="menu-subcategory-heading" data-i18n="{i18n}">{text}</h4>\n'


META_PL = {
    "eyebrow": "Śniadania · kawa · lunch",
    "title": "Menu",
    "lead": "Śniadania, lunch, słodkości i napoje — przez cały dzień.",
    "catFood": "Jedzenie",
    "catBreakfast": "Śniadania",
    "catPanini": "Panini",
    "catScrambled": "Jajecznica",
    "catSandwiches": "Kanapki",
    "catToasts": "Tosty",
    "catSalads": "Sałatka",
    "catSweet": "Trochę słodkości",
    "catDrinks": "Napoje",
    "catSeasonalLattes": "Sezonowe latte",
    "catExtras": "Dodatki",
    "catMatcha": "Matcha i napoje specjalne",
    "catHotDrinks": "Inne napoje na ciepło",
    "catColdAlt": "Alternatywy kawowe i napoje na zimno",
    "catColdCoffee": "Kawa na zimno i napoje letnie",
    "catAltBrew": "Alternatywne parzenie",
    "catFreshJuice": "Świeżo wyciskane soki",
    "catCoffee": "Kawa",
}

META_EN = {
    "eyebrow": "Breakfast · coffee · lunch",
    "title": "Menu",
    "lead": "Breakfast, lunch, sweet treats and drinks — all day.",
    "catFood": "Food",
    "catBreakfast": "Breakfasts",
    "catPanini": "Panini",
    "catScrambled": "Scrambled eggs",
    "catSandwiches": "Sandwiches",
    "catToasts": "Toasts",
    "catSalads": "Salads",
    "catSweet": "Sweet options",
    "catDrinks": "Drinks",
    "catSeasonalLattes": "Seasonal lattes",
    "catExtras": "Extras",
    "catMatcha": "Matcha & specialty drinks",
    "catHotDrinks": "Other hot drinks",
    "catColdAlt": "Coffee alternatives & cold drinks",
    "catColdCoffee": "Cold coffee & summer drinks",
    "catAltBrew": "Alternative brew coffee",
    "catFreshJuice": "Fresh juice",
    "catCoffee": "Coffee",
}

BREAKFAST = [
    item(
        "food.french_toast",
        "Tosty francuskie",
        "33 zł",
        "Brioszka naszego wypieku z cynamonem, karmelizowaną śliwką, kruszonką i śmietaną.",
        "French toast",
        "33 PLN",
        "French toast on homemade brioche with cinnamon, caramelized plum, crumble, and sour cream.",
    ),
    item(
        "food.brioche_kimchi",
        "Brioszka z kimchi i jajkiem sadzonym",
        "33 zł",
        "Brioszka z kimchi, jajkiem sadzonym, serkiem śmietankowym, sałatą z rukoli, ogórkiem, cebulą, szczypiorkiem i sezamem.",
        "Brioche with kimchi & fried egg",
        "33 PLN",
        "Brioche with kimchi, fried egg, cream cheese, lamb's lettuce salad, cucumber, onion, chives, and sesame.",
    ),
    item(
        "food.chorizo_omelette",
        "Omlet z chorizo",
        "33 zł",
        "Omlet z sosem pomidorowym, brioszką naszego wypieku i sałatką sezonową.",
        "Chorizo omelette",
        "33 PLN",
        "Omelette with tomato sauce, homemade brioche, and seasonal salad.",
    ),
]

PANINI = [
    item(
        "food.panini_chicken",
        "Z kurczakiem",
        "",
        "Pieczony kurczak i camembert, podawane z sałatką i sosem miodowo-musztardowym.",
        "With chicken",
        "",
        "Roasted chicken and camembert, served with salad and honey-mustard sauce.",
    ),
    item(
        "food.panini_vege",
        "Wegetariańska",
        "",
        "Mozzarella i suszone pomidory, podawane z sałatką i sosem miodowo-musztardowym.",
        "Vegetarian",
        "",
        "Mozzarella and sun-dried tomatoes, served with salad and honey-mustard sauce.",
    ),
]

SCRAMBLED = [
    item(
        "food.scrambled",
        "Jajecznica",
        "",
        "2 jajka z żółtym serem, szynką, sałatką warzywną, sosem miodowo-musztardowym i ciepłym pieczywem.",
        "Scrambled eggs",
        "",
        "2 eggs with yellow cheese, ham, vegetable salad, honey-mustard sauce, and warm bread.",
    ),
]

SANDWICHES = [
    item(
        "food.sandwiches",
        "Kanapki",
        "",
        "z kurczakiem i camembertem · z suszonymi pomidorami i mozzarellą · z awokado i pastą z suszonych pomidorów",
        "Sandwiches",
        "",
        "with chicken and camembert · with sun-dried tomatoes and mozzarella · with avocado and sun-dried tomato paste",
    ),
]

TOASTS = [
    item(
        "food.toasts",
        "Tosty",
        "",
        "Z żółtym serem, szynką, sosem majonezowym i sałatką warzywną. Dostępne w wersji małej i dużej.",
        "Toasts",
        "",
        "Served with yellow cheese, ham, mayo sauce, and vegetable salad. Small / large sizes available.",
    ),
]

SALADS = [
    item(
        "food.salad_chicken",
        "Z kurczakiem",
        "",
        "Kurczak, camembert, warzywa, sos miodowo-musztardowy, ciepłe pieczywo.",
        "With chicken",
        "",
        "Chicken, camembert, vegetables, honey-mustard sauce, warm bread.",
    ),
    item(
        "food.salad_salmon",
        "Z łososiem",
        "",
        "Wędzony łosoś, mozzarella, warzywa, sos miodowo-musztardowy, ciepłe pieczywo.",
        "With salmon",
        "",
        "Smoked salmon, mozzarella, vegetables, honey-mustard sauce, warm bread.",
    ),
]

SWEET = [
    item(
        "food.sweet_bowls",
        "Granola · pudding chia · tapioka · owsianka",
        "",
        "mleko / woda / mleko roślinne (+3 zł)",
        "Granola · chia pudding · tapioca · oatmeal",
        "",
        "milk / water / plant milk (+3 PLN)",
    ),
    item(
        "food.sweet_toasts",
        "Słodkie tosty",
        "",
        "masło orzechowe · karmel i banan",
        "Sweet toasts",
        "",
        "peanut butter · caramel & banana",
    ),
]

SEASONAL_LATTES = [
    item(
        "drinks.pumpkin_spice",
        "Pumpkin spice latte",
        "18 zł",
        "230 / 400 ml",
        "Pumpkin spice latte",
        "18 PLN",
        "230 / 400 ml",
    ),
    item(
        "drinks.vanilla_cinnamon",
        "Wanilia z cynamonem",
        "18 zł",
        "Latte waniliowo-cynamonowe.\n230 / 400 ml",
        "Vanilla & cinnamon",
        "18 PLN",
        "Vanilla & cinnamon latte.\n230 / 400 ml",
    ),
    item(
        "drinks.spiced_latte",
        "Korzenne latte",
        "18 zł",
        "230 / 400 ml",
        "Spiced latte",
        "18 PLN",
        "230 / 400 ml",
    ),
    item(
        "drinks.mocha",
        "Mokka",
        "18 zł",
        "230 / 400 ml",
        "Mocha latte",
        "18 PLN",
        "230 / 400 ml",
    ),
]

EXTRAS = [
    item("drinks.extra_espresso", "Dodatkowe espresso", "5 zł", "", "Extra espresso", "5 PLN", ""),
    item("drinks.plant_milk", "Mleko roślinne", "2 zł", "", "Plant milk", "2 PLN", ""),
]

MATCHA = [
    item(
        "drinks.plum_matcha",
        "Śliwkowa matcha latte",
        "21 zł",
        "300 ml",
        "Plum matcha latte",
        "21 PLN",
        "300 ml",
    ),
    item(
        "drinks.salted_matcha",
        "Salted matcha z miodem",
        "21 zł",
        "300 ml",
        "Salted matcha with honey",
        "21 PLN",
        "300 ml",
    ),
    item(
        "drinks.hojicha",
        "Hojicha latte",
        "20 zł",
        "Alternatywa dla matchy.\n300 ml",
        "Hojicha latte",
        "20 PLN",
        "Alternative to matcha.\n300 ml",
    ),
    item("drinks.chai", "Chai latte", "19 zł", "300 ml", "Chai latte", "19 PLN", "300 ml"),
]

HOT_DRINKS = [
    item(
        "drinks.lavender_ginger",
        "Lawendowy napar imbirowy",
        "20 zł",
        "Napar lawendowo-imbirowy z cytrusami i miodem.\n400 ml",
        "Lavender ginger infusion",
        "20 PLN",
        "Lavender ginger infusion with citrus and honey.\n400 ml",
    ),
    item(
        "drinks.warming_tea",
        "Herbata rozgrzewająca",
        "20 zł",
        "Herbata czarna z cytrusami, goździkami i malinami.\n400 ml",
        "Warming tea",
        "20 PLN",
        "Black tea with citrus, cloves, and raspberries.\n400 ml",
    ),
]

COLD_ALT = [
    item(
        "drinks.cold_alt",
        "Alternatywy kawowe i napoje na zimno",
        "",
        "Herbaty aromatyczne · herbata czarna · herbata zielona · napar imbirowy · kakao · świeżo wyciskany sok pomarańczowy · smoothie owocowe · koktajl owocowy · woda gazowana / niegazowana · napoje butelkowane",
        "Coffee alternatives & cold drinks",
        "",
        "Aromatic teas · black tea · green tea · ginger infusion · cocoa · fresh orange juice · fruit smoothie · fruit cocktail · sparkling / still water · bottled drinks",
    ),
]

COLD_COFFEE = [
    item(
        "drinks.cold_coffee",
        "Kawa na zimno i napoje letnie",
        "",
        "Doppio z sokiem pomarańczowym · tonic espresso · iced drip · lemoniada · mrożona herbata owocowa · ice matcha · matcha tonic",
        "Cold coffee & summer drinks",
        "",
        "Doppio with orange juice · tonic espresso · iced drip · lemonade · iced fruit tea · ice matcha · matcha tonic",
    ),
]

ALT_BREW = [
    item("drinks.drip", "Drip", "", "250 ml", "Drip", "", "250 ml"),
    item("drinks.chemex", "Chemex", "", "300 ml", "Chemex", "", "300 ml"),
]

FRESH_JUICE = [
    item("drinks.orange_juice", "Pomarańcza", "", "", "Orange", "", ""),
    item("drinks.grapefruit_juice", "Grejpfrut", "", "", "Grapefruit", "", ""),
]

COFFEE = [
    item("drinks.espresso", "Espresso", "", "", "Espresso", "", ""),
    item("drinks.doppio", "Doppio", "", "", "Doppio", "", ""),
    item("drinks.black_coffee", "Kawa czarna", "", "", "Black coffee", "", ""),
    item("drinks.flat_white", "Flat white", "", "", "Flat white", "", ""),
    item(
        "drinks.cappuccino",
        "Cappuccino",
        "",
        "mały / duży",
        "Cappuccino",
        "",
        "small / large",
    ),
    item(
        "drinks.latte",
        "Latte",
        "",
        "mały / duży · opcja mleka roślinnego",
        "Latte",
        "",
        "small / large · plant milk option available",
    ),
]


def render_list(items):
    return "\n".join(item_html(i) for i in items)


def render_category(cat_key, pl_title, items):
    if not items:
        return ""
    return f"""{sub(f"menu.{cat_key}", pl_title)}
              <ul class="menu-items">
{render_list(items)}
              </ul>
"""


def build_menu_json_for_lang(meta, all_items, lang):
    menu = dict(meta)
    for it in all_items:
        if it.get("note"):
            menu[it["key"]] = it[lang]
            continue
        src = it[lang]
        entry = {"name": src["name"], "price": src["price"] or ""}
        if src.get("desc"):
            entry["desc"] = src["desc"]
        parts = it["key"].split(".")
        cur = menu
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = entry
    return menu


def main():
    food_sections = [
        ("catBreakfast", "Śniadania", BREAKFAST),
        ("catPanini", "Panini", PANINI),
        ("catScrambled", "Jajecznica", SCRAMBLED),
        ("catSandwiches", "Kanapki", SANDWICHES),
        ("catToasts", "Tosty", TOASTS),
        ("catSalads", "Sałatka", SALADS),
        ("catSweet", "Trochę słodkości", SWEET),
    ]
    drink_sections = [
        ("catSeasonalLattes", "Sezonowe latte", SEASONAL_LATTES),
        ("catExtras", "Dodatki", EXTRAS),
        ("catMatcha", "Matcha i napoje specjalne", MATCHA),
        ("catHotDrinks", "Inne napoje na ciepło", HOT_DRINKS),
        ("catColdAlt", "Alternatywy kawowe i napoje na zimno", COLD_ALT),
        ("catColdCoffee", "Kawa na zimno i napoje letnie", COLD_COFFEE),
        ("catAltBrew", "Alternatywne parzenie", ALT_BREW),
        ("catFreshJuice", "Świeżo wyciskane soki", FRESH_JUICE),
        ("catCoffee", "Kawa", COFFEE),
    ]

    all_items = []
    for _, _, items in food_sections + drink_sections:
        all_items.extend(items)

    food_html_parts = [
        '            <div class="menu-category">',
        '              <h3 class="menu-category-heading" data-i18n="menu.catFood">Jedzenie</h3>',
    ]
    for cat_key, pl_title, items in food_sections:
        food_html_parts.append(render_category(cat_key, pl_title, items))
    food_html_parts.append("            </div>")
    food_html = "\n".join(food_html_parts)

    drink_html_parts = [
        '            <div class="menu-category">',
        '              <h3 class="menu-category-heading" data-i18n="menu.catDrinks">Napoje</h3>',
    ]
    for cat_key, pl_title, items in drink_sections:
        drink_html_parts.append(render_category(cat_key, pl_title, items))
    drink_html_parts.append("            </div>")
    drinks_html = "\n".join(drink_html_parts)

    catalog = f"""          <div class="menu-catalog">
            <div class="menu-catalog-columns">
              <div class="menu-catalog-col menu-catalog-col--food">
{food_html}
              </div>
              <div class="menu-catalog-col menu-catalog-col--drinks">
{drinks_html}
              </div>
            </div>
          </div>"""

    index = (ROOT / "index.html").read_text()
    new_index = re.sub(
        r'          <div class="menu-catalog">[\s\S]*?</div>\n        </div>\n      </section>\n\n      <!-- Gallery -->',
        catalog + "\n        </div>\n      </section>\n\n      <!-- Gallery -->",
        index,
        count=1,
    )
    if new_index == index:
        raise SystemExit("Could not replace menu-catalog in index.html")

    (ROOT / "index.html").write_text(new_index)

    for lang, meta in [("pl", META_PL), ("en", META_EN)]:
        path = ROOT / "translations" / f"{lang}.json"
        data = json.loads(path.read_text())
        data["menu"] = build_menu_json_for_lang(meta, all_items, lang)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    print("OK:", len(all_items), "items")


if __name__ == "__main__":
    main()
