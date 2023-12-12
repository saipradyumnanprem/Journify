import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

emotionss = ['fear', 'neutral',
             'happiness', 'sadness', 'anger', 'surprise']

anger_keywords = ['anger', 'irritation', 'rage', 'outrage', 'frustration', 'resentment', 'fury', 'hostility', 'indignation', 'annoyance',
                  'agitation', 'exasperation', 'bitterness', 'enrage', 'livid', 'mad', 'fuming', 'temper', 'wrath', 'upset',
                  'offended', 'incensed', 'infuriated', 'provoked', 'irate', 'pissed off', 'cross', 'aggressive', 'irate', 'outraged',
                  'vexation', 'displeasure', 'disgruntled', 'irascible', 'disgusted', 'mad as hell', 'boiling', 'storming', 'furious',
                  'impatience', 'resentful', 'livid', 'irate', 'frustrated', 'fume', 'steam', 'pissed']


fear_keywords = ['fear', 'anxiety', 'apprehension', 'dread', 'terror', 'panic', 'phobia', 'alarm', 'fright', 'horror',
                 'uneasiness', 'worry', 'nervousness', 'trepidation', 'intimidation', 'dismay', 'consternation', 'overwhelmed',
                 'foreboding', 'jitters', 'tension', 'anxious', 'edgy', 'scared', 'panicked', 'paranoia', 'doubt', 'distress',
                 'tense', 'restless', 'fretful', 'nail-biting', 'suspense', 'timid', 'frightened', 'agitation', 'stress',
                 'uneasy', 'phobic', 'worried', 'nervous', 'terrified', 'horrified', 'dreadful', 'trepid', 'foreboding']


happiness_keywords = ['happiness', 'joy', 'glee', 'delight', 'euphoria', 'contentment', 'elation', 'bliss', 'ecstasy', 'cheerfulness',
                      'merriment', 'jubilation', 'satisfaction', 'excitement', 'exhilaration', 'uplifting', 'pleasure', 'gratitude',
                      'sunny', 'smile', 'laugh', 'beaming', 'happy', 'joyful', 'delighted', 'elated', 'exuberant', 'radiant', 'content',
                      'cheerful', 'jovial', 'pleased', 'gleeful', 'lighthearted', 'overjoyed', 'satisfied', 'blissful', 'ecstatic',
                      'vibrant', 'festive', 'good mood', 'high spirits', 'jolly', 'merry', 'upbeat', 'sunny', 'laughter']


sadness_keywords = ['sadness', 'sorrow', 'grief', 'melancholy', 'despair', 'heartache', 'tearful', 'unhappy', 'mourning', 'blue',
                    'woeful', 'disheartened', 'downcast', 'dejected', 'miserable', 'gloomy', 'despondent', 'downhearted', 'wretched',
                    'somber', 'lugubrious', 'depressed', 'forlorn', 'dismal', 'crestfallen', 'brokenhearted', 'low-spirited', 'weepy',
                    'sullen', 'glum', 'down', 'cast down', 'bitter', 'troubled', 'heavy-hearted', 'cheerless', 'morose', 'lamentable',
                    'funereal', 'sombre', 'down in the dumps', 'pensive', 'poignant', 'woebegone', 'long-faced', 'mournful']


surprise_keywords = ['surprise', 'amazement', 'astonishment', 'stun', 'awe', 'shock', 'wonder', 'startle', 'astound', 'dismay',
                     'stagger', 'stupefy', 'stupor', 'gasp', 'flabbergasted', 'incredulous', 'unbelievable',  'bewilderment', 'disbelief', 'confound', 'perplexity', 'disconcert', 'unexpected', 'daze', 'stunning', 'mind-blowing', 'jaw-dropping', 'awe-struck', 'breathtaking', 'astonishing', 'flummoxed', 'speechless''unanticipated', 'overwhelm', 'stupendous', 'eye-popping', 'mind-boggling', 'amazing', 'unforeseen', 'shook', 'stunned', 'unreal', 'dumbfounded', 'captivating', 'mesmerizing', 'in awe', 'out of the blue', 'unpredictable', 'remarkable', 'extraordinary', 'fantastic', 'incomprehensible', 'jolting', 'spectacular', 'surprised', 'shivering']

neutral_keywords = ['neutral', 'indifferent', 'unbiased', 'impartial', 'detached', 'nonchalant', 'uninterested', 'uninvolved',
                    'unresponsive', 'emotionless', 'apathetic', 'reserved', 'calm', 'composed', 'even-tempered', 'dispassionate',
                    'unemotional', 'stoic', 'unflappable', 'undisturbed', 'unruffled', 'unperturbed', 'unbothered', 'aloof', 'cool',
                    'collected', 'unexcitable', 'unimpressed', 'unmoved', 'undemonstrative', 'matter-of-fact', 'impersonal', 'neutral',
                    'noncommittal', 'uncommitted', 'unprejudiced', 'unbiased', 'impartial', 'blank', 'expressionless', 'detached',
                    'nonplussed', 'phlegmatic', 'unconcerned', 'unresponsive', 'uninterested', 'uninvolved', 'unfeeling']


