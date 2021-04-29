# Process raw item file into a yaml document for loading
import dataclasses
import yaml

slots = yaml.load(open('slots.yaml'))

slot_map = {}

for slot in slots:
    slot_no = slot['pk']
    slot_name = slot['fields']['name']
    slot_map[slot_name] = slot_no

dungeons = yaml.load(open('dungeons.yaml'))

dungeon_map = {}

for dungeon in dungeons:
    dungeon_no = dungeon['pk']
    dungeon_name = dungeon['fields']['name']
    dungeon_map[dungeon_name] = dungeon_no

@dataclasses.dataclass
class Item:
    item_id: int
    name: str
    slot: int
    dropped_by: str
    wowhead_link: str
    icon_link:str

@dataclasses.dataclass
class Boss:
    name: str
    dungeon: int
    id_no: int


items = []
bosses = {}
boss_id = 1


with open('items_raw.txt', 'r') as f_item:
    while True:
        _ = f_item.readline()
        line = f_item.readline()
        if line == '@@@':
            break

        slot = f_item.readline().strip()
        wowhead_link = f_item.readline().strip()
        icon_link = f_item.readline().strip()
        name = f_item.readline().strip()
        dropped_by = f_item.readline().strip()
        if dropped_by not in bosses:
            bosses[dropped_by] = Boss(dropped_by, 3457, boss_id)
            boss_id += 1
        try:
            item_id = int(wowhead_link.split('=')[1].split('/')[0])
        except IndexError:
            print('slot:', slot)
            print('wowhead_link:', wowhead_link)
            raise
        items.append(Item(item_id, name, slot, dropped_by, wowhead_link, icon_link))


with open('karazhan_items.yaml', 'w') as out_item:
    out_item.write('---\n')
    for item in items:
        out_item.write('- model: dashboard.Item\n')
        out_item.write(f'  pk: {item.item_id}\n')
        out_item.write('  fields:\n')
        out_item.write(f'    slot: {slot_map[item.slot]}\n')
        out_item.write(f'    wowhead_link: "{item.wowhead_link}"\n')
        out_item.write(f'    icon_link: "{item.icon_link}"\n')
        out_item.write(f'    name: "{item.name}"\n')
        out_item.write(f'    dropped_by: {bosses[item.dropped_by].id_no}\n')

with open('karazhan_bosses.yaml', 'w') as out_item:
    out_item.write('---\n')
    for item in bosses.values():
        out_item.write('- model: dashboard.Boss\n')
        out_item.write(f'  pk: {item.id_no}\n')
        out_item.write('  fields:\n')
        out_item.write(f'    name: "{item.name}"\n')
        out_item.write(f'    dungeon: 3457\n')
'''
Cloak
"https://tbc.wowhead.com/item=28570/shadow-cloak-of-dalaran"
"https://wow.zamimg.com/images/wow/icons/tiny/inv_misc_cape_20.gif"
Shadow-Cloak of Dalaran
Moroes
'''
'''
- model: dashboard.Item
  pk: 28529
  fields:
    slot: Cloak
    wowhead_link: "https://tbc.wowhead.com/item=28529/royal-cloak-of-arathi-kings"
    icon_link: "https://wow.zamimg.com/images/wow/icons/tiny/inv_misc_cape_10.gif"
    name: Royal Cloak of Arathi Kings
    dropped_by: Moroes
'''