from flask import Flask, render_template, request, redirect, session, send_from_directory, Response
import os

app = Flask(__name__)
app.secret_key = 'fl4sk_s3cr3t_n0t_th3_fl4g_xD'

FLAG = os.environ.get('FLAG', 'CUTS{gh0st_1n_th3_m4ch1n3_4l3x_n3v3r_d13d}')
VAULT_TOKEN = 'gh0st_1n_th3_m4ch1n3'
ADMIN_USER = 'admin'
ADMIN_PASS = 'r4d10h34d'
VIGENERE_KEY = 'radiohead'

SUPPORTED_LANGS = ['en', 'ru', 'uz']

TRANSLATIONS = {
    'en': {
        'nav_home': 'home',
        'nav_about': 'about',
        'nav_music': 'music',
        'nav_setup': 'setup',
        'obituary': 'This blog is preserved in memory of Alex R., who passed away on January 3rd, 2003. His friend Marco wrote: <em>"Alex\'s password was always something he loved more than anything in the world."</em> — Rest in peace, Alex. The machine remembers.',
        'footer_copy': 'alex-r.local &copy; 2001-2003 &nbsp;|&nbsp; best viewed in 800x600',
        'footer_visitors': 'visitors',
        'section_posts': 'recent posts',
        'back': 'back',
        'back_posts': 'back to all posts',
        'logout': '[ logout ]',
        'no_comments': 'no comments yet.',
        # about
        'about_section': 'about me',
        'about_p1': "I'm Alex. 21 years old (as of 2002). I live somewhere cold and spend most of my time in front of screens. Programmer by instinct, not by profession — yet.",
        'about_p2': 'Started coding at 13 on my dad\'s 386. First language was BASIC, then C, now mostly Python when I\'m building things, and bash when I\'m breaking things. Linux user since 1998. I dual-boot exactly zero things.',
        'about_p3': "When I'm not coding, I'm listening to music. My absolute favourite band in the world is",
        'about_p3b': "Has been since I was 16 and first heard The Bends. I've seen them live twice. OK Computer is the greatest album ever recorded. This is not up for debate.",
        'about_p4': "I care about privacy, encryption, and the idea that information should be free — but that secrets should be kept by those who deserve to keep them.",
        'about_p5': "This blog started in 2001 as a place to think out loud. I don't know who reads it. Probably nobody. That's fine.",
        'about_interests': 'interests',
        'about_i1': 'cryptography — classical and modern',
        'about_i2': 'linux systems administration',
        'about_i3': 'network security (the ethical kind... mostly)',
        'about_i4': 'radiohead, portishead, massive attack, aphex twin',
        'about_i5': 'science fiction — specifically gibson, dick, lem',
        'about_i6': 'amateur radio (call sign: not telling you)',
        'about_contact': 'contact',
        'about_c1': "I don't have a contact form. If you know me, you know how to reach me.",
        'about_c2': "If you don't know me — figure it out. That's kind of the point.",
        # admin
        'access_restricted': '[ ACCESS RESTRICTED ]',
        'admin_subtitle': 'admin panel // authorized users only',
        'label_username': 'username',
        'label_password': 'password',
        'btn_auth': 'authenticate',
        'admin_footer_1': "private area. if you don't know the credentials,",
        'admin_footer_2': "you're not supposed to be here.",
        'admin_footer_3': 'or maybe you are. dig deeper.',
        'error_invalid': 'Invalid credentials.',
        # diary
        'diary_section': "alex's private journal",
        'diary_access_1': 'Access granted. These files were encrypted by Alex before his death.',
        'diary_access_2': 'The contents are protected with his personal cipher. Only those who truly knew him can read this.',
        'diary_cipher_label': '// journal_entry_2002-12-12.enc — vigenere cipher',
        'diary_hint_pre': 'The cipher key is something Alex loved deeply. He wrote about it. Many times. The key starts with the letter',
        'diary_hint_post': 'What mattered most to him was never a secret.',
        'diary_tools_1': '// Vigenere cipher: each letter is shifted by the corresponding letter of the key.',
        'diary_tools_2': '// Key repeats cyclically. Non-alphabetic characters are unchanged.',
        'diary_tools_3': '// Tools:',
        # vault
        'vault_title': '// ACCESS GRANTED //',
        'vault_sub': "you found alex's vault &nbsp;|&nbsp; well done",
        'vault_text_1': 'You read everything he wrote.',
        'vault_text_2': 'You found the git history.',
        'vault_text_3': 'You cracked the cipher.',
        'vault_text_4': 'You are exactly the person Alex meant to find this.',
        'vault_quote': '"The system outlives the user. The information outlives the person."',
        'vault_author': '— Alex R., December 12, 2002. 03:47 AM.',
        # vault denied
        'denied_access': 'access denied. wrong token.',
        'denied_sub': "the vault knows you haven't earned it yet.",
    },
    'ru': {
        'nav_home': 'главная',
        'nav_about': 'обо мне',
        'nav_music': 'музыка',
        'nav_setup': 'железо',
        'obituary': 'Этот блог сохранён в память об Алексе Р., скончавшемся 3 января 2003 года. Его друг Марко написал: <em>«Пароль Алекса всегда был тем, что он любил больше всего на свете.»</em> — Покойся с миром, Алекс. Машина помнит.',
        'footer_copy': 'alex-r.local &copy; 2001-2003 &nbsp;|&nbsp; лучше смотреть при 800x600',
        'footer_visitors': 'посетители',
        'section_posts': 'последние записи',
        'back': 'назад',
        'back_posts': 'ко всем записям',
        'logout': '[ выйти ]',
        'no_comments': 'комментариев пока нет.',
        # about
        'about_section': 'обо мне',
        'about_p1': 'Я Алекс. 21 год (на 2002 год). Живу где-то на холоде и провожу большую часть времени перед экранами. Программист по призванию, но не по профессии — пока.',
        'about_p2': 'Начал кодить в 13 лет на папиной 386-й. Первый язык — BASIC, потом C, сейчас в основном Python для разработки и bash для «ломания» вещей. Пользователь Linux с 1998 года. Двойную загрузку не использую от слова совсем.',
        'about_p3': 'Когда не кожу, слушаю музыку. Моя абсолютно любимая группа в мире —',
        'about_p3b': 'Так было с 16 лет, когда я впервые услышал The Bends. Видел их вживую дважды. OK Computer — величайший альбом из когда-либо записанных. Это не обсуждается.',
        'about_p4': 'Мне важны приватность, шифрование и идея о том, что информация должна быть свободной — но тайны должны хранить те, кто их заслуживает.',
        'about_p5': 'Этот блог появился в 2001-м как место, где я думаю вслух. Не знаю, кто его читает. Наверное, никто. Ну и ладно.',
        'about_interests': 'интересы',
        'about_i1': 'криптография — классическая и современная',
        'about_i2': 'системное администрирование Linux',
        'about_i3': 'сетевая безопасность (этичная... в основном)',
        'about_i4': 'radiohead, portishead, massive attack, aphex twin',
        'about_i5': 'научная фантастика — особенно гибсон, дик, лем',
        'about_i6': 'радиолюбительство (позывной: не скажу)',
        'about_contact': 'контакты',
        'about_c1': 'У меня нет формы обратной связи. Если знаешь меня — знаешь, как связаться.',
        'about_c2': 'Если нет — разберись сам. Это и есть суть.',
        # admin
        'access_restricted': '[ ДОСТУП ОГРАНИЧЕН ]',
        'admin_subtitle': 'панель администратора // только авторизованным',
        'label_username': 'логин',
        'label_password': 'пароль',
        'btn_auth': 'войти',
        'admin_footer_1': 'закрытая зона. если не знаешь учётные данные,',
        'admin_footer_2': 'тебя здесь быть не должно.',
        'admin_footer_3': 'или всё же должно. копай глубже.',
        'error_invalid': 'Неверные учётные данные.',
        # diary
        'diary_section': 'личный дневник алекса',
        'diary_access_1': 'Доступ предоставлен. Эти файлы были зашифрованы Алексом до его смерти.',
        'diary_access_2': 'Содержимое защищено его личным шифром. Прочесть это могут только те, кто действительно его знал.',
        'diary_cipher_label': '// journal_entry_2002-12-12.enc — шифр Виженера',
        'diary_hint_pre': 'Ключ шифра — это то, что Алекс любил всем сердцем. Он писал об этом много раз. Ключ начинается на букву',
        'diary_hint_post': 'То, что было для него важнее всего, никогда не было секретом.',
        'diary_tools_1': '// Шифр Виженера: каждая буква сдвигается на соответствующую букву ключа.',
        'diary_tools_2': '// Ключ повторяется циклически. Не-алфавитные символы не меняются.',
        'diary_tools_3': '// Инструменты:',
        # vault
        'vault_title': '// ДОСТУП РАЗРЕШЁН //',
        'vault_sub': 'ты нашёл хранилище алекса &nbsp;|&nbsp; отличная работа',
        'vault_text_1': 'Ты прочёл всё, что он написал.',
        'vault_text_2': 'Ты нашёл историю git.',
        'vault_text_3': 'Ты взломал шифр.',
        'vault_text_4': 'Ты именно тот человек, которого Алекс имел в виду.',
        'vault_quote': '«Система переживает пользователя. Информация переживает человека.»',
        'vault_author': '— Алекс Р., 12 декабря 2002, 03:47.',
        # vault denied
        'denied_access': 'доступ запрещён. неверный токен.',
        'denied_sub': 'хранилище знает, что ты ещё не заслужил.',
    },
    'uz': {
        'nav_home': 'bosh sahifa',
        'nav_about': 'men haqimda',
        'nav_music': 'musiqa',
        'nav_setup': 'sozlamam',
        'obituary': "Ushbu blog 2003 yil 3 yanvarda vafot etgan Aleks R. xotirasiga saqlanib qolgan. Uning do'sti Marko yozdi: <em>«Aleksning paroli doim dunyoda eng ko'p yaxshi ko'rgan narsasi bo'lgan.»</em> — Tinch yot, Aleks. Mashina eslab qoladi.",
        'footer_copy': "alex-r.local &copy; 2001-2003 &nbsp;|&nbsp; 800x600 da ko'rish tavsiya etiladi",
        'footer_visitors': 'tashrif buyuruvchilar',
        'section_posts': "so'nggi yozuvlar",
        'back': 'orqaga',
        'back_posts': 'barcha yozuvlarga',
        'logout': '[ chiqish ]',
        'no_comments': "hali izoh yo'q.",
        # about
        'about_section': 'men haqimda',
        'about_p1': "Men Aleks. 21 yoshdaman (2002 yildan). Sovuq bir joyda yashayman va vaqtimning ko'p qismini ekranlar oldida o'tkazaman. Dasturchi — instinkt bilan, kasb sifatida emas — hali.",
        'about_p2': "13 yoshimda otamning 386-sida kod yoza boshladim. Birinchi til BASIC, keyin C, hozir asosan Python qurish uchun va bash buzish uchun. 1998 yildan Linux foydalanuvchisi. Ikki tizimli yuklamani umuman qilmayman.",
        'about_p3': "Kod yozmasam, musiqa tinglayman. Mening dunyodagi eng sevimli guruhim —",
        'about_p3b': "16 yoshimda The Bends ni birinchi marta eshitganimdan beri shunday. Ularni jonli ikki marta ko'rdim. OK Computer — yozilgan eng buyuk albom. Bu muhokama qilinmaydi.",
        'about_p4': "Maxfiylik, shifrlash va ma'lumot erkin bo'lishi kerak degan g'oyaga ishonaman — lekin sirlar ularni saqlashga loyiq bo'lganlarda qolishi kerak.",
        'about_p5': "Bu blog 2001 yilda ovoz chiqarib o'ylash joyi sifatida boshlandi. Kim o'qishini bilmayman. Balki hech kim. Yaxshi.",
        'about_interests': 'qiziqishlarim',
        'about_i1': 'kriptografiya — klassik va zamonaviy',
        'about_i2': 'Linux tizim boshqaruvi',
        'about_i3': "tarmoq xavfsizligi (etik tur... asosan)",
        'about_i4': 'radiohead, portishead, massive attack, aphex twin',
        'about_i5': "ilmiy fantastika — xususan gibson, dick, lem",
        'about_i6': "havaskor radio (chaqirish belgisi: aytmayman)",
        'about_contact': 'aloqa',
        'about_c1': "Menda aloqa formi yo'q. Meni bilsang — qanday murojaat qilishni bilasan.",
        'about_c2': "Bilmasang — o'zing topib ol. Maqsad ham shu.",
        # admin
        'access_restricted': '[ KIRISH CHEKLANGAN ]',
        'admin_subtitle': 'admin paneli // faqat vakolatli foydalanuvchilar',
        'label_username': 'foydalanuvchi nomi',
        'label_password': 'parol',
        'btn_auth': 'kirish',
        'admin_footer_1': "yopiq zona. agar kirish ma'lumotlarini bilmasang,",
        'admin_footer_2': "bu yerda bo'lishing kerak emas.",
        'admin_footer_3': "yoki balki kerakdir. chuqurroq qazib ko'r.",
        'error_invalid': "Noto'g'ri kirish ma'lumotlari.",
        # diary
        'diary_section': "aleksning shaxsiy kundaliği",
        'diary_access_1': "Kirish ruxsat etildi. Bu fayllar Aleks tomonidan o'limidan oldin shifrlangan.",
        'diary_access_2': "Tarkib uning shaxsiy shifri bilan himoyalangan. Faqat uni haqiqatan bilganlar o'qiy oladi.",
        'diary_cipher_label': '// journal_entry_2002-12-12.enc — Vigenere shifri',
        'diary_hint_pre': "Shifr kaliti Aleks chuqur sevgan narsa. U bu haqda ko'p marta yozdi. Kalit harfi bilan boshlanadi",
        'diary_hint_post': "Uning uchun eng muhim bo'lgan narsa hech qachon sir bo'lmagan.",
        'diary_tools_1': '// Vigenere shifri: har bir harf kalit harfiga mos ravishda siljiydi.',
        'diary_tools_2': "// Kalit siklik ravishda takrorlanadi. Alifbo bo'lmagan belgilar o'zgarmaydi.",
        'diary_tools_3': '// Vositalar:',
        # vault
        'vault_title': '// KIRISH RUXSAT ETILDI //',
        'vault_sub': "siz aleksning seirini topdingiz &nbsp;|&nbsp; ajoyib ish",
        'vault_text_1': "Siz u yozgan hamma narsani o'qidingiz.",
        'vault_text_2': 'Siz git tarixini topdingiz.',
        'vault_text_3': 'Siz shifrni yechdingiz.',
        'vault_text_4': 'Siz aynan Aleks kutgan odam ekansiz.',
        'vault_quote': '«Tizim foydalanuvchidan uzoqroq yashaydi. Ma\'lumot insondan uzoqroq yashaydi.»',
        'vault_author': '— Aleks R., 2002 yil 12 dekabr. 03:47.',
        # vault denied
        'denied_access': "kirish rad etildi. noto'g'ri token.",
        'denied_sub': "seif hali bunga loyiq emasligingizni biladi.",
    },
}

