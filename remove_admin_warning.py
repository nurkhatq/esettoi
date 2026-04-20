import re

filepath = 'd:/toi/esettoi/src/app/admin/page.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I will use a regex to aggressively remove the warning block.
# Usually it's within a <p> or <div> block.
# I'll search for 'Назар аударыңыз' and remove its containing tag.

# The exact text has '(Vercel)' and 'data.csv'. Let's find the p tag or div tag that contains this.
new_content = re.sub(r'<p[^>]*>.*?Назар аударыңыз.*?Vercel.*?түсіп отырады!.*?</p>', '', content, flags=re.DOTALL)
new_content = re.sub(r'<div[^>]*>.*?Назар аударыңыз.*?Vercel.*?түсіп отырады!.*?</div>', '', new_content, flags=re.DOTALL)

# Just in case it's in a slightly different format
new_content = re.sub(r'Назар аударыңыз \(Vercel\): Бұл жазбалар уақытша файлда \(data\.csv\) сақталады\. Vercel сервері ұйықтағанда бұл файл өшіп қалуы мүмкін\. Тізім Телеграмға міндетті түрде түсіп отырады!', '', new_content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Removed warning text.')
