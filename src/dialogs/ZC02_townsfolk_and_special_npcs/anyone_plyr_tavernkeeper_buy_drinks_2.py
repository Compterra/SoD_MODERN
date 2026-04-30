DIALOGS = [
[anyone|plyr, "tavernkeeper_buy_drinks_2",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$temp"),
        (str_store_party_name, s10, "$current_town"),
    ], "Let everyone know of the generosity of {playername} to the people of {s10}.", "tavernkeeper_buy_drinks_end", [

        ]],
]