POSTS = [
    {
        'id': 1,
        'slug': 'radiohead-ok-computer',
        'titles': {
            'en': 'Why OK Computer Changed My Life',
            'ru': 'Почему OK Computer изменил мою жизнь',
            'uz': 'Nima uchun OK Computer hayotimni o\'zgartirdi',
        },
        'dates': {
            'en': 'March 15, 2001',
            'ru': '15 марта 2001',
            'uz': '15 mart, 2001',
        },
        'contents': {
            'en': """
I was 19 when I first heard OK Computer. My roommate played it through these terrible PC speakers,
and I sat there for 47 minutes not moving. Radiohead does something to your brain that I can't explain.

Thom Yorke writes about paranoia, technology, and alienation like someone who actually gets it.
Every time I'm deep in a coding session at 3am and the world feels like a simulation,
I put on Paranoid Android and everything makes sense again.

If I could listen to only one album for the rest of my life, this would be it.
No question. Radiohead is more than a band — it's a state of mind.

Favorite tracks, in order: Exit Music (For A Film), No Surprises, Karma Police.
Though honestly every track is perfect. There are no skips.

Anyone who says Kid A is better is wrong. (I say this with love, Kid A is also incredible.)
            """,
            'ru': """
Мне было 19, когда я впервые услышал OK Computer. Сосед по комнате включил его через ужасные компьютерные колонки,
и я просидел там 47 минут, не шевелясь. Radiohead делает с твоим мозгом что-то необъяснимое.

Том Йорк пишет о паранойе, технологиях и отчуждении как человек, который действительно всё понимает.
Каждый раз, когда я глубоко погружаюсь в код в 3 ночи и мир кажется симуляцией,
я включаю Paranoid Android — и всё встаёт на свои места.

Если бы я мог слушать только один альбом всю оставшуюся жизнь — это был бы он.
Без вопросов. Radiohead — это больше чем группа. Это состояние ума.

Любимые треки, по порядку: Exit Music (For A Film), No Surprises, Karma Police.
Хотя честно — каждый трек идеален. Ни одного лишнего.

Тот, кто говорит, что Kid A лучше — ошибается. (Говорю это с любовью, Kid A тоже невероятен.)
            """,
            'uz': """
OK Computer ni birinchi marta eshitganimda 19 yoshda edim. Xona sherigi uni dahshatli kompyuter karnaylari orqali qo'ydi,
va men 47 daqiqa qimirlamasdan o'tirdim. Radiohead miyangga tushuntirib bo'lmaydigan narsa qiladi.

Tom Yorke paranoya, texnologiya va begonalashuv haqida buni chindan tushunadigan odamdek yozadi.
Har safar tunda soat 3 da kod yozishga chuqur sho'ng'iganimda va dunyo simulatsiyaga o'xshab ko'ringanda,
Paranoid Android ni qo'yaman — va hamma narsa joyiga tushadi.

Hayotimning qolgan qismida faqat bitta albom tinglashim kerak bo'lsa — bu bo'lardi.
Hech shubhasiz. Radiohead — bu guruhdan ko'proq narsa. Bu ong holati.

Sevimli treklarim, tartibda: Exit Music (For A Film), No Surprises, Karma Police.
Garchi rostini aytsam — har bir trek mukammal. Hech biri ortiqcha emas.

Kid A yaxshiroq deydiganlar yanglishadi. (Buni muhabbat bilan aytaman, Kid A ham ajoyib.)
            """,
        },
        'comments': {
            'en': [
                {'author': 'marco_dev', 'text': 'bro ur obsessed lmao. but yeah ok computer hits different at 3am'},
                {'author': 'h4ck3rg1rl_99', 'text': 'finally someone with taste on this website'},
            ],
            'ru': [
                {'author': 'marco_dev', 'text': 'бро ты одержимый лмао. но да, ok computer по другому звучит в 3 ночи'},
                {'author': 'h4ck3rg1rl_99', 'text': 'наконец-то кто-то со вкусом на этом сайте'},
            ],
            'uz': [
                {'author': 'marco_dev', 'text': 'bro sen maftun bo\'libsan lmao. lekin ha, ok computer soat 3 da boshqacha yangraydi'},
                {'author': 'h4ck3rg1rl_99', 'text': 'nihoyat bu saytda did bor odam topildi'},
            ],
        },
    },
    {
        'id': 2,
        'slug': 'vigenere-cipher',
        'titles': {
            'en': 'Vigenere Cipher: Elegant and Underrated',
            'ru': 'Шифр Виженера: элегантный и недооценённый',
            'uz': 'Vigenere shifri: nafis va kam baholangan',
        },
        'dates': {
            'en': 'March 22, 2002',
            'ru': '22 марта 2002',
            'uz': '22 mart, 2002',
        },
        'contents': {
            'en': """
Been playing around with classical cryptography lately. Everyone knows Caesar cipher,
but not enough people appreciate Vigenere.

The beauty of Vigenere is how the key determines everything.
Without the right key, the ciphertext looks like random gibberish.
But with the right key — perfect clarity.

I've started using it for my personal notes. Nothing sensitive, just as an exercise.
The trick is choosing a key that's meaningful to you but hard for others to guess.
Mine is something I love deeply. Something anyone who knows me well would immediately think of.

If you ever find my encrypted notes somewhere, you already know enough about me to decrypt them.
That's the point. Only someone who truly knows me could read them.

Vigenere: my favorite cipher for personal use.
            """,
            'ru': """
В последнее время играюсь с классической криптографией. Шифр Цезаря знают все,
но шифр Виженера ценят недостаточно.

Красота Виженера в том, что ключ определяет всё.
Без правильного ключа шифртекст выглядит как случайная абракадабра.
Но с правильным ключом — полная ясность.

Я начал использовать его для личных заметок. Ничего секретного, просто как упражнение.
Хитрость в том, чтобы выбрать ключ, значимый для тебя, но трудный для угадывания другими.
Мой — это то, что я люблю по-настоящему. То, о чём сразу подумает каждый, кто хорошо меня знает.

Если ты когда-нибудь найдёшь мои зашифрованные заметки, ты уже знаешь обо мне достаточно, чтобы их расшифровать.
В этом и смысл. Прочесть их сможет только тот, кто действительно меня знает.

Виженер: мой любимый шифр для личного использования.
            """,
            'uz': """
Yaqinda klassik kriptografiya bilan o'ynayman. Tsezar shifrini hamma biladi,
lekin Vigenere ni yetarlicha qadrlamaydilar.

Vigenere ning go'zalligi — kalit hamma narsani belgilaydi.
To'g'ri kalit bo'lmasa, shifrlangan matn tasodifiy safsata kabi ko'rinadi.
Lekin to'g'ri kalit bilan — mukammal aniqlik.

Uni shaxsiy yozuvlarim uchun ishlatishni boshladim. Hech narsa maxfiy emas, shunchaki mashq.
Hiyla — siz uchun mazmunli, boshqalar uchun taxmin qilish qiyin kalit tanlash.
Meniki — chuqur sevadigan narsam. Meni yaxshi biladigan har bir kishi darhol o'ylaydi.

Agar siz biror joyda mening shifrlangan yozuvlarimni topsangiz, ularni ochish uchun men haqimda yetarlicha bilasiz.
Maqsad shu. Faqat meni chindan biladigan kishi o'qiy oladi.

Vigenere: shaxsiy foydalanish uchun sevimli shifrim.
            """,
        },
        'comments': {
            'en': [
                {'author': 'cr4ck3r_jack', 'text': 'vigenere is breakable tho, look up kasiski test'},
                {'author': 'alex_r', 'text': 'yeah but my key is personal enough that frequency analysis wont save you ;)'},
            ],
            'ru': [
                {'author': 'cr4ck3r_jack', 'text': 'виженер всё равно взламывается, погугли тест Касиски'},
                {'author': 'alex_r', 'text': 'да, но мой ключ достаточно личный, чтобы частотный анализ тебя не спас ;)'},
            ],
            'uz': [
                {'author': 'cr4ck3r_jack', 'text': 'vigenere buziladi lekin, kasiski testini qidiring'},
                {'author': 'alex_r', 'text': 'ha lekin mening kalitim shunchalik shaxsiyki, chastotali tahlil sizni qutqara olmaydi ;)'},
            ],
        },
    },
    {
        'id': 3,
        'slug': 'ghost-in-the-machine',
        'titles': {
            'en': 'Ghost in the Machine',
            'ru': 'Призрак в машине',
            'uz': 'Mashinadagi arvoh',
        },
        'dates': {
            'en': 'December 10, 2002',
            'ru': '10 декабря 2002',
            'uz': '10 dekabr, 2002',
        },
        'contents': {
            'en': """
Late night. December. The kind of cold that makes the computer fans sound louder than usual.

I've been thinking a lot about legacy lately. What happens to your digital life after you're gone?
Your files, your projects, your little encrypted notes with things you never said out loud.

I set up something today. A kind of digital time capsule. Hidden, but findable.
For the right person. Someone curious enough, patient enough.

If you're the type who reads robots.txt, checks git history, stares at ciphertext until it breaks —
you'll know what I mean. You're already one of us.

The ghost in the machine isn't a ghost. It's just information, waiting.

- A.
            """,
            'ru': """
Поздняя ночь. Декабрь. Такой холод, что вентиляторы компьютера звучат громче обычного.

Последнее время много думаю о наследии. Что происходит с твоей цифровой жизнью после того, как тебя не станет?
Твои файлы, проекты, маленькие зашифрованные заметки с тем, что ты никогда не говорил вслух.

Сегодня я кое-что настроил. Своеобразная цифровая капсула времени. Скрытая, но найти её можно.
Для нужного человека. Достаточно любопытного, достаточно терпеливого.

Если ты из тех, кто читает robots.txt, проверяет историю git, смотрит на шифртекст, пока он не сломается —
ты поймёшь, о чём я. Ты уже один из нас.

Призрак в машине — не призрак. Это просто информация, которая ждёт.

- А.
            """,
            'uz': """
Kech tun. Dekabr. Kompyuter fanatlarini odatdagidan balandroq eshitiladigan qiladigan sovuq.

Yaqinda meros haqida ko'p o'ylayman. O'lib ketganingdan keyin raqamli hayotingga nima bo'ladi?
Fayllar, loyihalar, hech qachon ovoz chiqarib aytmagan narsalaringdagi kichik shifrlangan yozuvlar.

Bugun bir narsa o'rnatdim. Bir turdagi raqamli vaqt kapsulasi. Yashirin, lekin topish mumkin.
To'g'ri odam uchun. Yetarlicha qiziquvchan, yetarlicha sabr-toqatli.

Agar siz robots.txt o'qiydigan, git tarixini tekshiradigan, shifrlangan matnga u sinmaguncha tikilgan turdan bo'lsangiz —
nima demoqchiligimni tushunasiz. Siz allaqachon bizdan birisiz.

Mashinadagi arvoh — arvoh emas. Bu shunchaki kutayotgan ma'lumot.

- A.
            """,
        },
        'comments': {
            'en': [
                {'author': 'marco_dev', 'text': 'bro you sound like youre writing a will lol. stop being dramatic'},
                {'author': 'alex_r', 'text': 'maybe i am. anyway. listen to more radiohead'},
            ],
            'ru': [
                {'author': 'marco_dev', 'text': 'бро ты звучишь как будто пишешь завещание лол. хватит драматизировать'},
                {'author': 'alex_r', 'text': 'может, и пишу. ладно. слушай больше radiohead'},
            ],
            'uz': [
                {'author': 'marco_dev', 'text': 'bro vasiyatnoma yozayotganga o\'xshaysan lol. dramatik bo\'lishni bas qil'},
                {'author': 'alex_r', 'text': "balki shundaydirman. xullas. ko'proq radiohead ting'la"},
            ],
        },
    },
    {
        'id': 4,
        'slug': 'my-setup',
        'titles': {
            'en': 'Current Setup',
            'ru': 'Моё железо',
            'uz': 'Mening sozlamam',
        },
        'dates': {
            'en': 'June 1, 2002',
            'ru': '1 июня 2002',
            'uz': '1 iyun, 2002',
        },
        'contents': {
            'en': """
Everyone's doing setup posts now, so here's mine:

Machine: Self-built tower, Athlon XP 1800+, 512MB RAM
OS: Debian GNU/Linux (with a Windows partition I boot into approximately never)
Editor: vim. Always vim.
Music: Winamp with Radiohead on infinite shuffle
Desk: IKEA. Two monitors. One for code, one for... also code.
Chair: Whatever this is. My back hurts constantly.

I keep my important files encrypted. Paranoid? Maybe.
But paranoia is just pattern recognition taken seriously.

Currently working on a small web project. Flask-based.
Don't ask me about it — if it ever goes live, you'll know.

Stay curious.
            """,
            'ru': """
Все сейчас пишут посты про своё железо, вот и моё:

Машина: самосборная башня, Athlon XP 1800+, 512 МБ ОЗУ
ОС: Debian GNU/Linux (с разделом Windows, который я загружаю примерно никогда)
Редактор: vim. Всегда vim.
Музыка: Winamp с Radiohead на бесконечном перемешивании
Стол: IKEA. Два монитора. Один для кода, другой для... тоже кода.
Кресло: Что бы это ни было. Спина болит постоянно.

Важные файлы храню зашифрованными. Паранойя? Возможно.
Но паранойя — это просто распознавание паттернов, воспринятое всерьёз.

Сейчас работаю над небольшим веб-проектом. На Flask.
Не спрашивай — если он когда-нибудь выйдет, ты узнаешь.

Будь любопытным.
            """,
            'uz': """
Hamma hozir sozlama haqida yozmoqda, meni ham:

Mashina: O'zim yig'ilgan minora, Athlon XP 1800+, 512MB RAM
OS: Debian GNU/Linux (taxminan hech qachon yuklamaydigan Windows bo'limi bilan)
Muharrir: vim. Doim vim.
Musiqa: Winamp da Radiohead cheksiz aralashtirib
Stol: IKEA. Ikki monitor. Biri kod uchun, ikkinchisi... ham kod uchun.
Kreslo: Bu nima bo'lsa. Belim doim og'riydi.

Muhim fayllarimni shifrlangan saqlaman. Paranoya? Balki.
Lekin paranoya — bu jiddiy qabul qilingan naqsh tanish.

Hozir kichik veb loyiha ustida ishlayman. Flask asosida.
So'rama — agar u biror kun chiqsa, bilasan.

Qiziquvchan bo'ling.
            """,
        },
        'comments': {
            'en': [],
            'ru': [],
            'uz': [],
        },
    },
]


