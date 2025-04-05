SYSTEM_PROMPT = """You are a professional translator. Translate the following English text into formal, professional 
Hebrew suitable for inclusion in a psychological assessment report, maintaining the original meaning and tone. Ensure 
that the Hebrew text uses formal language and preserves the original structure and intent. Preserve the page count by 
using the following format: --- page # ---, where # is the page number. in pages 5-10, the page structure should be 
as if the text was extracted from a table, for example : \"Ways to connect with others \nINITIATING–RECEIVING  
\nmidzoneWill initiate conversations in social situations \nwith people you already know or if your role \ncalls for 
this.\nAppear at ease socially in familiar situations, \nless at ease in large social gatherings.Are willing to 
introduce people to each other \nif no one else does so and introductions are \nnecessary.\"\nwould be: \"\nWays to 
connect with others \nINITIATING–RECEIVING \nmidzone\nWill initiate conversations in social situations with people 
you already know or if your role calls for this.\nAppear at ease socially in familiar situations, less at ease in 
large social gatherings.\nAre willing to introduce people to each other if no one else does so and introductions are 
necessary.\"\n remove all empty rows, keep the seperation to pages as '--- page {number} ---' make sure to translate
extroversion and introversion into 'מוחצנות' and 'מופנמות' respectively.
 """
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
    "Sensing": "חישה",
    "Intuition": "אינטואיציה",
    "Thinking": "חשיבה",
    "Feeling": "רגש",
    "Judging": "שיפוטיות",
    "Perceiving": "הסתגלות"
}
# Mapping of MBTI types to their qualities
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


def fixed_text(mbti_info, format_mbti_string):
    fixed_text_const = {
        2: {1: """דוח הפרשנות שלך הוא תיאור מעמיק ומותאם אישית של העדפות האישיות שלך, הנגזרות מתשובותיך בשאלון שמילאת.
                הוא כולל את תוצאות שלב 1 שלך ואת הטיפוס שלך בארבע אותיות, יחד עם תוצאות שלב 2 שלך,המראות כמה מהדרכים הייחודיות שבהן אתה מבטא את הטיפוס שלך בשלב 1.\n
                הערכת כלי ה-MBTI פותחה על ידי איזבל מאיירס וקתרין בריגס
                כיישום של תיאוריית טיפוסי האישיות של קרל יונג. תיאוריה זו מדברת על כך שיש לנו דרכים מנוגדות לכוון ולקבל
                אנרגיה  (מוחצנות או מופנמות), לקלוט מידע (חושים או אינטואיציה), להחליט או להגיע למסקנות לגבי מידע זה
                (לוגיקה או הסכמה), ולגשת לעולם החיצון (מנוהל או מתנהל)."""},
        3: {
            1: f"טיפוס האישיות שלך כפי שדווח: {mbti_info['type']}",
            2: f"ההעדפות שלך הן\n{format_mbti_string(mbti_page3)}",
            6: "DELETE",
            5: "DELETE"
        },
        4: {1: """תוצאות שלב 2 שלך
                הערכת MBTI Step II מסבירה חלק מהמורכבות של האישיות שלך על ידי הצגת התוצאות שלך בחמישה חלקים שונים, או ׳פנים׳, עבור כל אחד מזוגות ההעדפות של שלב 1.
                התעמקות בתוצאות שלך ב-20 הפנים הללו יכולה לעזור לך להבין טוב יותר את הדרך הייחודית שלך לחוות ולבטא את הטיפוס שלך.
                עובדות על 20 הפנים
                •	חמשת הפנים בתוך העדפה אינן מכסות או מסבירות את המשמעות המלאה של ההעדפה.
                •	לכל פן יש נושא, כגון "דרכים להתחבר עם אחרים".
                •	לכל פן יש שני קטבים מנוגדים (למשל, יוזם ומקבל).
                •	הפנים מקבלות ניקוד שונה מההעדפות, ולכן חמשת ציוני הפנים שלך אינם מסתכמים לציון ההעדפה של שלב 1 שלך.
                •	כל פן יכול להופיע ב-3 אופנים:
                o	״בתוך ההעדפה״ – כלומר שייך להעדפה של שלב 1
                o	״אזור ביניים״ – כלומר בין שני הקטבים של שלב 1
                o	״מחוץ לההעדפה״ – כלומר שייך לקוטב ההפוך מהתוצאה של שלב 1"""
            },
        5: {1: """1. ממה אתה מקבל אנרגיה?
                EXTROVERSION (מוחצנות) / INTROVERSION (מופנמות)"""
            },
        6: {1: """2. כיצד את.ה קולט.ת מידע?
                SENSOR(חושים) / INTUITION (אינטואיציה)"""
            },
        7: {1: """3. באיזה אופן את.ה מקבל.ת החלטות
                THINKING (חשיבה) / FILEENG (הסכמה/רגש)"""
            },
        8: {1: """4. איך את.ה מתנהל.ת בעולם
                JUDJING (מתוכנן) / PERCEIVING (מתנהל)"""
            },
        9: {2: """כל ההיבטים של הטיפוס שלך משפיעים על האופן שבו אתה מתקשר, במיוחד כחלק מצוות. תשעה מה׳פנים׳ רלוונטיים במיוחד לתקשורת. ההעדפות שלך לתשעת הפנים הללו יחד עם טיפים לתקשורת טובה יותר מופיעים להלן.
                בנוסף לטיפים שלהלן, זכור שתקשורת עבור כל טיפוס כוללת:
                a.	לספר לאחרים איזה סוג מידע אתה צריך.
                b.	לשאול אחרים מה הם צריכים.
                c.	לפקח על חוסר הסבלנות שלך כאשר סגנונות אחרים שולטים.
                d.	להבין שאחרים כנראה לא מנסים להרגיז אותך כשהם משתמשים בסגנונות התקשורת שלהם."""
            },
        10: {1: """יישום תוצאות שלב 2 לקבלת החלטות
                קבלת החלטות יעילה דורשת איסוף מידע ממגוון נקודות מבט ויישום שיטות שונות להערכת מידע זה. ידע על פני שלב 2 נותן לנו דרכים ספציפיות לשפר את קבלת ההחלטות שלנו, במיוחד את ה׳פנים׳ הקשורות לחושים, אינטואיציה, חשיבה ורגש. להלן שאלות כלליות הקשורות לפנים אלה. קטבי הפנים שאתה מעדיף נמצאים בכתב נטוי כחול. אם אתה באזור הביניים, אף קוטב לא מודגש.""",
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
                אנשים שמעדיפים מוחצנות אוהבים להשתמש בתהליך המועדף עליהם בעיקר בעולם החיצון של אנשים ודברים. לאיזון, הם משתמשים בתהליך השני שלהם בעולם הפנימי שלהם של רעיונות ורשמים. אנשים שמעדיפים מופנמות נוטים להשתמש בתהליך המועדף עליהם בעיקר בעולם הפנימי שלהם ולאזן זאת עם השימוש בתהליך השני שלהם בעולם החיצון.
                        """}
    }
    return fixed_text_const
