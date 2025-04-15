SYSTEM_PROMPT = """You are a professional translator. Translate the following English text into formal, professional Hebrew suitable for inclusion in a psychological assessment report, maintaining the original meaning and tone. Ensure that the Hebrew text uses formal language and preserves the original structure and intent, with changes according to the specific instructions only.
General Guidelines:
1. Preserve the page count and structure exactly as in the original text.
2. Use the following format to clearly separate pages: --- page # ---, where # is the page number.
3. Ensure that all content from a specific page in the original text remains on the same page in the translation.
4. Remove all empty rows.
5. Use bullet points (•) for lists within the table-like structures on pages 5-12
6. Do not translate MBTI type codes (e.g., ISTJ, ENFP). Keep these in their original English format.
7. when translation, take into account the specific translation instructions, and the specific page instructions.

specific translation instructions:

Extraversion: מוחצנות, Introversion: מופנמות, Sensing: חושיות
Intuition: אינטואיטיביות
Thinking: חשיבתיות
Feeling: רגשיות
Judging: שיפוטיות
Perceiving: גמישות
In-preference: בהעדפה
midzone: אזור ביניים
out-of-preference: מחוץ להעדפה
Concrete, Abstract, Realistic, Imaginative, Practical, Conceptual, Experiential, Theoretical,
Traditional, Original, Logical, Empathetic, Reasonable, Compassionate, Questioning, Accommodating,
Critical, Accepting, Tough, Tender

for page 3:
1. for the specific section, make sure to structure the line like this example:
"PCI RESULTS:
EXTRAVERSION | 11 INTUITION | 9 THINKING | 4 PERCEIVING | 11"
to:
ההעדפות שלך הן:
מוחצנות: 11 | אינטואיטיביות: 9 | חשיבתיות: 4 | גמישות: 11
make sure to enter the currect values and qualities from the original text.
make sure to translate the rest of the page as well.

For pages 5-9, structure the content as if extracted from a table. For example:

Original:
"Ways to connect with others
INITIATING–RECEIVING
midzoneWill initiate conversations in social situations
with people you already know or if your role
calls for this.
Appear at ease socially in familiar situations,
less at ease in large social gatherings.Are willing to
introduce people to each other
if no one else does so and introductions are
necessary."

Should be translated and formatted as:

"__**דרכים להתחבר עם אחרים**__
**יוזמה–קבלה** (אזור ביניים)
• יוזם שיחות במצבים חברתיים עם אנשים שאתה כבר מכיר או אם תפקידך דורש זאת.
• נראה בנוח חברתית במצבים מוכרים, פחות בנוח באירועים חברתיים גדולים.
• מוכן להציג אנשים זה לזה אם אף אחד אחר לא עושה זאת והצגות נחוצות."

for pages 9,11,12 format each quality to be like this:
"**quality** (preference, if applicable):
• {table 2nd title} style: {line content}
" enhancing your style: {line content}"


Your primary goal is to produce a well-structured, accurately translated document that strictly adheres to the original
page layout and content separation, while ensuring that MBTI-related terms are translated with their English equivalents in parentheses."""

MBTI_TYPES = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]
MBTI_QUALITIES = [
    "Extraversion", "Introversion",
    "Sensing", "Intuition",
    "Thinking", "Feeling",
    "Judging", "Perceiving"
]

MBTI_QUALITIES_HEBREW = {
    "Extraversion": "מוחצנות",
    "Introversion": "מופנמות",
    "Sensing": "חושיות",
    "Intuition": "אינטואיטיביות",
    "Thinking": "חשיבתיות",
    "Feeling": "רגשיות",
    "Judging": "מתוכנן.ת",
    "Perceiving": "גמישות"
}

MBTI_QUALITIES_FORMATTED = {
    "Extraversion": "Extraversion (מוחצנות)",
    "Introversion": "Introversion (מופנמות)",
    "Sensing": "Sensing (חושיות)",
    "Intuition": "Intuition (אינטואיטיביות)",
    "Thinking": "Thinking (חשיבתיות)",
    "Feeling": "Feeling (רגשיות)",
    "Judging": "Judging (מתוכנן.ת)",
    "Perceiving": "Perceiving (גמישות)"
}