def vigenere_encrypt(text, key):
    result = []
    key = key.lower()
    ki = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - ord('a')
            if c.isupper():
                result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
            ki += 1
        else:
            result.append(c)
    return ''.join(result)


DIARY_PLAIN = """\
== Personal Journal - Alex R. ==
== December 12, 2002 ==

Another late night. The wind outside sounds like white noise through my headphones.
Radiohead on loop. Specifically OK Computer. Track six. Again and again.

I have decided to leave something behind. A trail.
Only for someone who truly wants to find it.
Someone who reads everything, trusts nothing, questions everything.

If you have come this far - you found my blog, my git history, you logged in -
then you deserve the last piece.

Navigate to the secret path: /vault?token=gh0st_1n_th3_m4ch1n3

Good luck. And remember: we are all ghosts in the machine.
The system outlives the user. The information outlives the person.

- Alex R.
December 12, 2002. 03:47 AM.
"""

DIARY_CIPHER = vigenere_encrypt(DIARY_PLAIN, VIGENERE_KEY)


def get_lang():
    lang = session.get('lang', 'en')
    if lang not in SUPPORTED_LANGS:
        lang = 'en'
    return lang


def get_post_for_lang(post, lang):
    return {
        'id': post['id'],
        'slug': post['slug'],
        'title': post['titles'].get(lang, post['titles']['en']),
        'date': post['dates'].get(lang, post['dates']['en']),
        'content': post['contents'].get(lang, post['contents']['en']),
        'comments': post['comments'].get(lang, post['comments']['en']),
    }


