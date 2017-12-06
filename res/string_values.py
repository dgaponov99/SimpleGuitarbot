"""Константные строковые значения для пользователя"""

cpt_tuner = 'Нота Ля первой октавы (440Hz)'
not_found_chord = 'В нашей базе нет такого аккорда'
description = 'Для получения информации о боте воспользуйтесь командой /help'
hello = 'Здравствуйте, '
text_inline_button = 'Аккорд не найден\nЕсли такой аккорд существует, то Вы можете отправить его нам на рассмотрение'
update = 'Обновление базы...'
update_complete = 'Обновление базы завершено\nПриносим извинения за ожидание'
to_offer = 'Отправить'
not_exist = 'Такого аккорда не существует'
message_to_admins = 'Пользователь {} (chat_id={}) отправил на рассмотрение аккорд {}'

# -----------------------------------------------------------------------------------------

help_description = """Наш бот создан для помощи начинающим (и не только) <i>гитаристам</i> и <i>укулелистам</i> (укулельщикам???)
Теперь Вам не нужно в очередной раз гуглить аккорд и искать его на множестве сайтов в нужной форме, достаточно отправить название нужного вам аккорда нашему боту и Вы увидите все возможные его представления.

Также у нас есть несколько других полезных командочек:
• /tuner - камертон для ненавистников мобильных тюнеров (для Димы)
• /tutorial_image - выводит список командочек, каждая из которых поможет Вам научиться чему-нибудь
• /experience - немного разговоров о жизни

В будущем мы хотим научить нашего бота показывать аккорды для укулеле, сохранять ваши любимые аккорды, быстрее работать и нормально шутить.
"""

# -----------------------------------------------------------------------------------------

tutorial = """ Доступные туториалы:
• /care - уход за гитарой
• /parts - названия частей гитары
• /tuning - настройка шестиструнной гитары
• /tuning_uku - настройка укулеле
"""

# -----------------------------------------------------------------------------------------

tuning = """<b>Стандартный строй гитары:</b>
1 струна (самая тонкая) - E (Ми)
2 струна - B (Си)
3 струна - G (Соль)
4 струна - D (Ре)
5 струна - A (Ля)
6 струна - E (Ми) 

<b>Настройка гитары:</b>
<i>(ОСТОРОЖНО! ОЧЕНЬ СЛОЖНО, НЕ ВЕРЬТЕ НАЗВАНИЮ)</i>
<b>Первый шаг</b> - настроить 1-ую струну:
Зажимаем первую струну на пятом ладу (1 струна, зажатая на пятом ладу должна исполнять ноту Ля (номера ладов считаются от головы грифа)) и извлекаем из нее звук, он должен быть в унисон (одинаково звучать) с камертоном (/tuner). 

<b>Второй шаг</b> - вторая струна:
Будем настраивать по открытой первой струне. Зажимаем вторую струну на пятом ладу и щипаем открытую первую и зажатую вторую струны одновременно или поочередно, подтягивая вторую, пока они не будут звучать в унисон (одинаково).

<b>Третий шаг</b> - третья струна (неожиданно):
Будем ее настраивать по второй открытой. Зажимаем третью струну на четвертом ладу (все портит, остальные на пятом, мне она всегда не нравилась) и щипаем открытую вторую и зажатую третью струны одновременно или поочередно, подтягивая третью струну пока они не будут звучать в унисон (одинаково). 

<b>Четвертый шаг</b> - четвертая струна:
Настраивается по третьей открытой струне. Зажимаем четвертую струну на пятом ладу и повторяем описанные ранее действия с нашей струной, пока они не будут звучать в унисон (надеюсь, что Вы уже запомнили, что это значит одинаково). 

<b>Пятый шаг</b> - пятая струна:
Будем ее настраивать по четвертой открытой. Зажимаем пятую струну на пятом ладу и, да-да, повторяем все то же самое, что и раньше. 

<b>Шестой шаг</b> - угадайте какая струна:
Шестая струна - самая толстая струна. Зажимаем шестую струну на пятом ладу и повторяем все опять, день сурка.
"""

