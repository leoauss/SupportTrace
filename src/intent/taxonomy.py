# src/intent/taxonomy.py

"""
Single source of truth for the AppleSupport intent taxonomy.
All intent names, descriptions, and few-shot examples live here.
"""
INTENT_CATALOG = {
    "device_issue": "Hardware problem — screen, battery, charging, physical damage",
    "software_update": "iOS/macOS update issues — stuck, failed, post-update regression",
    "software_issue": "OS/app bugs NOT caused by updates — autocorrect, UI glitches, system errors",
    "app_crash": "A specific app not working, crashing, or freezing",
    "account_access": "Apple ID, login, 2FA, locked account",
    "icloud_storage": "iCloud sync, storage full, backup issues",
    "billing_subscription": "Charges, refunds, Apple Music/TV+/One subscriptions",
    "connectivity": "WiFi, Bluetooth, cellular, AirDrop issues",
    "performance": "Slow device, overheating, battery drain (no update mentioned)",
    "data_transfer": "Migration, backup restore, switching devices",
    "purchase_delivery": "Order status, shipping, Apple Store issues",
    "how_to": "General how-to questions, feature discovery",
    "conduct_complaint": "Complaints about staff behavior, customer service rudeness, or discrimination in-store or online",
    "content_dispute": "Fraudulent sales, licensing disputes, or disputes over authorized repair center claims",
    "feature_request": "Suggestions for new features, design tweaks, or product roadmap requests, NOT fault reports",
    "other": "Feedback, complaints, off-topic, or unclear",
}


VALID_INTENTS = list(INTENT_CATALOG.keys())