MBTI_TYPE_QUALITIES = {
    "ISTJ": ["Introversion", "Sensing", "Thinking", "Judging"],
    "ISFJ": ["Introversion", "Sensing", "Feeling", "Judging"],
    "INFJ": ["Introversion", "Intuition", "Feeling", "Judging"],
    "INTJ": ["Introversion", "Intuition", "Thinking", "Judging"],
    "ISTP": ["Introversion", "Sensing", "Thinking", "Perceiving"],
    "ISFP": ["Introversion", "Sensing", "Feeling", "Perceiving"],
    "INFP": ["Introversion", "Intuition", "Feeling", "Perceiving"],
    "INTP": ["Introversion", "Intuition", "Thinking", "Perceiving"],
    "ESTP": ["Extraversion", "Sensing", "Thinking", "Perceiving"],
    "ESFP": ["Extraversion", "Sensing", "Feeling", "Perceiving"],
    "ENFP": ["Extraversion", "Intuition", "Feeling", "Perceiving"],
    "ENTP": ["Extraversion", "Intuition", "Thinking", "Perceiving"],
    "ESTJ": ["Extraversion", "Sensing", "Thinking", "Judging"],
    "ESFJ": ["Extraversion", "Sensing", "Feeling", "Judging"],
    "ENFJ": ["Extraversion", "Intuition", "Feeling", "Judging"],
    "ENTJ": ["Extraversion", "Intuition", "Thinking", "Judging"]
}


