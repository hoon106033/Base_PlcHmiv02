import csv
import uuid

INPUT_CSV = 'CSV.csv'
OUTPUT_GVL = 'Name/GVLs/GVL_AlarmData.TcGVL'
GUID = str(uuid.uuid4())

codes = []
locations = []
messages = []

with open(INPUT_CSV, newline='', encoding='utf-8-sig') as f:
    for row in csv.reader(f):
        if len(row) >= 3:
            try:
                codes.append(int(row[0].strip()))
            except ValueError:
                continue
            locations.append(row[1].strip())
            messages.append(row[2].strip())

count = len(codes)

codes_str = ', '.join(map(str, codes))
loc_str = ', '.join(f"'{loc.replace('\\', '\\')}'" for loc in locations)
msg_str = ', '.join(f"'{msg.replace('\\', '\\')}'" for msg in messages)

gvl_content = f'''<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1">
  <GVL Name="GVL_AlarmData" Id="{GUID}">
    <Declaration><![CDATA[
VAR_GLOBAL CONSTANT
    aiAlarmCode : ARRAY[1..{count}] OF INT := [{codes_str}];
    asLocation : ARRAY[1..{count}] OF STRING(50) := [{loc_str}];
    asAlarmMessage : ARRAY[1..{count}] OF STRING(255) := [{msg_str}];
END_VAR
]]></Declaration>
  </GVL>
</TcPlcObject>
'''

with open(OUTPUT_GVL, 'w', encoding='utf-8') as f:
    f.write(gvl_content)

print(f'Generated {OUTPUT_GVL} with {count} entries.')
