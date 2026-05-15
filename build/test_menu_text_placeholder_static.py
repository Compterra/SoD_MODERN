from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_menu_text_placeholders_are_expanded_before_display() -> None:
    ladders = read("src/menus/centers/common/build_ladders_cont.py")
    tower = read("src/menus/centers/castle/build_siege_tower_cont.py")
    cattle = read("src/menus/centers/village/village_steal_cattle_confirm.py")
    taxes = read("src/menus/start_game/start_collecting.py")
    jotnar_pick = read("src/menus/jotnar/jc_choose_bet.py")
    jotnar_ready = read("src/menus/jotnar/player_choosen_select_bet.py")
    payday = read("src/menus/0000_hardcoded_mb1011/pay_day.py")
    upgrade = read("src/menus/other/sod_upgrade_continue.py")
    sod_upgrade = read("src/menus/other/sod_upgrade.py")
    sod_upgrade_camp = read("src/menus/camp/sod_upgrade_camp.py")
    training = read("src/menus/other/make_preparation.py")
    retreat = read("src/menus/prisoners/leave_behind.py")
    tournament = read("src/menus/other/go_back_dot.py")
    grant_message = read("src/menus/other/continue_18.py")
    grant_confirm = read("src/menus/other/continue_19.py")
    invasion_status = read("src/menus/reports/invasion_status_report.py")
    fief_prosperity = read("src/menus/kingdom/fief_prosperity_report.py")
    public_health = read("src/menus/kingdom/center_public_health_report.py")
    fief_trade_pressure = read("src/menus/kingdom/fief_trade_pressure_report.py")
    town_market = read("src/menus/economy/town_market_report.py")
    regional_economy_flow = read("src/menus/economy/regional_economy_flow_report.py")
    castle_support = read("src/menus/economy/castle_support_report.py")
    center_goods_market = read("src/menus/centers/common/center_goods_market_report.py")
    castle = read("src/menus/centers/castle/castle_castle.py")
    village = read("src/menus/centers/village/recruit_volunteers.py")
    siege = read("src/menus/centers/castle/siege_request_meeting.py")
    center_notes = read("src/scripts/ZD_centers/update_center_notes.py")
    castle_taken = read("src/menus/other/continue_17.py")
    cattle_stolen = read("src/menus/other/continue_30.py")
    tournament_other = read("src/menus/other/continue_36.py")
    tax_revolt = read("src/menus/other/continue_40.py")
    game_options_3 = read("src/menus/0000_hardcoded_mb1011/game_options_3.py")
    reports_menu = read("src/menus/0000_hardcoded_mb1011/reports.py")
    quick_start = read("src/menus/0000_hardcoded_mb1011/quick_start.py")
    add_companions = read("src/menus/0000_hardcoded_mb1011/add_companions.py")
    fief_reports = read("src/menus/0000_hardcoded_mb1011/fief_reports.py")
    lord_reports = read("src/menus/0000_hardcoded_mb1011/lord_reports.py")
    faction_relations = read("src/menus/0000_hardcoded_mb1011/faction_relations_report.py")
    guild_relations = read("src/menus/0000_hardcoded_mb1011/guilds_relations_report.py")
    lord_readiness = read("src/menus/kingdom/lord_readiness_report.py")
    lord_fief_assignment = read("src/menus/kingdom/lord_fief_assignment_report.py")
    construction_available = read("src/menus/kingdom/fief_available_construction_report.py")
    construction_current = read("src/menus/kingdom/fief_under_construction_report.py")
    pre_join = read("src/menus/encounter/pre_join_help_attackers.py")
    join_attack = read("src/menus/encounter/join_attack.py")
    prisoner_train = read("src/menus/prisoners/prisoner_train_orders.py")
    prisoner_economy = read("src/menus/prisoners/prisoner_economy_report.py")
    training_result = read("src/menus/training/training_ground_training_result.py")
    end_game = read("src/menus/0000_hardcoded_mb1011/end_game.py")

    for raw in (ladders, tower, cattle, taxes, training, retreat, grant_message, grant_confirm):
        assert_contains(raw, '"{s68}"')

    assert_contains(ladders, "you estimate that it will take {reg4} hours")
    assert_contains(ladders, "{s3} estimates that it will take {reg4} hours")
    assert_not_contains(ladders, "{reg3?you estimate:{s3} estimates}")

    assert_contains(tower, "you estimate that building a siege tower will take {reg4} hours")
    assert_contains(tower, "{s3} estimates that building a siege tower will take {reg4} hours")
    assert_not_contains(tower, "{reg3?you estimate:{s3} estimates}")

    assert_contains(cattle, "You reckon the herd can be driven off")
    assert_contains(cattle, "{s1} reckons the herd can be driven off")
    assert_not_contains(cattle, "{reg3?You reckon:{s1} reckons}")

    assert_contains(taxes, "You expect the tax collection to take {s2}.")
    assert_contains(taxes, "{s1} expects the tax collection to take {s2}.")
    assert_not_contains(taxes, "{reg3?You expect:{s1} expects}")

    assert_contains(training, "you expect that getting some peasants ready for practice will take {reg4} hours")
    assert_contains(training, "{s1} expects that getting some peasants ready for practice will take {reg4} hours")
    assert_not_contains(training, "{reg3?you expect:{s1} expects}")

    assert_contains(end_game, "You give up the adventurer's life")
    assert_not_contains(end_game, "sunset....")

    assert_contains(retreat, "you devise a plan that will allow you and your men to escape")
    assert_contains(retreat, "{s3} devises a plan that will allow you and your men to escape")
    assert_not_contains(retreat, "{reg3?you devise:{s3} devises}")

    assert_contains(tournament, "The odds against you are {reg5} to {reg6}{s68}{s2}")
    assert_contains(tournament, "You have already made regular bets of {reg1} denars")
    assert_not_contains(tournament, "{reg1? You have already made regular bets")

    assert_contains(grant_message, "She has decided to grant {s2} and the nearby village of {s4} to you")
    assert_contains(grant_message, "He has decided to grant {s2} to you")
    assert_not_contains(grant_message, "{reg4?She:He}")
    assert_not_contains(grant_message, "{reg3? and the nearby village")

    assert_contains(grant_confirm, '(str_store_string, s69, "@ and its bound village {s4}")')
    assert_contains(grant_confirm, "They will make a fine part of your fiefdom.")
    assert_contains(grant_confirm, "It will make a fine part of your fiefdom.")
    assert_not_contains(grant_confirm, "{reg3? and its bound village")
    assert_not_contains(grant_confirm, "{reg5?This is a high military honor")

    for raw in (jotnar_pick, jotnar_ready):
        assert_contains(raw, "Current bet: {s68}")
        assert_contains(raw, '(str_store_string, s68, "@{reg1} denars")')
        assert_contains(raw, '(str_store_string, s68, "@no bet")')
        assert_not_contains(raw, "{reg1?{reg1} denars:no bet}")
    assert_contains(jotnar_pick, "Your opponent has selected the following equipment:^{s69}")
    assert_contains(jotnar_pick, "Medium Armor, Two Handed Sword")
    assert_contains(jotnar_pick, "Light Armor, One Handed Sword, Shield, Bow and Arrows, Horse")
    assert_not_contains(jotnar_pick, "@{s1},")

    assert_contains(payday, 'assign, ":weekly_expense_entries", 0')
    assert_contains(payday, '(str_store_string, s68, "@Net income")')
    assert_contains(payday, '(str_store_string, s68, "@Total payment")')
    assert_contains(payday, '(str_store_string_reg, s97, s10)')
    assert_contains(payday, '(str_store_string_reg, s97, s20)')
    assert_contains(payday, "^{s68}: {reg7} denars")
    assert_not_contains(payday, '(str_store_string, s10, "@{s10}')
    assert_not_contains(payday, '(str_store_string, s20, "@{s20}')
    assert_not_contains(payday, "{reg0?{reg0}")
    assert_not_contains(payday, "{reg0?Net income:Total payment}")
    assert_not_contains(payday, "{reg9?Command purses")
    assert_not_contains(payday, "{reg12?Retinue shortages")
    assert_not_contains(payday, "{reg13?Unpaid retinue")

    assert_not_contains(upgrade, "{reg0?")

    for raw in (sod_upgrade, sod_upgrade_camp):
        assert_contains(raw, '"{s98}"')
        assert_contains(raw, "str_store_string_reg, s97")
        assert_not_contains(raw, '"{s1}"')
        assert_not_contains(raw, "@{s1}")
        assert_not_contains(raw, "@{s18},")

    assert_contains(invasion_status, '(str_store_string, s39, "@several realms have answered")')
    assert_contains(invasion_status, '(str_store_string, s39, "@too few realms have answered")')
    assert_contains(invasion_status, "Calradian war response: {s39}.")
    assert_not_contains(invasion_status, "{reg5?several realms have answered:too few realms have answered}")

    assert_contains(fief_prosperity, '(str_store_string, s68, "@fief")')
    assert_contains(fief_prosperity, '(str_store_string, s68, "@fiefs")')
    assert_contains(fief_prosperity, "Average prosperity for your {reg2} {s68} is")
    assert_contains(fief_prosperity, "Steward priority:")
    assert_contains(fief_prosperity, "Priority score {reg3}")
    assert_contains(fief_prosperity, "health, prosperity, population, and rent pressure")
    assert_contains(fief_prosperity, '"{s98}"')
    assert_contains(fief_prosperity, "(str_clear, s98)")
    assert_contains(fief_prosperity, "str_store_string_reg, s97, s98")
    assert_contains(fief_prosperity, "str_store_string_reg, s96, s8")
    assert_not_contains(fief_prosperity, "{reg0?fiefs:fief}")
    assert_not_contains(fief_prosperity, '"{s9}"')
    assert_not_contains(fief_prosperity, "@{s9}")

    assert_contains(public_health, '"{s98}"')
    assert_contains(public_health, "(str_clear, s98)")
    assert_contains(public_health, "str_store_string_reg, s97, s98")
    assert_contains(public_health, "Public Health Report:")
    assert_not_contains(public_health, '"{s9}"')
    assert_not_contains(public_health, "@{s8}^^")

    for raw in (fief_trade_pressure, town_market, regional_economy_flow, castle_support, center_goods_market):
        assert_contains(raw, "{s98}")
        assert_contains(raw, "(str_clear, s98)")
        assert_contains(raw, "str_store_string_reg, s97, s98")
        assert_not_contains(raw, '"{s9}"')
        assert_not_contains(raw, "@{s9}")
    assert_contains(fief_trade_pressure, "Trade and Prosperity Report:^^{s98}")
    assert_contains(town_market, "Town Market Report:")
    assert_contains(regional_economy_flow, "Regional Economy Flow Report:")
    assert_contains(castle_support, "Castle Support Report:")
    assert_contains(center_goods_market, "Center Goods Market Report:")

    for raw in (castle, village):
        assert_contains(raw, '(str_store_string, s68, "@Oversee the current")')
        assert_contains(raw, '(str_store_string, s68, "@Commission a new")')
        assert_contains(raw, '"{s68} due to {s1}."')
        assert_not_contains(raw, "{reg1?Oversee the current:Commission a new}")
        assert_not_contains(raw, "{reg5?Continue collecting taxes:Collect taxes}")
    assert_contains(castle, '(str_store_string, s69, "@town")')
    assert_contains(castle, '(str_store_string, s69, "@castle")')
    assert_contains(castle, "@{s68} building project at this {s69}.")
    assert_contains(village, "@{s68} building project at this village.")
    assert_not_contains(castle, "{reg0?town:castle}")

    assert_contains(siege, '(str_store_string, s68, "@town\'s")')
    assert_contains(siege, '(str_store_string, s68, "@castle\'s")')
    assert_contains(siege, "The {s68} food stores")
    assert_not_contains(siege, "{reg6?town's:castle's}")

    assert_contains(center_notes, '(str_store_string, s68, "@Its village is")')
    assert_contains(center_notes, '(str_store_string, s68, "@Its villages are")')
    assert_contains(center_notes, "(str_store_string_reg, s97, s2)")
    assert_contains(center_notes, "@{s97}{s68} {s8}.^")
    assert_not_contains(center_notes, "@{s2}{s68} {s8}.^")
    assert_not_contains(center_notes, "{reg0?Its villages are:Its village is}")

    assert_contains(castle_taken, "full control of the {s68}.")
    assert_contains(castle_taken, '(str_store_string, s68, "@town")')
    assert_contains(castle_taken, '(str_store_string, s68, "@castle")')
    assert_not_contains(castle_taken, "{reg2?town:castle}")

    assert_contains(cattle_stolen, '(str_store_string, s68, "@head")')
    assert_contains(cattle_stolen, '(str_store_string, s68, "@heads")')
    assert_contains(cattle_stolen, "You drive away {reg17} {s68} of cattle")
    assert_not_contains(cattle_stolen, "{reg12?heads:head}")

    assert_contains(tournament_other, "As the only {s68} to remain undefeated")
    assert_contains(tournament_other, '(str_store_string, s68, "@fighter")')
    assert_contains(tournament_other, '(str_store_string, s68, "@man")')
    assert_not_contains(tournament_other, "{reg3?fighter:man}")

    assert_contains(tax_revolt, "A large band of angry {s68} is marching nearer")
    assert_contains(tax_revolt, '(str_store_string, s68, "@peasants")')
    assert_contains(tax_revolt, '(str_store_string, s68, "@townsmen")')
    assert_not_contains(tax_revolt, "{reg9?peasants:townsmen}")

    assert_contains(game_options_3, '"{s98}"')
    assert_contains(game_options_3, "str_store_string_reg, s97, s98")
    assert_contains(game_options_3, "Troop transfers: Disabled.")
    assert_contains(game_options_3, "Adult events filter")
    assert_not_contains(game_options_3, "@{s98}")
    assert_not_contains(game_options_3, "{s1}")
    assert_not_contains(game_options_3, "Troop_transfer")
    assert_not_contains(game_options_3, "Parental Nanny")
    assert_not_contains(game_options_3, "Strategic AI Changes")

    assert_contains(reports_menu, "{playername} {s69}^Formerly of the {s68}")
    assert_contains(reports_menu, "str_store_string_reg, s97, s69")
    assert_contains(reports_menu, "Ruler of the {s70}")
    assert_not_contains(reports_menu, "{playername} {s2}^Formerly of the {s1}")
    assert_not_contains(reports_menu, "@{s2}^Ruler")
    assert_not_contains(reports_menu, "@{s2}^vassal")
    assert_not_contains(reports_menu, "@{s2}^mercenary")

    for raw in (quick_start, add_companions):
        assert_contains(raw, "{s98}")
        assert_contains(raw, "script_store_troop_name\", s68")
        assert_contains(raw, "str_store_string_reg, s69, s70")
        assert_not_contains(raw, "@{s1} (lvl")
        assert_not_contains(raw, "@{s1}^{s2}")
        assert_not_contains(raw, "@{s1} and {s2}")
        assert_not_contains(raw, "@{s1}, {s2}")
    assert_contains(add_companions, "No unjoined companions are currently available.")
    assert_contains(add_companions, "str_store_string_reg, s97, s98")

    for raw in (fief_reports, lord_reports):
        assert_contains(raw, '"{s98}"')
        assert_contains(raw, "{s68}")
        assert_contains(raw, "You owe allegiance to no realm.")
        assert_not_contains(raw, "allegience")
        assert_not_contains(raw, "of the {s1}")
        assert_not_contains(raw, '"{s1}"')
    assert_contains(fief_reports, "Estates: {s8}.")
    assert_contains(fief_reports, "Treasury awaiting collection: {reg1} denars.")
    assert_contains(fief_reports, "Mercenary Guild Halls")
    assert_contains(fief_reports, "str_store_string_reg, s97, s98")
    assert_contains(fief_reports, "str_store_string_reg, s97, s8")
    assert_not_contains(fief_reports, "@{s98}")
    assert_not_contains(fief_reports, "@{s8} and")
    assert_not_contains(fief_reports, "@{s8},")

    for raw in (construction_available, construction_current):
        assert_contains(raw, "{s98}")
        assert_contains(raw, "str_store_string_reg, s97, s98")
        assert_not_contains(raw, '"{s2}"')
        assert_not_contains(raw, 'str_store_string, s1, "@{s1}')
        assert_not_contains(raw, 'str_store_string, s2, "@{s2}')
    assert_contains(construction_available, "Every fief with available construction is already building something.")
    assert_contains(construction_available, 'str_store_string, s98, "@{s97}^^{s68} has the most advanced active project')
    assert_contains(construction_current, "No construction projects are currently underway")
    assert_contains(construction_current, 'str_store_string, s99, "@{s68}: {s69}"')

    assert_contains(pre_join, "You come across a battle between:^^{s70} and {s73}.")
    assert_contains(pre_join, "Move in to help {s70}.")
    assert_contains(pre_join, "Rush to the aid of {s73}.")
    assert_contains(pre_join, 'str_store_string, s70, "@{s68} of the {s69}"')
    assert_contains(pre_join, 'str_store_string, s73, "@{s71} of the {s72}"')
    assert_not_contains(pre_join, "{s1}")
    assert_not_contains(pre_join, "{s2}")
    assert_not_contains(pre_join, 'str_store_string, s1, "@{s1}')
    assert_not_contains(pre_join, 'str_store_string, s2, "@{s2}')

    assert_contains(join_attack, "You are helping {s73} against {s72}.")
    assert_contains(join_attack, "Your side looks {s74}; the enemy line looks {s75}.")
    assert_contains(join_attack, "(str_store_party_name, s72, \"$g_enemy_party\")")
    assert_contains(join_attack, "(str_store_party_name, s73, \"$g_ally_party\")")
    assert_not_contains(join_attack, "You are helping {s2} against {s1}")
    assert_not_contains(join_attack, "(str_store_party_name, 1,")
    assert_not_contains(join_attack, "(str_store_party_name, 2,")

    for raw in (prisoner_train, prisoner_economy):
        assert_contains(raw, '"{s98}"')
        assert_contains(raw, "str_store_string_reg, s97, s98")
        assert_not_contains(raw, '"{s9}"')
        assert_not_contains(raw, "@{s9}")
    assert_contains(prisoner_economy, "(str_clear, s98)")

    assert_contains(training_result, '"{s98}{s97}"')
    assert_contains(training_result, "str_store_string_reg, s96, s97")
    assert_contains(training_result, "str_store_troop_name_by_count, s68")
    assert_not_contains(training_result, '"{s7}{s2}"')
    assert_not_contains(training_result, "@{s2}^{reg1}")
    assert_not_contains(training_result, "@{s2}^{s1}")

    for raw in (faction_relations, guild_relations, lord_readiness):
        assert_contains(raw, '"{s98}"')
        assert_not_contains(raw, '"{s1}"')
        assert_not_contains(raw, "@{s2}^")
    assert_contains(faction_relations, "str_store_string_reg, s96, s97")
    assert_contains(faction_relations, "str_store_string_reg, s95, s96")
    assert_contains(guild_relations, "str_store_string_reg, s96, s97")
    assert_contains(guild_relations, "^{s97}")
    assert_contains(lord_readiness, "script_store_troop_name\", s68")
    assert_contains(lord_readiness, "Battle readiness report for {s68}")
    assert_not_contains(lord_readiness, "@{s2} is a prisoner")
    assert_not_contains(lord_readiness, "@{s2} has no troops")
    assert_contains(lord_fief_assignment, "script_get_prosperity_text\", s69")
    assert_contains(lord_fief_assignment, "str_store_string_reg, s95, s68")
    assert_contains(lord_fief_assignment, "script_store_troop_name\", s70")
    assert_not_contains(lord_fief_assignment, "@{s2} ({s3})")
    assert_not_contains(lord_fief_assignment, "^{s2}: {s96}")

    training_melee = read("src/menus/training/training_ground_selection_details_melee_2.py")
    training_description = read("src/menus/training/training_ground_description.py")
    peasant_training = read("src/menus/other/continue_41.py")
    permanent_damage = read("src/menus/other/s0.py")
    training_start = read("src/scripts/ZI_campaign_ai/start_training_at_training_ground.py")
    training_option = read("src/scripts/ZI_campaign_ai/cf_training_ground_sub_routine_1_for_melee_details.py")

    assert_contains(training_melee, '"training_ground_melee_1"')
    assert_contains(training_melee, '"training_ground_melee_20"')
    assert_contains(training_melee, '"{s68}"')
    assert_not_contains(training_melee, '"{s0}"')
    assert_not_contains(training_melee, '("s0"')
    assert_contains(training_description, '"{s68}"')
    assert_not_contains(training_description, '"{s0}"')
    assert_contains(training_start, '(str_store_string, s68, "@Your opponents are ready for the fight.")')
    assert_contains(training_option, '"script_store_troop_name_link", s68')
    assert_not_contains(training_option, '"script_store_troop_name_link", s0')

    assert_contains(peasant_training, '"{s68}"')
    assert_not_contains(peasant_training, '"{s0}"')
    assert_contains(permanent_damage, '"permanent_damage_accept"')
    assert_contains(permanent_damage, '"{s68}"')
    assert_not_contains(permanent_damage, '"{s0}"')


def test_dialog_and_menu_text_do_not_display_volatile_s0() -> None:
    offenders = []
    for rel in ("src/dialogs", "src/menus"):
        for path in sorted((ROOT / rel).rglob("*.py")):
            raw = path.read_text(encoding="utf-8", errors="replace")
            if "{s0}" in raw or '("s0"' in raw:
                offenders.append(path.relative_to(ROOT).as_posix())
    assert not offenders, "visible volatile s0 remains in: " + ", ".join(offenders[:20])


if __name__ == "__main__":
    test_menu_text_placeholders_are_expanded_before_display()
    test_dialog_and_menu_text_do_not_display_volatile_s0()
    print("test_menu_text_placeholder_static: OK")
