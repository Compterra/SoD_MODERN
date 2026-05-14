from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = ("src", "docs")
MISSPELLINGS = (
    "definately",
    "immidiately",
    "oders",
    "occured",
    "powerfull",
    "seperate",
    "seperately",
    "seperation",
    "seperatists",
    "suceeded",
    "towads",
)


def main():
    offenders = []
    for root_name in SOURCE_ROOTS:
        for path in sorted((ROOT / root_name).rglob("*")):
            if path.suffix not in {".py", ".md"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            for word in MISSPELLINGS:
                if word in text:
                    offenders.append(f"{path.relative_to(ROOT)} contains {word}")
    assert not offenders, "Known typo spellings remain:\n" + "\n".join(offenders)


if __name__ == "__main__":
    main()
