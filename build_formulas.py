#!/usr/bin/env python3
"""
Generate a supplementary formulas.json with classical Shang Han Lun formula
compositions. These are from the public-domain classical text (傷寒論/金匱要略),
not proprietary. For educational reference only.
"""
import json

FORMULAS = [
    # ── 太陽病 ──
    {
        "name": "桂枝湯",
        "category": "太陽病 · 方劑組成",
        "composition": "桂枝三兩（去皮）、芍藥三兩、甘草二兩（炙）、生薑三兩（切）、大棗十二枚（擘）",
        "usage": "水煎服。服後啜熱稀粥，溫覆取微汗。",
        "indication": "太陽中風，頭痛發熱，汗出惡風，脈緩。",
        "contraindication": "酒客、吐家、裡熱盛者慎用。",
        "source": "傷寒論 · 太陽病篇"
    },
    {
        "name": "麻黃湯",
        "category": "太陽病 · 方劑組成",
        "composition": "麻黃三兩（去節）、桂枝二兩（去皮）、甘草一兩（炙）、杏仁七十個（去皮尖）",
        "usage": "先煮麻黃去上沫，再入諸藥。",
        "indication": "太陽傷寒，頭痛身疼，無汗而喘，脈浮緊。",
        "contraindication": "咽乾、淋家、瘡家、亡血家禁用。尺脈遲微者禁汗。",
        "source": "傷寒論 · 太陽病篇"
    },
    {
        "name": "葛根湯",
        "category": "太陽病 · 方劑組成",
        "composition": "葛根四兩、麻黃三兩（去節）、桂枝二兩（去皮）、芍藥二兩、甘草二兩（炙）、生薑三兩（切）、大棗十二枚（擘）",
        "usage": "先煮葛根、麻黃去沫，再入諸藥。",
        "indication": "太陽病，項背強几几，無汗惡風。",
        "contraindication": "表虛有汗者不宜。",
        "source": "傷寒論 · 太陽病篇"
    },
    {
        "name": "小青龍湯",
        "category": "太陽病 · 方劑組成",
        "composition": "麻黃三兩（去節）、芍藥三兩、細辛三兩、乾薑三兩、甘草三兩（炙）、桂枝三兩（去皮）、五味子半升、半夏半升（洗）",
        "usage": "先煮麻黃去沫。",
        "indication": "傷寒表不解，心下有水氣，乾嘔發熱而咳，或喘。",
        "contraindication": "陰虛乾咳無痰者不宜。",
        "source": "傷寒論 · 太陽病篇"
    },
    {
        "name": "大青龍湯",
        "category": "太陽病 · 方劑組成",
        "composition": "麻黃六兩（去節）、桂枝二兩（去皮）、甘草二兩（炙）、杏仁四十枚（去皮尖）、生薑三兩（切）、大棗十枚（擘）、石膏如雞子大（碎）",
        "usage": "先煮麻黃去沫，⚠️ 發汗峻劑，一服汗出即停後服。",
        "indication": "太陽中風，脈浮緊，發熱惡寒，身疼痛，不汗出而煩躁。",
        "contraindication": "⚠️ 脈微弱、汗出惡風者不可服。服之則厥逆、筋惕肉瞤。",
        "source": "傷寒論 · 太陽病篇"
    },
    {
        "name": "五苓散",
        "category": "太陽病 · 方劑組成",
        "composition": "豬苓十八銖（去皮）、澤瀉一兩六銖、白朮十八銖、茯苓十八銖、桂枝半兩（去皮）",
        "usage": "上為散，白飲和服，日三服。多飲暖水，汗出愈。",
        "indication": "太陽病，小便不利，微熱消渴，水逆。",
        "contraindication": "陰虛津虧者慎用。",
        "source": "傷寒論 · 太陽病篇"
    },

    # ── 少陽病 ──
    {
        "name": "小柴胡湯",
        "category": "少陽病 · 方劑組成",
        "composition": "柴胡半斤、黃芩三兩、人參三兩、半夏半升（洗）、甘草三兩（炙）、生薑三兩（切）、大棗十二枚（擘）",
        "usage": "去滓再煎。",
        "indication": "往來寒熱，胸脅苦滿，默默不欲飲食，心煩喜嘔。婦人熱入血室。",
        "contraindication": "單純太陽表證、陽明腑實者不宜。",
        "source": "傷寒論 · 少陽病篇"
    },
    {
        "name": "大柴胡湯",
        "category": "少陽病 · 方劑組成",
        "composition": "柴胡半斤、黃芩三兩、芍藥三兩、半夏半升（洗）、生薑五兩（切）、枳實四枚（炙）、大棗十二枚（擘）、大黃二兩",
        "usage": "去滓再煎。",
        "indication": "少陽陽明合病，往來寒熱，心下急，嘔不止，鬱鬱微煩，大便秘結。",
        "contraindication": "單純少陽無裡實者不宜。",
        "source": "傷寒論 · 少陽病篇"
    },

    # ── 陽明病 ──
    {
        "name": "白虎湯",
        "category": "陽明病 · 方劑組成",
        "composition": "知母六兩、石膏一斤（碎）、甘草二兩（炙）、粳米六合",
        "usage": "煮米熟湯成，去滓溫服。",
        "indication": "陽明經熱，大熱、大汗、大渴、脈洪大。",
        "contraindication": "表證未解、裡寒者禁用。",
        "source": "傷寒論 · 陽明病篇"
    },
    {
        "name": "白虎加人參湯",
        "category": "陽明病 · 方劑組成",
        "composition": "知母六兩、石膏一斤（碎）、甘草二兩（炙）、粳米六合、人參三兩",
        "usage": "煮米熟湯成，去滓溫服。",
        "indication": "陽明經熱，大渴，舌上乾燥，欲飲水數升。",
        "contraindication": "表不解、無大熱大渴者不宜。",
        "source": "傷寒論 · 陽明病篇"
    },
    {
        "name": "大承氣湯",
        "category": "陽明病 · 方劑組成",
        "composition": "大黃四兩（酒洗）、厚朴半斤（去皮炙）、枳實五枚（炙）、芒硝三合",
        "usage": "先煮厚朴枳實，後下大黃，去滓納芒硝。⚠️ 中病即止。",
        "indication": "陽明腑實重證，便秘、腹滿拒按、譫語、日晡潮熱。",
        "contraindication": "⚠️ 表證未解、結胸、臟結、虛寒便秘禁用。孕婦禁用。",
        "source": "傷寒論 · 陽明病篇"
    },
    {
        "name": "小承氣湯",
        "category": "陽明病 · 方劑組成",
        "composition": "大黃四兩（酒洗）、厚朴二兩（去皮炙）、枳實三枚（炙）",
        "usage": "水煎服。",
        "indication": "陽明腑實輕證，腹滿、大便硬、潮熱。",
        "contraindication": "腹不滿、不硬者不宜。",
        "source": "傷寒論 · 陽明病篇"
    },
    {
        "name": "調胃承氣湯",
        "category": "陽明病 · 方劑組成",
        "composition": "大黃四兩（酒洗）、甘草二兩（炙）、芒硝半升",
        "usage": "先煮大黃甘草，去滓納芒硝。",
        "indication": "陽明燥熱，不大便，心煩，蒸蒸發熱。",
        "contraindication": "虛寒者禁用。",
        "source": "傷寒論 · 陽明病篇"
    },
    {
        "name": "麻子仁丸",
        "category": "陽明病 · 方劑組成",
        "composition": "麻子仁二升、芍藥半斤、枳實半斤（炙）、大黃一斤（去皮）、厚朴一尺（去皮炙）、杏仁一升（去皮尖）",
        "usage": "蜜和為丸，日三服，漸加。",
        "indication": "脾約，小便數，大便硬，不更衣十日無所苦。",
        "contraindication": "虛寒便秘不宜。",
        "source": "傷寒論 · 陽明病篇"
    },

    # ── 太陰病 ──
    {
        "name": "理中湯（丸）",
        "category": "太陰病 · 方劑組成",
        "composition": "人參、乾薑、甘草（炙）、白朮各三兩",
        "usage": "水煎服或蜜丸。",
        "indication": "太陰病，自利不渴，腹滿而吐，食不下。",
        "contraindication": "實熱證不宜。",
        "source": "傷寒論 · 太陰病篇"
    },

    # ── 少陰病 ──
    {
        "name": "四逆湯",
        "category": "少陰病 · 方劑組成",
        "composition": "甘草二兩（炙）、乾薑一兩半、附子一枚（生用，去皮，破八片）",
        "usage": "水煎服。⚠️ 含生附子，必須由專業醫師處方。",
        "indication": "少陰病，四肢厥冷，下利清穀，脈微欲絕。",
        "contraindication": "⚠️ 真熱假寒禁用。必須專業醫師辨證。不可自行服用。",
        "source": "傷寒論 · 少陰病篇"
    },
    {
        "name": "真武湯",
        "category": "少陰病 · 方劑組成",
        "composition": "茯苓三兩、芍藥三兩、生薑三兩（切）、白朮二兩、附子一枚（炮，去皮，破八片）",
        "usage": "水煎服。含炮附子。",
        "indication": "少陰病，腹痛，小便不利，四肢沉重疼痛，水氣內停。",
        "contraindication": "⚠️ 陰虛津虧者慎用。含附子需醫師處方。",
        "source": "傷寒論 · 少陰病篇"
    },
    {
        "name": "黃連阿膠湯",
        "category": "少陰病 · 方劑組成",
        "composition": "黃連四兩、黃芩二兩、芍藥二兩、雞子黃二枚、阿膠三兩",
        "usage": "先煮三物去滓，納阿膠烊化，稍冷入雞子黃攪勻。",
        "indication": "少陰病，心中煩，不得臥。",
        "contraindication": "陽虛寒證不宜。",
        "source": "傷寒論 · 少陰病篇"
    },
    {
        "name": "麻黃附子細辛湯",
        "category": "少陰病 · 方劑組成",
        "composition": "麻黃二兩（去節）、細辛二兩、附子一枚（炮，去皮，破八片）",
        "usage": "先煮麻黃去沫。⚠️ 含附子+細辛。",
        "indication": "少陰病，始得之，反發熱，脈沉。",
        "contraindication": "⚠️ 脈微細下利者禁用。含附子細辛，需醫師處方。",
        "source": "傷寒論 · 少陰病篇"
    },

    # ── 厥陰病 ──
    {
        "name": "烏梅丸",
        "category": "厥陰病 · 方劑組成",
        "composition": "烏梅三百枚、細辛六兩、乾薑十兩、黃連十六兩、當歸四兩、附子六兩（炮）、蜀椒四兩、桂枝六兩、人參六兩、黃柏六兩",
        "usage": "烏梅醋浸去核，與諸藥搗篩，蜜和為丸。",
        "indication": "厥陰病，蛔厥，久利。消渴，氣上撞心，心中疼熱，飢不欲食。",
        "contraindication": "純熱證不宜。",
        "source": "傷寒論 · 厥陰病篇"
    },
    {
        "name": "當歸四逆湯",
        "category": "厥陰病 · 方劑組成",
        "composition": "當歸三兩、桂枝三兩（去皮）、芍藥三兩、細辛三兩、甘草二兩（炙）、通草二兩、大棗二十五枚（擘）",
        "usage": "水煎服。",
        "indication": "手足厥寒，脈細欲絕。凍瘡，末梢循環障礙。",
        "contraindication": "內有久寒者需加生薑附子。",
        "source": "傷寒論 · 厥陰病篇"
    },

    # ── 常用時方 ──
    {
        "name": "小建中湯",
        "category": "太陰病 · 方劑組成",
        "composition": "桂枝三兩（去皮）、甘草二兩（炙）、大棗十二枚（擘）、芍藥六兩、生薑三兩（切）、膠飴一升",
        "usage": "去滓納飴糖，微火溶化。",
        "indication": "虛勞裡急，腹中痛，心悸，手足煩熱。",
        "contraindication": "實熱腹痛不宜。",
        "source": "傷寒論 / 金匱要略"
    },
    {
        "name": "炙甘草湯",
        "category": "太陽病 · 方劑組成",
        "composition": "甘草四兩（炙）、生薑三兩（切）、人參二兩、生地黃一斤、桂枝三兩（去皮）、阿膠二兩、麥門冬半升（去心）、麻仁半升、大棗三十枚（擘）",
        "usage": "酒水合煮。阿膠烊化。",
        "indication": "脈結代，心動悸。虛勞肺痿。",
        "contraindication": "實熱證不宜。",
        "source": "傷寒論 · 太陽病篇"
    },
    {
        "name": "半夏瀉心湯",
        "category": "太陽病 · 方劑組成",
        "composition": "半夏半升（洗）、黃芩三兩、乾薑三兩、人參三兩、甘草三兩（炙）、黃連一兩、大棗十二枚（擘）",
        "usage": "水煎服。",
        "indication": "心下痞，嘔而腸鳴，下利。",
        "contraindication": "單純實熱證不宜。",
        "source": "傷寒論 · 太陽病篇"
    },

    # ── 補遺 ──
    {
        "name": "苓桂朮甘湯",
        "category": "太陽病 · 方劑組成",
        "composition": "茯苓四兩、桂枝三兩（去皮）、白朮二兩、甘草二兩（炙）",
        "usage": "水煎服。",
        "indication": "心下有痰飲，胸脅支滿，目眩。",
        "contraindication": "陰虛津虧者慎用。",
        "source": "傷寒論 / 金匱要略"
    },
    {
        "name": "芍藥甘草湯",
        "category": "太陽病 · 方劑組成",
        "composition": "芍藥四兩、甘草四兩（炙）",
        "usage": "水煎服。",
        "indication": "腳攣急，腿抽筋。",
        "contraindication": "濕盛脹滿者不宜。",
        "source": "傷寒論 · 太陽病篇"
    },
    {
        "name": "茵陳蒿湯",
        "category": "陽明病 · 方劑組成",
        "composition": "茵陳蒿六兩、梔子十四枚（擘）、大黃二兩（去皮）",
        "usage": "先煮茵陳，後入梔子大黃。",
        "indication": "陽明病，身黃如橘子色，小便不利，腹微滿。",
        "contraindication": "陰黃（寒濕發黃）不宜。",
        "source": "傷寒論 · 陽明病篇"
    },
    {
        "name": "豬苓湯",
        "category": "陽明病 · 方劑組成",
        "composition": "豬苓（去皮）、茯苓、澤瀉、阿膠、滑石（碎）各一兩",
        "usage": "先煮四味去滓，納阿膠烊化。",
        "indication": "小便不利，心煩不得眠，渴欲飲水。泌尿結石、血尿。",
        "contraindication": "陽虛水腫不宜。",
        "source": "傷寒論 · 陽明病篇"
    },
]

# Convert to searchable entries
entries = []
for f in FORMULAS:
    entry = {
        "title": f["name"],
        "category": f["category"],
        "file": "formulas-classical.json",
        "content": f"""**組成**：{f["composition"]}

**用法**：{f["usage"]}

**主治**：{f["indication"]}

**禁忌**：{f["contraindication"]}

**出處**：{f["source"]}"""
    }
    entries.append(entry)

# Save
out_path = "/srv/projects/05 倪海廈中醫查詢/formulas_classical.json"
with open(out_path, 'w') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"Generated {len(entries)} formula entries to {out_path}")
