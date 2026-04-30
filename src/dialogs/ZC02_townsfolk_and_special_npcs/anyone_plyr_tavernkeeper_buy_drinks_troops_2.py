DIALOGS = [
[anyone|plyr, "tavernkeeper_buy_drinks_troops_2",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$temp"),
        (str_store_party_name, s10, "$current_town"),
    ], "The price is fair enough, let my men have at it.", "tavernkeeper_buy_drinks_troops_end", [

        ]],
]