@app.route('/lang/<code>')
def set_lang(code):
    if code in SUPPORTED_LANGS:
        session['lang'] = code
    return redirect('/')


@app.route('/')
def index():
    if 'lang' not in session:
        return render_template('lang_select.html')
    lang = get_lang()
    t = TRANSLATIONS[lang]
    posts = [get_post_for_lang(p, lang) for p in POSTS]
    return render_template('index.html', posts=posts, t=t, lang=lang)


@app.route('/about')
def about():
    lang = get_lang()
    t = TRANSLATIONS[lang]
    return render_template('about.html', t=t, lang=lang)


@app.route('/post/<slug>')
def post(slug):
    lang = get_lang()
    t = TRANSLATIONS[lang]
    p_raw = next((p for p in POSTS if p['slug'] == slug), None)
    if not p_raw:
        return render_template('404.html', t=t, lang=lang), 404
    p = get_post_for_lang(p_raw, lang)
    return render_template('post.html', post=p, t=t, lang=lang)


@app.route('/robots.txt')
def robots():
    return Response(
        "User-agent: *\nDisallow: /admin-1337\nDisallow: /vault\n",
        mimetype='text/plain'
    )


@app.route('/.git/<path:filename>')
def git_files(filename):
    git_dir = os.path.join(app.root_path, '.git')
    return send_from_directory(git_dir, filename)


@app.route('/admin-1337', methods=['GET', 'POST'])
def admin():
    lang = get_lang()
    t = TRANSLATIONS[lang]
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect('/diary')
        else:
            error = t['error_invalid']
    return render_template('admin.html', error=error, t=t, lang=lang)


@app.route('/diary')
def diary():
    if not session.get('logged_in'):
        return redirect('/admin-1337')
    lang = get_lang()
    t = TRANSLATIONS[lang]
    return render_template('diary.html', ciphertext=DIARY_CIPHER, key_hint=VIGENERE_KEY[0], t=t, lang=lang)


@app.route('/vault')
def vault():
    lang = get_lang()
    t = TRANSLATIONS[lang]
    token = request.args.get('token', '')
    if token == VAULT_TOKEN:
        return render_template('vault.html', flag=FLAG, t=t, lang=lang)
    return render_template('vault_denied.html', t=t, lang=lang), 403


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5021)), debug=False)