def section_creator(token_sent, keywords):
    return (" ".join([sentence for sentence in token_sent if any(keyword.lower() in sentence.lower() for keyword in keywords)]))


def classify(text):
    token_sent = nltk.sent_tokenize(text)

    calculations = dict()

    for emotion in emotionss:
        if emotion != "":
            calculations[emotion + "_score"] = 0

    for emotion in emotionss:
        if emotion != "":
            calculations[emotion + "_section"] = section_creator(
                token_sent, eval(emotion + "_keywords"))
            if calculations[emotion + "_section"] != "":
                pol_sco = sia.polarity_scores(
                    calculations[emotion + "_section"])['compound']
                standardizeData = (pol_sco + 1) / 2
                calculations[emotion + "_score"] += standardizeData

    unclassified = {
        'Surprised': calculations["surprise_score"],
        'Feared': calculations["fear_score"],
        'Neutral': calculations["neutral_score"],
        'Happy': calculations["happiness_score"],
        'Sad': calculations["sadness_score"],
        'Angry': calculations["anger_score"],
    }

    classified = sorted(unclassified.items(), key=lambda x: x[1], reverse=True)

    clas_dict = dict(classified)

    final = []

    flag = 0

    for key in clas_dict:
        final.append(key)
        flag += 1
        if flag == 2:
            break

    return final


emotions = {
    "feared": [
        [
            "Take deep breaths to calm your nervous system.",
            "Identify and challenge irrational thoughts causing fear.",
            "Gradually expose yourself to what you fear to build resilience."
        ],
        [
            "Practice mindfulness techniques during anxious moments.",
            "Seek professional support to address deep-seated fears.",
            "Create a 'fear hierarchy' to tackle fears step by step."
        ],
        [
            "Visualize a calming place to reduce anxiety.",
            "Keep a fear journal to track triggers and reactions.",
            "Build a support network to share fears and seek encouragement."
        ]
    ],

    "neutral": [
        [
            "Practice mindfulness to stay in the present moment.",
            "Engage in activities that bring a sense of balance.",
            "Explore new hobbies to add variety to your routine."
        ],
        [
            "Take a break from screens and enjoy nature.",
            "Schedule 'me time' to recharge and relax.",
            "Reflect on the positives in your life to maintain a neutral mood."
        ],
        [
            "Maintain a consistent sleep schedule for emotional stability.",
            "Practice gratitude to appreciate the ordinary moments.",
            "Connect with others without the expectation of strong emotions."
        ]
    ],

    "happy": [
        [
            "Express gratitude for positive aspects of your life.",
            "Engage in activities that bring you joy and fulfillment.",
            "Connect with loved ones and share happy moments."
        ],
        [
            "Set achievable goals to experience a sense of accomplishment.",
            "Surround yourself with positive influences.",
            "Celebrate small victories to boost overall happiness."
        ],
        [
            "Practice acts of kindness to enhance your mood.",
            "Savor enjoyable moments and create positive memories.",
            "Engage in laughter and find humor in daily life."
        ]
    ],

    "sad": [
        [
            "Allow yourself to feel and acknowledge your emotions.",
            "Reach out to friends or a support system for comfort.",
            "Engage in activities that provide comfort and solace."
        ],
        [
            "Express your feelings through creative outlets like art or writing.",
            "Create a self-care routine to prioritize your emotional well-being.",
            "Set realistic expectations for yourself during challenging times."
        ],
        [
            "Attend social events to maintain connections even when feeling down.",
            "Seek professional help if sadness persists or intensifies.",
            "Practice self-compassion and avoid self-criticism during low moments."
        ]
    ],

    "angry": [
        [
            "Practice deep breathing or meditation to manage anger.",
            "Communicate assertively rather than aggressively.",
            "Take a break and engage in physical activity to release tension."
        ],
        [
            "Use 'I' statements to express your feelings without blame.",
            "Implement time-outs to cool off during heated moments.",
            "Explore the root causes of anger to address underlying issues."
        ],
        [
            "Channel anger into productive activities like exercise.",
            "Develop healthy outlets for frustration, such as journaling.",
            "Seek guidance from a therapist to explore and manage anger issues."
        ]
    ],

    "surprised": [
        [
            "Embrace the unexpected with an open mind.",
            "Find humor in surprises to lighten the mood.",
            "Reflect on the positive aspects of surprises in your life."
        ],
        [
            "Cultivate a sense of curiosity and openness to new experiences.",
            "Share surprise moments with others to enhance connections.",
            "Celebrate the spontaneity of life and its unpredictable nature."
        ],
        [
            "Adapt to unexpected changes with flexibility and resilience.",
            "Learn from surprises and view them as opportunities for growth.",
            "Find joy in the unpredictability of life's twists and turns."
        ]
    ]
}


def ret_tips(emotion):

    if emotion.lower() in emotions:
        return random.choice(emotions[emotion.lower()])
    else:
        return "Emotion not found."