def fixed_text_data(mbti_info, mbti_type_qualities):
    fixed_text_const = {
        1: {5: """תרגום החוברת מבוצע בין השאר (אך לא רק) על ידי מערכות בינה מלאכותית (AI), ולכן התרגום עלול להיות לא מדויק.\n 
באחריות המשתמש להשתמש בו בצמוד לחוברת הפרשנות המקורית והרשמית (MYER-BRIGGS TYPE INDICATOR™).\n
השימוש בתרגום לצרכים אישיים בלבד ועל אחריות הקורא.
        """},
        2: {1: """דוח הפרשנות שלך הוא תיאור מעמיק ומותאם אישית של העדפות האישיות שלך, הנגזרות מתשובותיך בשאלון שמילאת.
הוא כולל את תוצאות שלב 1 שלך ואת הטיפוס שלך בארבע אותיות, יחד עם תוצאות שלב 2 שלך,המראות כמה מהדרכים הייחודיות שבהן אתה מבטא את הטיפוס שלך בשלב 1.\n
הערכת כלי ה-MBTI פותחה על ידי איזבל מאיירס וקתרין בריגס כיישום של תיאוריית טיפוסי האישיות של קרל יונג. תיאוריה זו מדברת על כך שיש לנו דרכים מנוגדות לכוון ולקבל אנרגיה (מוחצנות או מופנמות), לקלוט מידע (חושים או אינטואיציה), להחליט או להגיע למסקנות לגבי מידע זה (לוגיקה או הסכמה), ולגשת לעולם החיצון (מנוהל או מתנהל)."""},
        3: {1: f"טיפוס האישיות שלך כפי שדווח: {mbti_info['type']}",
            # 2: f"**__ההעדפות שלך הן__\n{format_mbti_string}**",
            6: "DELETE",
            5: "DELETE"},
        4: {1: """__**תוצאות שלב 2 שלך**__
הערכת MBTI Step II מסבירה חלק מהמורכבות של האישיות שלך על ידי הצגת התוצאות שלך בחמישה חלקים שונים, או ׳פנים׳, עבור כל אחד מזוגות ההעדפות של שלב 1.
התעמקות בתוצאות שלך ב-20 הפנים הללו יכולה לעזור לך להבין טוב יותר את הדרך הייחודית שלך לחוות ולבטא את הטיפוס שלך.
__**עובדות על 20 הפנים**__
• חמשת הפנים בתוך העדפה אינן מכסות או מסבירות את המשמעות המלאה של ההעדפה. 
• לכל פן יש נושא, כגון "דרכים להתחבר עם אחרים". 
• לכל פן יש שני קטבים מנוגדים (למשל, יוזם ומקבל). 
• הפנים מקבלות ניקוד שונה מההעדפות, ולכן חמשת ציוני הפנים שלך אינם מסתכמים לציון ההעדפה של שלב 1 שלך. 
כל פן יכול להופיע ב-3 אופנים:
o	**״בתוך ההעדפה״** – כלומר שייך להעדפה של שלב 1
o	**״אזור ביניים״** – כלומר בין שני הקטבים של שלב 1
o	**״מחוץ להעדפה״** – כלומר שייך לקוטב ההפוך מהתוצאה של שלב 1"""
            },
        5: {1: f"""**1. ממה אתה מקבל אנרגיה?**\n{mbti_type_qualities[0]}"""},
        6: {1: f"""**2. כיצד את.ה קולט.ת מידע?**\n{mbti_type_qualities[1]}"""},
        7: {1: f"""**3. באיזה אופן את.ה מקבל.ת החלטות**\n{mbti_type_qualities[2]}"""},
        8: {1: f"""**4. איך את.ה מתנהל.ת בעולם**\n{mbti_type_qualities[3]}"""},
        9: {3: """כל ההיבטים של הטיפוס שלך משפיעים על האופן שבו אתה מתקשר, במיוחד כחלק מצוות. תשעה מה׳פנים׳ רלוונטיים במיוחד לתקשורת. ההעדפות שלך לתשעת הפנים הללו יחד עם טיפים לתקשורת טובה יותר מופיעים להלן.
בנוסף לטיפים שלהלן, זכור שתקשורת עבור כל טיפוס כוללת:
1.	לספר לאחרים איזה סוג מידע אתה צריך.
2.	לשאול אחרים מה הם צריכים.
3.	לפקח על חוסר הסבלנות שלך כאשר סגנונות אחרים שולטים.
4.	להבין שאחרים כנראה לא מנסים להרגיז אותך כשהם משתמשים בסגנונות התקשורת שלהם."""
            },
        10: {1: """__**יישום תוצאות שלב II™ לקבלת החלטות**__
קבלת החלטות יעילה דורשת איסוף מידע ממגוון נקודות מבט ויישום שיטות שונות להערכת מידע זה. ידע על פני שלב 2 נותן לנו דרכים ספציפיות לשפר את קבלת ההחלטות שלנו, במיוחד את ה׳פנים׳ הקשורות לחושים, אינטואיציה, חשיבה ורגש. להלן שאלות כלליות הקשורות לפנים אלה. קטבי הפנים שאתה מעדיף נמצאים בכתב נטוי כחול. אם אתה באזור הביניים, אף קוטב לא מודגש.""",
             2: """חישה (SENSING) / אינטואיציה (INTUITION)\n\nקונקרטי (Concrete):\nמה אנחנו יודעים? איך אנחנו יודעים את זה?\n\n
אבסטרקטי (Abstract):\nמה עוד זה יכול להביע?\n\nראליסטי (Realistic):\nמהם העלויות האמיתיות?\n\nבעל דמיון (Imaginative):
מה עוד אפשר להמציא?\n\nמעשי (Practical):\nהאם זה יעבוד?\n\nרעיוני (Conceptual):\nאילו רעיונות מעניינים נוספים קיימים?\n
התנסותי (Experiential):\nאתה יכול להראות לי איך זה עובד?\n\nתאורטי (Theoretical):\nאיך הכול מחובר זה לזה?\n
שמרני (Traditional):\nהאם באמת צריך לשנות משהו?\n\nמקורי (Original):\nמהי דרך חדשה לעשות את זה?\n
חשיבה (THINKING) / רגש (FEELING)\n\nהגיוני (Logical):\nמה היתרונות והחסרונות?\n\nאמפתי (Empathetic):
מה אנחנו אוהבים או לא אוהבים בזה?\n\nרציונלי (Reasonable):\nמה ההשלכות הלוגיות?\n\nבעל חמלה (Compassionate):
איך זה ישפיע על אנשים?\n\nמטיל ספק (Questioning):\nאבל מה לגבי…?\n\nמסתגל (Accommodating):\nאיך נוכל לשמח את כולם?\n
ראייה ביקורתית (Critical):\nמה לא בסדר בזה?\n\nקבלה (Accepting):\nמה טוב בזה?\n\nקשוח (Tough):
למה אנחנו לא ממשיכים עם זה עכשיו?\n\nעדין (Tender):\nמה עם האנשים שעלולים להיפגע?\n
""",
             28: """ טיפים:
בפתרון בעיות אישיות, התחל בשאילת כל השאלות מלמעלה.
שימו לב היטב לתשובות. השאלות שכן מנוגדות לאלה המופיעות באותיות כחולות עשויות להיות מפתח מכיוון שהם מייצגות נקודות מבט שאינך צפוי לשקול.
נסו לאזן את סגנון קבלת ההחלטות שלכם על ידי התחשבות בחלקים פחות מועדפים באישיות שלכם.
בפתרון בעיות בקבוצה, חפשו באופן פעיל אנשים עם נקודות מבט שונות משלכם. בקשו את הלבטים ונקודות המבט שלהם.
לאחר קבלת ההחלטה בצעו בדיקה אחרונה כדי לוודא שכל השאלות למעלה נשאלו וכי סגנונות קבלת החלטות שונים נכללו בתהליך.
אם חסרה לכם פרספקטיבה, עשו מאמצים נוספים לשקול מה זה עשוי להוסיף."""
             },
        11: {3: """נראה ששינוי הוא בלתי נמנע ומשפיע על אנשים בדרכים שונות. כדי לעזור לך להתמודד עם שינוי:
•	היה ברור לגבי מה משתנה ומה נשאר זהה.
•	זהה את מה שאתה צריך לדעת כדי להבין את השינוי ולאחר מכן חפש את המידע הזה.
•	כדי לעזור לאחרים להתמודד עם שינוי, עודד דיון פתוח על השינוי; היה מודע לכך שזה קל יותר לחלק מהמעורבים.
•	ודא שנשקלו גם סיבות לוגיות וגם ערכים אישיים או חברתיים.
טיפוס האישיות שלך משפיע גם על סגנון ניהול השינויים שלך, במיוחד התוצאות שלך בתשעת ה׳פנים׳ שלהלן. סקור את הפנים והטיפים לשיפור התגובה שלך לשינוי."""},
        12: {3: """קונפליקטים הם בלתי נמנעים בעבודה עם אחרים. אנשים עם טיפוסי אישיות מובהקים עשויים להיות שונים במה שהם מגדירים כקונפליקט, כיצד הם מגיבים אליו וכיצד הם מגיעים לפתרון. למרות שלפעמים הם לא נעימים, קונפליקטים מובילים לעתים קרובות למצבי עבודה משופרים וליחסים משופרים.
חלק מניהול קונפליקטים עבור כל טיפוס כולל:
•	דאגה להשלמת העבודה תוך שמירה על מערכות היחסים שלך עם האנשים המעורבים.
•	הכרה שלכל נקודת מבט יש מה להוסיף, אך כל נקודת מבט המופיעה בצורה קיצונית תפריע בסופו של דבר לפתרון קונפליקטים.
הטבלה שלהלן מסבירה כיצד התוצאות שלך בשישת ה׳פנים׳ של שלב 2 עשויות להשפיע על המאמצים שלך לנהל קונפליקטים.
        """},
        13: {3: """מהות הטיפוס כרוכה באופן שבו אנשים קולטים מידע (חושים או אינטואיציה) וכיצד הם מקבלים החלטות (חשיבה או רגש). לכל טיפוס יש דרך מועדפת לעשות את שני הדברים האלה. שתי האותיות האמצעיות של הטיפוס שלך בארבע אותיות (S או N ו-T או F) מראות את התהליכים המועדפים עליך. ההפכים שלהם, שהאותיות שלהם לא מופיעות בטיפוס שלך בארבע אותיות, הם שלישיים ורביעיים בחשיבותם עבור הטיפוס שלך. זכור - אתה משתמש בכל חלקי האישיות שלך לפחות חלק מהזמן.
שימוש בתהליכים המועדפים עליך
אנשים שמעדיפים מוחצנות אוהבים להשתמש בתהליך המועדף עליהם בעיקר בעולם החיצון של אנשים ודברים. לאיזון, הם משתמשים בתהליך השני שלהם בעולם הפנימי שלהם של רעיונות ורשמים. אנשים שמעדיפים מופנמות נוטים להשתמש בתהליך המועדף עליהם בעיקר בעולם הפנימי שלהם ולאזן זאת עם השימוש בתהליך השני שלהם בעולם החיצון."""}
    }
    return fixed_text_const


lines_to_remove = {
    0: [0, 1, 2, 3, 4, 5, 6, 7, 10, 11],
    1: "ALL",  # Skip entire page
    2: [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
        37, 38, 39, 40, 41],
    3: "ALL",
    4: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
        27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    5: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
        27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    6: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
        27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
    7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
        27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
    8: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
    9: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 37,
        38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
    10: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    11: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    12: [0, 1, 2, 4, 5, 6, 7, 8, 27, 28, 29, 30, 31],
    13: [0, 1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    14: "ALL",
    15: [0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
    16: [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
         29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
         60, 61, 62, 63, 64, 65, 66]
}
