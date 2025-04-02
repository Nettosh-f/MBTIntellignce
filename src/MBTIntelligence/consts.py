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