FEW_SHOT_EXAMPLES = [
# --- device_issue (hardware problem, not caused by software) ---
    {
        "text": "@115858 Why has my apple MacBook Pro charger which is 4-5 weeks old just exploded? What are you going to do about it????!!! I'm DISGUSTED!!!!",
        "primary_intent": "device_issue",
        "secondary_intents": [],
    },
    {
        "text": "PHONE KEEPS TURNING OFF ABRUPTLY EVEN THOUGH I RESTARTED IT AND KEPT IT OFF THE WHOLE NIGHT. WHAT DO I DO NOW @AppleSupport HOW DO I GET THIS DARK SCR",
        "primary_intent": "device_issue",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport I plugged in my Apple iPhone charger into my IPhone 7 and it didn't charge? A gold bit on each side has gone black?",
        "primary_intent": "device_issue",
        "secondary_intents": [],
    },
# --- software_update (problem explicitly attributed to an update/upgrade) ---
    {
        "text": "Since the iOS 11.0.3 update by @115858 my battery is shocking 19% now hardly used it all days & all battery sucking turned off. @AppleSupport",
        "primary_intent": "software_update",
        "secondary_intents": ["performance"],
    },
    {
        "text": "Anyone else running macOS 10.13.1 having trouble turning Bluetooth OFF? This release seems littered with bugs. @AppleSupport",
        "primary_intent": "software_update",
        "secondary_intents": ["connectivity"],
    },
    {
        "text": "@AppleSupport since I've updated my iPhone 6s to ios11 I can no longer download apps or music and my iTunes account keeps signing out",
        "primary_intent": "software_update",
        "secondary_intents": ["account_access"],
    },
# --- software_issue (a bug/glitch, no update causation stated) ---
    {
        "text": "@115858 if you can help me, ill really appreciate it. My phone is changing the i* for this symbol I️ . Do you know why, and how to fix it?",
        "primary_intent": "software_issue",
        "secondary_intents": [],
    },
    {
        "text": "Where did my app library go? @AppleSupport",
        "primary_intent": "software_issue",
        "secondary_intents": [],
    },
    {
        "text": "MY PHONE IS BEING SO WIERD like i was listening to music but it was playing just the instrumental part. no voice. i did a hard reset and suddenly ever",
        "primary_intent": "software_issue",
        "secondary_intents": [],
    },
# --- app_crash ---
    {
        "text": "@AppleSupport Please make the crashing and battery drain stop 😵😵😵",
        "primary_intent": "app_crash",
        "secondary_intents": ["performance"],
    },
    {
        "text": "@AppleSupport why does safari always kills background audio from the podcast app? #iOS11 #onlyapple",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
    {
        "text": "Meu celular ta travando de maneira surreal, @115858 @AppleSupport MELHORA ESSA PORRA DESSE IOS",
        "primary_intent": "software_issue",
        "secondary_intents": ["performance"],
    },
# --- performance ---
    {
        "text": "Why does my phone die at 50% @AppleSupport",
        "primary_intent": "performance",
        "secondary_intents": [],
    },
    {
        "text": "Hello @AppleSupport , Do you also sell a plug to prevent energy leaking out of mij iPhone battery..?",
        "primary_intent": "performance",
        "secondary_intents": [],
    },
    {
        "text": "Y the fuck my phone die so fast now I fucking hate this shit @115858 wyd",
        "primary_intent": "performance",
        "secondary_intents": [],
    },
# --- billing_subscription (charges, refunds, subscriptions) ---
    {
        "text": "@AppleSupport I bought an iTunes gift card worth 15 a week ago, and the email still hasn't come into my inbox to tell me the code",
        "primary_intent": "billing_subscription",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport I bought an iPhone 8 with AppleCare+. Wanting to return the iPhone 8. What happens with the AppleCare+?",
        "primary_intent": "billing_subscription",
        "secondary_intents": [],
    },
# --- connectivity ---
    {
        "text": "@AppleSupport still no reliable Bluetooth on my iPhone 8+.",
        "primary_intent": "connectivity",
        "secondary_intents": [],
    },
    {
        "text": "Anyone else dropping \"merged call\" on #ios11.1.1 ? Call merges, I get dropped they continue on, can't get back in @115858 #help",
        "primary_intent": "connectivity",
        "secondary_intents": [],
    },
    {
        "text": "Nice @115858. Less than a week old then WiFi and BT break on my new iPhone. I tried all your support articles. So glad I purchased! https://t.co/WKbGg",
        "primary_intent": "connectivity",
        "secondary_intents": [],
    },
# --- how_to ---
    {
        "text": "@AppleSupport can I use iCloud Drive to share files with my friends in the same manor as Dropbox?",
        "primary_intent": "how_to",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport Hi, how can I check on my iPhone when the last backup was? I cannot seem to find out with the iOS 11 update.. Please assist",
        "primary_intent": "how_to",
        "secondary_intents": ["icloud_storage"],
    },
    {
        "text": "@AppleSupport What VR set can I use with my base 2017 3.4GHz 5k iMac?",
        "primary_intent": "how_to",
        "secondary_intents": [],
    },
# --- icloud_storage ---
    {
        "text": "@AppleSupport hi I need help my photos are missing",
        "primary_intent": "icloud_storage",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport hey guys. My new #iPhoneX keeps missing messages. As in they appear on my iPad and remarkably on my Apple Watch but then don't show up o",
        "primary_intent": "icloud_storage",
        "secondary_intents": [],
    },
    {
        "text": "@115948 @AppleSupport why don't my playlists appear in my library?? :(",
        "primary_intent": "icloud_storage",
        "secondary_intents": [],
    },
# --- account_access ---
    {
        "text": "@AppleSupport Now the legitimate Apple login page isn't loading!!!! I want to reset my password!!!",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport So frustrating setting up an appt to come in - signed in w/ login info, can't move on w/o a 2factor authentification",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "@115858 suck! Upgrade phone and I lose my Apple ID. Can't get new id without old and can't book Genius bar help appointment",
        "primary_intent": "account_access",
        "secondary_intents": ["software_update"],
    },
# --- purchase_delivery ---
    {
        "text": "@AppleSupport @5146 @1671 Seriously the package was out for delivery and then no more updates for a full week. Now you need to investigate for a few w",
        "primary_intent": "purchase_delivery",
        "secondary_intents": [],
    },
    {
        "text": "Dear @115858, I have an online order which I never received - who can I talk to?",
        "primary_intent": "purchase_delivery",
        "secondary_intents": [],
    },
# --- data_transfer ---
    {
        "text": "Hey @AppleSupport what's the deal?!? Why the hell should I reset my Apple Watch to pair with my new iPhone? There's GOT to be another way. Really don'",
        "primary_intent": "data_transfer",
        "secondary_intents": ["connectivity"],
    },
    {
        "text": "@AppleSupport just installed your latest update on my 6s, it failed, and now my phone won't even restore 'error 21', thanks apple",
        "primary_intent": "data_transfer",
        "secondary_intents": ["software_update"],
    },
# --- other (vent / off-topic — doesn't fit a specific product issue) ---
    {
        "text": "@AppleSupport (2/2) I really have no idea anymore... so I might as well throw everything away. Never again with Apple for me. Terrible service!",
        "primary_intent": "other",
        "secondary_intents": [],
    },
    {
        "text": "My phone on some bullshit like dam @115858 must really want me to buy a new phone 🙄",
        "primary_intent": "other",
        "secondary_intents": ["performance"],
    },
    {
        "text": "@AppleSupport WTF? https://t.co/KP7it5y258",
        "primary_intent": "other",
        "secondary_intents": [],
    },

    {
        "text": "@AppleSupport My apple calender app is crashing again and again fix this shitty app",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
# --- conduct_complaint ---
    {
        "text": "@tim_cook and @Apple I'm just curious: do you endorse/encourage your customer facing reps to be jerks?:) Wish I could say “asking for a friend” but actually that's my chat with someone on your “lovely” team",
        "primary_intent": "conduct_complaint",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport Having the most terrible experience at Apple Covent Garden. Have an important [appointment] with the Genius Bar. Showed this to the greeters and other. Have been shouted at twice. Clearly 75 year old female customers are not welcome in your stores",
        "primary_intent": "conduct_complaint",
        "secondary_intents": [],
    },
# --- content_dispute ---
    {
        "text": "@Apple when itunes streams your film without any valid license agreement, there is no way to find a human to figure out who fraudulently sold the film to them. I am being shuffled around different customer services pages that require me to already be a member to access...",
        "primary_intent": "content_dispute",
        "secondary_intents": [],
    },
    {
        "text": "Hello, @Apple. Do you not consider it illegal and take appropriate action if a service facility falsely represents itself as an authorized one and displays that information on board, but in reality, it is not one?",
        "primary_intent": "content_dispute",
        "secondary_intents": [],
    },
# --- feature_request ---
    {
        "text": "Shouldn’t iPhones prioritize reconnection to the last used Bluetooth device over defaulting to CarPlay? A tweak for user-preferred connectivity would be great. @Apple, any chance?",
        "primary_intent": "feature_request",
        "secondary_intents": ["connectivity"],
    },
    # --- app_crash ---
    {
        "text": "Safari keeps crashing every time I try to open more than 3 tabs on my iPhone 13, so annoying",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport Instagram freezes and I have to force close it like 10 times a day now, is this an iOS thing?",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
    {
        "text": "why does the App Store just hang on a blank white screen every single time I open it #fed_up",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport Mail app crashed again while I was mid-email and I lost everything I typed 😡",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
    {
        "text": "Spotify keeps closing itself out of nowhere on my iPad, anyone else having this issue?",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport Camera app freezes up whenever I try to switch to portrait mode, have to restart my phone to fix it",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
    {
        "text": "Facebook keeps force closing on my iPhone 14 right after I open it, tried reinstalling twice already @AppleSupport",
        "primary_intent": "app_crash",
        "secondary_intents": [],
    },
# --- how_to ---
    {
        "text": "@AppleSupport how do I turn off read receipts just for one person in Messages?",
        "primary_intent": "how_to",
        "secondary_intents": [],
    },
    {
        "text": "Is there a way to set a specific ringtone for just one contact on iOS? Can't find the option @AppleSupport",
        "primary_intent": "how_to",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport how can I free up storage without deleting my photos?",
        "primary_intent": "how_to",
        "secondary_intents": ["icloud_storage"],
    },
    {
        "text": "how do you stop autoplay on Apple TV+ between episodes, it's driving me crazy",
        "primary_intent": "how_to",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport is there a way to schedule a text message to send later on iPhone?",
        "primary_intent": "how_to",
        "secondary_intents": [],
    },
    {
        "text": "How do I transfer my eSIM to my new iPhone 15? Anyone know the steps @AppleSupport",
        "primary_intent": "how_to",
        "secondary_intents": ["data_transfer"],
    },
    {
        "text": "@AppleSupport how can I see which apps are draining my battery the most?",
        "primary_intent": "how_to",
        "secondary_intents": [],
    },
# --- account_access ---
    {
        "text": "@AppleSupport locked out of my Apple ID, it says my account is disabled and I have no idea why",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "Can't get past two factor authentication because my trusted device is a phone I no longer have, @AppleSupport please help",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport I reset my password 3 times now and it still says incorrect when I try to log in",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "forgot the passcode to my old iPhone and now I can't get into my Apple ID to recover anything",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport keep getting 'incorrect verification code' even though I'm copying it directly from the text message",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "My Apple ID got locked after I traveled to a new country, verification code isn't even coming through @AppleSupport",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
    {
        "text": "@AppleSupport why does it keep logging me out of iCloud every single day, I have to sign back in constantly",
        "primary_intent": "account_access",
        "secondary_intents": [],
    },
]


def build_intent_description_block() -> str:
    """Format intent catalog as a numbered list for the prompt."""
    lines = []
    for i, (name, desc) in enumerate(INTENT_CATALOG.items(), 1):
        lines.append(f"{i}. {name}: {desc}")
    return "\n".join(lines)

def build_few_shot_block() -> str:
    """Format few-shot examples for the prompt."""
    lines = []
    for ex in FEW_SHOT_EXAMPLES:
        secondary = ", ".join(ex["secondary_intents"]) if ex["secondary_intents"] else "none"
        lines.append(
            f'Customer: "{ex["text"]}"\n'
            f'Primary intent: {ex["primary_intent"]}\n'
            f'Secondary intents: {secondary}\n'
        )
    return "\n".join(lines)