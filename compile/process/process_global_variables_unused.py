from module_info import *
from process_common import *
from process_operations import *
from pathlib import Path


print("Checking global variable usages...")
root_dir = Path(__file__).resolve().parents[2]
allowlist_path = root_dir / "docs" / "edit" / "global_variables_unused_allowlist.txt"
report_path = root_dir / "docs" / "reports" / "global_variables_unused_report.txt"
unused_allowlist = {}
if allowlist_path.exists():
  for line in allowlist_path.read_text(encoding="utf-8", errors="replace").splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
      if "#" in line:
        name, reason = line.split("#", 1)
        name = name.strip()
        reason = reason.strip()
      else:
        name = line
        reason = ""
      if name:
        unused_allowlist[name.lower()] = reason
variable_uses = []
variables = load_variables(export_dir,variable_uses)
known_variables = set([v.lower() for v in variables])
unused_globals = []
preserved_globals = []
i = 0
while (i < len(variables)):
  if i < len(variable_uses) and variable_uses[i] == 0:
    variable_name = variables[i]
    allow_reason = unused_allowlist.get(variable_name.lower(), None)
    if allow_reason is None:
      unused_globals.append(variable_name)
      print("WARNING: Global variable never used: " + variable_name)
    else:
      preserved_globals.append((variable_name, allow_reason))
  i = i + 1

stale_allowlist = []
for variable_name in sorted(unused_allowlist.keys()):
  if variable_name not in known_variables:
    stale_allowlist.append(variable_name)
    print("WARNING: Unused global allowlist entry does not exist: " + variable_name)

report_path.parent.mkdir(parents=True, exist_ok=True)
with report_path.open("w", encoding="utf-8") as report:
  report.write("Global Variables Unused Report\n")
  report.write("\n")
  report.write("Outcome: %d warning(s)\n" % (len(unused_globals) + len(stale_allowlist)))
  report.write("Unused globals: %d\n" % len(unused_globals))
  report.write("Preserved compatibility globals: %d\n" % len(preserved_globals))
  report.write("Stale allowlist entries: %d\n" % len(stale_allowlist))
  report.write("\n")
  report.write("Unused Globals\n")
  if unused_globals:
    for variable_name in unused_globals:
      report.write("- %s\n" % variable_name)
  else:
    report.write("- None\n")
  report.write("\n")
  report.write("Preserved Compatibility Globals\n")
  if preserved_globals:
    for variable_name, reason in preserved_globals:
      if reason:
        report.write("- %s: %s\n" % (variable_name, reason))
      else:
        report.write("- %s\n" % variable_name)
  else:
    report.write("- None\n")
  report.write("\n")
  report.write("Stale Allowlist Entries\n")
  if stale_allowlist:
    for variable_name in stale_allowlist:
      report.write("- %s\n" % variable_name)
  else:
    report.write("- None\n")
