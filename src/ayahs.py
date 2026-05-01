"""Curated list of significant Quran ayahs and date-based selector.

Each entry is (surah, ayah). The list is intentionally diverse: well-known protective /
remembrance verses, reminders on patience, gratitude, tawakkul, mercy, repentance, and
popular ayahs from frequently-recited surahs.
"""
from __future__ import annotations

import datetime as _dt
import hashlib

SIGNIFICANT_AYAHS: list[tuple[int, int]] = [
    # --- Al-Fatiha (entire surah, all 7 ayahs) ---
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),

    # --- Al-Baqarah ---
    (2, 2),     # "This is the Book about which there is no doubt..."
    (2, 21),    # "O mankind, worship your Lord..."
    (2, 45),    # Seek help through patience and prayer
    (2, 152),   # Remember Me; I will remember you
    (2, 153),   # Allah is with the patient
    (2, 155),   # We will surely test you with something of fear...
    (2, 156),   # Inna lillahi wa inna ilayhi raji'un
    (2, 186),   # When My servants ask you concerning Me, indeed I am near
    (2, 201),   # Our Lord, give us in this world good...
    (2, 216),   # Perhaps you hate a thing and it is good for you
    (2, 255),   # Ayat al-Kursi
    (2, 256),   # No compulsion in religion
    (2, 261),   # Charity multiplied like a grain producing seven ears
    (2, 268),   # Shaytan promises poverty
    (2, 285),   # The Messenger has believed...
    (2, 286),   # Allah does not burden a soul beyond that it can bear

    # --- Aal-e-Imran ---
    (3, 8),     # Our Lord, let not our hearts deviate
    (3, 26),    # O Allah, Owner of Sovereignty
    (3, 31),    # If you should love Allah, then follow me
    (3, 54),    # And they planned, and Allah planned
    (3, 102),   # Fear Allah as He should be feared
    (3, 134),   # Those who spend in ease and in adversity
    (3, 139),   # Do not weaken and do not grieve
    (3, 159),   # By mercy from Allah, you were lenient with them
    (3, 173),   # Sufficient for us is Allah, and excellent is the Trustee
    (3, 185),   # Every soul will taste death
    (3, 190),   # Indeed, in the creation of the heavens and earth
    (3, 191),   # Those who remember Allah standing, sitting, lying

    # --- An-Nisa ---
    (4, 36),    # Worship Allah and associate nothing with Him
    (4, 59),    # Obey Allah and the Messenger
    (4, 86),    # When you are greeted, greet with better

    # --- Al-Ma'idah ---
    (5, 2),     # Cooperate in righteousness and piety
    (5, 3),     # This day I have perfected for you your religion
    (5, 8),     # Be persistently standing firm in justice
    (5, 32),    # Whoever saves a life, it is as if he saved all mankind

    # --- Al-An'am ---
    (6, 59),    # With Him are the keys of the unseen
    (6, 73),    # His is the dominion the Day the Horn is blown
    (6, 162),   # My prayer, my sacrifice, my living and my dying...

    # --- Al-A'raf ---
    (7, 23),    # Our Lord, we have wronged ourselves
    (7, 56),    # Do not cause corruption on the earth
    (7, 199),   # Take what is given freely, enjoin what is good
    (7, 205),   # Remember your Lord within yourself in humility

    # --- Al-Anfal ---
    (8, 2),     # The believers are only those who, when Allah is mentioned, their hearts tremble

    # --- At-Tawbah ---
    (9, 51),    # Never will we be struck except by what Allah has decreed
    (9, 105),   # Do, for Allah will see your deeds
    (9, 128),   # There has certainly come to you a Messenger from yourselves
    (9, 129),   # Allah is sufficient for me, there is no deity except Him

    # --- Yunus ---
    (10, 62),   # Unquestionably, the allies of Allah have no fear
    (10, 107),  # If Allah touches you with adversity, no remover except Him

    # --- Hud ---
    (11, 88),   # My success is not but through Allah
    (11, 114),  # Indeed, good deeds do away with misdeeds
    (11, 115),  # Be patient, for indeed Allah does not allow to be lost the reward of doers of good

    # --- Yusuf ---
    (12, 64),   # Allah is the best Guardian, and He is the most Merciful
    (12, 87),   # Do not despair of relief from Allah

    # --- Ar-Ra'd ---
    (13, 11),   # Allah does not change a people's condition until they change themselves
    (13, 28),   # Verily, in the remembrance of Allah do hearts find rest

    # --- Ibrahim ---
    (14, 7),    # If you are grateful, I will surely increase you
    (14, 24),   # A good word is like a good tree
    (14, 34),   # If you should count the favors of Allah, you could not enumerate them
    (14, 40),   # My Lord, make me an establisher of prayer

    # --- An-Nahl ---
    (16, 18),   # If you should count the favors of Allah, you could not enumerate them
    (16, 53),   # Whatever you have of favor — it is from Allah
    (16, 90),   # Allah orders justice and good conduct
    (16, 97),   # Whoever does righteousness, We will surely give him a good life
    (16, 128),  # Indeed, Allah is with those who fear Him

    # --- Al-Isra ---
    (17, 23),   # Your Lord has decreed that you not worship except Him, and to parents good treatment
    (17, 24),   # Lower to them the wing of humility out of mercy
    (17, 32),   # Do not approach unlawful sexual intercourse
    (17, 80),   # My Lord, cause me to enter a sound entrance
    (17, 82),   # We send down of the Qur'an that which is healing and mercy

    # --- Al-Kahf ---
    (18, 10),   # Our Lord, grant us mercy from Yourself
    (18, 23), (18, 24),  # Never say of anything "I will do that tomorrow" except [adding] "If Allah wills"
    (18, 28),   # Keep yourself patient with those who call upon their Lord
    (18, 46),   # Wealth and children are the adornment of worldly life
    (18, 110),  # Whoever hopes for the meeting with his Lord, let him do righteous work

    # --- Maryam ---
    (19, 96),   # Those who have believed and done righteous deeds — the Most Merciful will appoint for them affection

    # --- Ta-Ha ---
    (20, 14),   # Indeed, I am Allah; there is no deity except Me, so worship Me
    (20, 25), (20, 26), (20, 27), (20, 28),  # Musa's dua: Rabbi-shrah-li sadri
    (20, 114),  # My Lord, increase me in knowledge
    (20, 124),  # Whoever turns away from My remembrance — his life will be of hardship

    # --- Al-Anbiya ---
    (21, 87),   # Yunus's dua: La ilaha illa anta subhanaka inni kuntu min az-zalimin
    (21, 107),  # We have not sent you except as a mercy to the worlds

    # --- Al-Hajj ---
    (22, 77),   # O you who have believed, bow and prostrate

    # --- Al-Mu'minun ---
    (23, 1), (23, 2),  # Successful are the believers, those who in their prayer are humbly submissive
    (23, 115),  # Did you think We created you uselessly?
    (23, 118),  # My Lord, forgive and have mercy

    # --- An-Nur ---
    (24, 35),   # Ayat al-Nur: Allah is the Light of the heavens and the earth
    (24, 55),   # Allah has promised those who have believed and done righteous deeds

    # --- Al-Furqan ---
    (25, 63),   # The servants of the Most Merciful are those who walk upon the earth easily
    (25, 70),   # Except for those who repent, believe and do righteous work
    (25, 74),   # Our Lord, grant us from among our wives and offspring comfort to our eyes

    # --- Ash-Shu'ara ---
    (26, 80),   # When I am ill, it is He who cures me
    (26, 83),   # My Lord, grant me wisdom and join me with the righteous

    # --- An-Naml ---
    (27, 62),   # Is He [not best] who responds to the desperate one when he calls upon Him

    # --- Al-Qasas ---
    (28, 24),   # Musa's dua: My Lord, indeed I am, for whatever good You would send down to me, in need
    (28, 77),   # Seek, through that which Allah has given you, the home of the Hereafter
    (28, 88),   # Everything will be destroyed except His Face

    # --- Al-Ankabut ---
    (29, 45),   # Recite what is sent of the Book and establish prayer
    (29, 69),   # Those who strive for Us — We will surely guide them to Our ways

    # --- Ar-Rum ---
    (30, 21),   # Among His signs is that He created for you mates from yourselves
    (30, 60),   # Be patient. Indeed, the promise of Allah is truth

    # --- Luqman ---
    (31, 13),   # O my son, do not associate anything with Allah
    (31, 17),   # O my son, establish prayer, enjoin what is right
    (31, 18),   # Do not turn your cheek in contempt toward people
    (31, 19),   # Be moderate in your pace and lower your voice

    # --- Al-Ahzab ---
    (33, 21),   # In the Messenger of Allah you have an excellent example
    (33, 35),   # Indeed, the Muslim men and Muslim women, the believing men and believing women...
    (33, 41),   # O you who have believed, remember Allah with much remembrance
    (33, 56),   # Allah confers blessing upon the Prophet, and His angels [ask Him to do so]
    (33, 70), (33, 71),  # Speak words of appropriate justice

    # --- Saba ---
    (34, 13),   # Few of My servants are grateful

    # --- Fatir ---
    (35, 5),    # Indeed, the promise of Allah is truth, so let not the worldly life delude you

    # --- Yasin ---
    (36, 1), (36, 2), (36, 3), (36, 4),  # Yasin opening
    (36, 9),    # We have put before them a barrier and behind them a barrier
    (36, 38),   # The sun runs on for a term appointed
    (36, 58),   # Peace, a word from a Merciful Lord
    (36, 82),   # His command, when He intends a thing, is only that He says "Be," and it is

    # --- As-Saffat ---
    (37, 180), (37, 181), (37, 182),  # Glorified is your Lord — closing of As-Saffat

    # --- Sad ---
    (38, 35),   # Sulayman's dua: My Lord, forgive me and grant me a kingdom

    # --- Az-Zumar ---
    (39, 9),    # Are those who know equal to those who do not know?
    (39, 10),   # Indeed, the patient will be given their reward without account
    (39, 53),   # Do not despair of the mercy of Allah; He forgives all sins

    # --- Ghafir ---
    (40, 7),    # Those who carry the Throne ask forgiveness for those who have believed
    (40, 60),   # Call upon Me; I will respond to you

    # --- Fussilat ---
    (41, 30),   # Those who have said "Our Lord is Allah" and remained on a right course
    (41, 33),   # Who is better in speech than one who invites to Allah
    (41, 34),   # Repel evil with that which is better
    (41, 53),   # We will show them Our signs in the horizons and within themselves

    # --- Ash-Shura ---
    (42, 11),   # There is nothing like unto Him, and He is the Hearing, the Seeing
    (42, 30),   # Whatever strikes you of disaster, it is for what your hands have earned

    # --- Az-Zukhruf ---
    (43, 67),   # Close friends, that Day, will be enemies — except for the righteous

    # --- Muhammad ---
    (47, 7),    # If you support Allah, He will support you

    # --- Al-Fath ---
    (48, 1),    # Indeed, We have given you, [O Muhammad], a clear conquest
    (48, 4),    # It is He who sent down tranquility into the hearts of the believers
    (48, 29),   # Muhammad is the Messenger of Allah; and those with him are forceful against the disbelievers

    # --- Al-Hujurat ---
    (49, 10),   # The believers are but brothers
    (49, 11),   # Do not let a people ridicule another people
    (49, 12),   # Avoid much suspicion. Some suspicion is sin
    (49, 13),   # We have created you from male and female and made you peoples and tribes

    # --- Qaf ---
    (50, 16),   # We are closer to him than his jugular vein

    # --- Adh-Dhariyat ---
    (51, 56),   # I did not create the jinn and mankind except to worship Me

    # --- An-Najm ---
    (53, 39), (53, 40),  # Man can have nothing but what he strives for

    # --- Ar-Rahman ---
    (55, 1), (55, 2), (55, 3), (55, 4),  # The Most Merciful taught the Qur'an
    (55, 13),   # So which of the favors of your Lord would you deny?
    (55, 26), (55, 27),  # Everyone upon the earth will perish, and there will remain the Face of your Lord
    (55, 60),   # Is the reward for good [anything] but good?
    (55, 78),   # Blessed is the name of your Lord, Owner of Majesty and Honor

    # --- Al-Waqi'ah ---
    (56, 79),   # None touch it except the purified

    # --- Al-Hadid ---
    (57, 4),    # He is with you wherever you are
    (57, 20),   # Know that the life of this world is but amusement and diversion

    # --- Al-Mujadila ---
    (58, 11),   # Allah will raise those who have believed among you and those given knowledge

    # --- Al-Hashr ---
    (59, 18),   # Let every soul look to what it has put forth for tomorrow
    (59, 19),   # Do not be like those who forgot Allah, so He made them forget themselves
    (59, 22), (59, 23), (59, 24),  # The names of Allah — closing of Al-Hashr

    # --- As-Saff ---
    (61, 2), (61, 3),  # Why do you say what you do not do?

    # --- At-Talaq ---
    (65, 2), (65, 3),  # Whoever fears Allah, He will make for him a way out

    # --- At-Tahrim ---
    (66, 8),    # O you who have believed, repent to Allah with sincere repentance

    # --- Al-Mulk ---
    (67, 1), (67, 2),  # Blessed is He in whose hand is dominion
    (67, 13), (67, 14),  # Whether you conceal your speech or publicize it
    (67, 15),   # It is He who made the earth tame for you
    (67, 19),   # Have they not seen the birds above them...

    # --- Al-Qalam ---
    (68, 4),    # Indeed, you are of a great moral character

    # --- Al-Ma'arij ---
    (70, 5),    # So be patient with gracious patience

    # --- Al-Muzzammil ---
    (73, 8),    # Remember the name of your Lord and devote yourself to Him

    # --- Al-Insan ---
    (76, 8), (76, 9),  # They give food in spite of love for it...

    # --- An-Naba ---
    (78, 39),   # That is the True Day; so he who wills may take to his Lord a return

    # --- Al-A'la ---
    (87, 14), (87, 15),  # He has certainly succeeded who purifies himself

    # --- Ash-Sharh ---
    (94, 5), (94, 6),  # For indeed, with hardship will be ease
    (94, 7), (94, 8),  # When you have finished, then stand up [for worship]

    # --- At-Tin ---
    (95, 4),    # We have certainly created man in the best of stature

    # --- Al-Alaq ---
    (96, 1), (96, 2), (96, 3), (96, 4), (96, 5),  # Iqra — first revelation

    # --- Al-Qadr ---
    (97, 1), (97, 3),  # Indeed, We sent it down during the Night of Decree

    # --- Al-Bayyinah ---
    (98, 7), (98, 8),  # Those who have believed and done righteous deeds — best of creatures

    # --- Az-Zalzalah ---
    (99, 7), (99, 8),  # Whoever does an atom's weight of good will see it

    # --- Al-Asr (entire surah) ---
    (103, 1), (103, 2), (103, 3),

    # --- Al-Kawthar (entire surah) ---
    (108, 1), (108, 2), (108, 3),

    # --- Al-Ikhlas (entire surah) ---
    (112, 1), (112, 2), (112, 3), (112, 4),

    # --- Al-Falaq (entire surah) ---
    (113, 1), (113, 2), (113, 3), (113, 4), (113, 5),

    # --- An-Nas (entire surah) ---
    (114, 1), (114, 2), (114, 3), (114, 4), (114, 5), (114, 6),
]


def pick_for_date(date: _dt.date) -> tuple[int, int]:
    """Deterministically pick an ayah for the given UTC date.

    Same date always yields the same ayah (so re-runs are idempotent), but the choice
    rotates through the curated list as dates advance.
    """
    if not SIGNIFICANT_AYAHS:
        raise ValueError("SIGNIFICANT_AYAHS list is empty")
    digest = hashlib.sha256(date.isoformat().encode("utf-8")).digest()
    index = int.from_bytes(digest[:8], "big") % len(SIGNIFICANT_AYAHS)
    return SIGNIFICANT_AYAHS[index]
