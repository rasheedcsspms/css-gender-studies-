"""The seven topics — the single source of truth for titles, syllabus heads, colours, folders and budgets."""
from engine import style as S

TOPICS = [
    dict(n=1, roman="I", colour=S.TEAL, heads=["I", "II"], kb_words=18500,
         title="Gender Studies and the Social Construction of Gender",
         short="The Discipline & Social Construction",
         blurb="What gender is, how the discipline was born, Women's vs Gender Studies, the autonomy–integration "
               "debate, the field in Pakistan; sex and gender, constructionism, queer theory, masculinities, "
               "nature versus culture, gendered language and the transgender debate."),
    dict(n=2, roman="II", colour=S.ROSE, heads=["III"], kb_words=17500,
         title="Feminist Theories and Practice",
         short="Feminist Theories",
         blurb="What feminism is; liberal, radical, Marxist/socialist, psychoanalytic, men's and postmodern "
               "feminism; plus intersectionality, Black, postcolonial, eco- and Muslim feminisms."),
    dict(n=3, roman="III", colour=S.GOLD, heads=["IV"], kb_words=17000,
         title="Feminist Movements — the West, the United Nations and Pakistan",
         short="Feminist Movements",
         blurb="The four waves in the West, the UN conferences and CEDAW, and the women's movement in Pakistan "
               "from APWA and WAF to Aurat March and digital activism; NGO-isation."),
    dict(n=4, roman="IV", colour=S.BLUE, heads=["V"], kb_words=19000,
         title="Gender and Development",
         short="Gender and Development",
         blurb="Colonial and capitalist perspectives; modernisation, dependency, world-system and structural "
               "functionalism; WID, WAD, GAD; Moser and Kabeer; SAPs; globalisation; gender and climate."),
    dict(n=5, roman="V", colour=S.GREEN, heads=["VI"], kb_words=17000,
         title="Status of Women in Pakistan",
         short="Status of Women in Pakistan",
         blurb="Health, education, employment and law; the Constitution and pro-women laws; the Global Gender "
               "Gap; the digital divide; climate impacts; women and human rights."),
    dict(n=6, roman="VI", colour=S.CORAL, heads=["VII"], kb_words=16000,
         title="Gender and Governance",
         short="Gender and Governance",
         blurb="Defining governance; the suffrage movement; women as voters, candidates and representatives; "
               "the history and impact of political quotas in Pakistan; women in leadership."),
    dict(n=7, roman="VII", colour=S.NAVY, heads=["VIII", "IX"], kb_words=18000,
         title="Gender-Based Violence and the Three Case Studies",
         short="Gender-Based Violence & Case Studies",
         blurb="Defining GBV; theories of violence against women; structural and direct violence; forms, laws "
               "and strategies; masculinities and violence; Mukhtaran Mai, Malala Yousafzai and Sharmeen "
               "Obaid-Chinoy."),
]

SYLLABUS_HEADS = {
    "I": "Introduction to Gender Studies",
    "II": "Social Construction of Gender",
    "III": "Feminist Theories and Practice",
    "IV": "Feminist Movements",
    "V": "Gender and Development",
    "VI": "Status of Women in Pakistan",
    "VII": "Gender and Governance",
    "VIII": "Gender Based Violence",
    "IX": "Case Studies",
}


def topic(n):
    return TOPICS[n - 1]


def folder(n):
    t = topic(n)
    return f"T{n}_Topic {t['roman']} — {t['title']}"


def kb_file(n):
    return f"T{n}KB_{topic(n)['title']}.docx"


def qa_file(n):
    return f"T{n}QA_{topic(n)['title']}.docx"
