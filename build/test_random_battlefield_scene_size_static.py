from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def test_random_battlefields_are_320_by_320() -> None:
    raw = read("compile/module_scenes.py")
    scene_ids = (
        "random_scene",
        "random_scene_steppe",
        "random_scene_plain",
        "random_scene_snow",
        "random_scene_desert",
        "random_scene_steppe_forest",
        "random_scene_plain_forest",
        "random_scene_snow_forest",
        "random_scene_desert_forest",
    )
    for scene_id in scene_ids:
        needle = f'("{scene_id}",sf_generate|sf_randomize|sf_auto_entry_points,"none", "none", (0,0),(320,320),'
        assert needle in raw, f"{scene_id} should use 320x320 generated bounds"


if __name__ == "__main__":
    test_random_battlefields_are_320_by_320()
    print("test_random_battlefield_scene_size_static: OK")
