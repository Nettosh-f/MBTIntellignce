import re
from utils import get_all_info, extract_mbti_qualities_scores


def format_mbti_string(mbti_page3):
    formatted_items = [f"{quality} : {score}" for quality, score in mbti_page3.items()]
    return " | ".join(formatted_items)


def insert_fixed_text(input_file, output_file, page_line_text_map):
    """
    Insert fixed text into specified lines on each page of a document,
    or delete lines if the value contains "DELETE".

    Parameters:
    ----------
    input_file : str
        Path to the input text file
    output_file : str
        Path to the output text file
    page_line_text_map : dict
        Dictionary where:
        - Keys are page numbers (int)
        - Values are dictionaries with:
            - Keys: line numbers within that page (int, 1-based index)
            - Values: text to insert at that line (str)
                      or "DELETE" to remove the line

    Example:
    -------
    page_line_text_map = {
        1: {3: "Header text for page 1", 10: "DELETE"},  # Insert text after line 3, delete line 10
        2: {5: "Some fixed text for page 2"}
    }
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_page = 0
    line_count_in_page = 0
    result_lines = []

    # Lines marked for deletion (tuples of page, line)
    lines_to_delete = []

    # First, identify all lines to delete
    for page, line_dict in page_line_text_map.items():
        for line_num, text in line_dict.items():
            if isinstance(text, str) and "DELETE" in text:
                lines_to_delete.append((page, line_num))

    for line in lines:
        # Check if this is a page delimiter line
        if line.strip().startswith('--- Page ') and line.strip().endswith('---'):
            # Extract the page number
            try:
                page_str = line.strip().replace('--- Page ', '').replace(' ---', '')
                current_page = int(page_str)
                # Reset line count for the new page
                line_count_in_page = 0
            except ValueError:
                # If we can't parse the page number, just continue
                pass

            # Add the page delimiter line to results
            result_lines.append(line)
            line_count_in_page += 1

        else:
            # Check if the current line should be deleted
            if (current_page, line_count_in_page) in lines_to_delete:
                print(f"Deleted line at Page {current_page}, Line {line_count_in_page}: {line.strip()[:30]}...")
                line_count_in_page += 1
                continue

            # For non-page delimiter lines, add them if not marked for deletion
            result_lines.append(line)
            line_count_in_page += 1

        # Check if we need to insert fixed text after this line
        if current_page in page_line_text_map and line_count_in_page - 1 in page_line_text_map[current_page]:
            text_to_insert = page_line_text_map[current_page][line_count_in_page - 1]

            # Only insert if not a DELETE command
            if not (isinstance(text_to_insert, str) and "DELETE" in text_to_insert):
                result_lines.append(text_to_insert + '\n')
                print(f"Inserted text at Page {current_page}, Line {line_count_in_page - 1}: {text_to_insert[:30]}...")

    # Write the modified content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(result_lines)

    print(f"Successfully processed the file. Output saved to {output_file}")


# Example usage
if __name__ == "__main__":
    # Load MBTI information
    mbti_info = get_all_info(r"F:\projects\MBTInteligence\MBTItranslated\asaf-solomon-267149-4ae2ac9c-005e-ef11-bdfd-6045bd04b01a-cleaned-hebrew.txt")
    mbti_page3 = extract_mbti_qualities_scores(
        r"F:\projects\MBTInteligence\MBTItranslated\asaf-solomon-267149-4ae2ac9c-005e-ef11-bdfd-6045bd04b01a-cleaned-hebrew.txt")

    # Example configuration with both insertions and deletions
    page_line_text_map = {
        2: {1: """דוח הפרשנות שלך הוא תיאור מעמיק ומותאם אישית של העדפות האישיות שלך, הנגזרות מתשובותיך בשאלון שמילאת.
הוא כולל את תוצאות שלב 1 שלך ואת הטיפוס שלך בארבע אותיות, יחד עם תוצאות שלב 2 שלך,המראות כמה מהדרכים הייחודיות שבהן אתה מבטא את הטיפוס שלך בשלב 1.\n
הערכת כלי ה-MBTI פותחה על ידי איזבל מאיירס וקתרין בריגס
כיישום של תיאוריית טיפוסי האישיות של קרל יונג. תיאוריה זו מדברת על כך שיש לנו דרכים מנוגדות לכוון ולקבל
אנרגיה  (מוחצנות או מופנמות), לקלוט מידע (חושים או אינטואיציה), להחליט או להגיע למסקנות לגבי מידע זה
(לוגיקה או הסכמה), ולגשת לעולם החיצון (מנוהל או מתנהל)."""},
        3: {
            1: f"טיפוס האישיות שלך כפי שדווח: {mbti_info['MBTI Type']}",
            2: f"ההעדפות שלך הן\n{format_mbti_string(mbti_page3)}",
            6: "DELETE",
            5: "DELETE"}
#             4: """האם הטיפוס הזה מתאים לך?\n שים לב לחלקים בתיאור הקודם שמתאימים לך ולכל חלק שלא. תוצאות שלב 2 שלך
# בעמודים הבאים עשויות לעזור להבהיר כל תחום שלא מתאר אותך היטב. אם טיפוס שלב 1 שדיווחת עליו אינו מתאים,
# תוצאות שלב 2 שלך עשויות לעזור להציע טיפוס אחר שמדויק יותר עבורך."""}
        ,
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

    insert_fixed_text(
        input_file=r"F:\projects\MBTInteligence\MBTItranslated\asaf-solomon-267149-4ae2ac9c-005e-ef11-bdfd-6045bd04b01a-cleaned-hebrew.txt",
        output_file=r"F:\projects\MBTInteligence\MBTItranslated\asaf-solomon-MBTI-fixed.txt",
        page_line_text_map=page_line_text_map
    )