# -----------------------------------------------------------------------------------------

tuning_ukulele = """<b>Стандартный строй укулеле:</b>
1 струна (которая снизу) - A (Ля)
2 струна - E (Ми)
3 струна - С (До)
4 струна - G (Соль)

<b>Настройка укулеле:</b>
<i>(немного легче, чем на гитаре)</i>
<b>Первый шаг</b> - первая струна:
Настройте первую струну на ноту A (Ля) при помощи камертона (/tuner) так точно, как можете.

<b>Второй шаг</b> - вторая струна:
Зажмите пятый лад второй струны (хммм, что-то мне это напоминает) и настройте ее звучание в соответствии со звучанием первой струны.

<b>Третий шаг</b> - третья струна:
4-й лад 3-й струны должен звучать так же, как и свободная 2-я струна.

<b>Четвертый шаг</b> - четвертая струна:
2-й лад 4-й струны должен звучать так же, как свободная 1-я струна. 
"""

# -----------------------------------------------------------------------------------------

care = """<b>Уход за гитарой.</b>
<b>1. Чистка струн.</b> 
Здесь мы должны, в первую очередь, очистить грязь со струн, т.к. она  сокращает их колебания. Последствие этого - плохой звук. Чтобы этого избежать, нужно каждый раз после игры протирать струны сухим и чистым хлопковым платком или тряпочкой.

<b>2. Чистка грифа.</b> 
Чтобы прочистить гриф гитары, используйте небольшое количество лимонного масла, нанесенное на ткань из микрофибры. Делать это нужно время от времени, а также тогда, когда вы меняете струны. 
ЗАПОМНИТЕ: вместо того, чтобы продевать ткань под струны, лучше всего их снимать и чистить поочерёдно. Если их снять все сразу, то можно вызвать искривление грифа из-за резкого падения натяжения. 

<b>3. Влияние температур.</b> 
Чувствительная и пористая структура дерева, климатические изменения, колебания температуры и влажность могут влиять на то, как инструмент звучит. Стоит обеспечить комфортные условия для гитары, не позволяя ей сильно нагреваться или охлаждаться. Оптимальная влажность для инструмента: от 40 до 60%. 

<b>4. Безопасность.</b> 
Всегда храните гитару в чехле, потому что он уменьшает воздействие окружающей среды на инструмент и защищает его от загрязнений во время путешествий.
"""

# -----------------------------------------------------------------------------------------


experience = """Здесь нет описаний, как ставить баре или играть какой-либо бой, только немного личного опыта и моих ужасных шуток.
Научиться играть на гитаре можно в домашних условиях, не навредив себе и окружающим (но это не точно). 

Несколько песенок, которые заставят Вас попотеть, но вы научитесь чему-нибудь:
<b>1. Shoking Blue - Venus</b> - чтобы добиться чего-то похожего на оригинальное звучание, придется попотеть над боем.
<b>2. Валентин Стрыкало - Дешевые драмы</b> - удивительно, но даже у Стрыкало есть песни, которые могут чему-то научить, например, как быстро менять положение своих пальцев и попадать в бой.
<b>3. Дайте танк(!) - Хомилия (с придыханием)/Утро/Гореть</b> - бой, бой и еще раз бой.
<b>4. Twenty One Pilots - The Judge</b> - для укулеле. Подберите ритм, пока  Тайлер Джозеф читает.
<b>5. The Retuses - Синий вечер</b> - для укулеле в оригинальной тональности. Разомните свои пальчики или умрите.

<b>Несколько советов:</b>
1. Видео-уроки или down-down-up-down-up.
2. Играть синхронно с песнями.
3. Роксмит (если у вас есть электрогитара, лишние 700 рублей на игру и 3000 на провод)
4. Необязательно начинать с простых песен, одной-двух для разгона будет достаточно. 
И удачи
"""
