def get_profs():
    profs = ['Аварийный комиссар', 'Авиамеханик', 'Автомаляр', 'Авторазборщик', 'Автослесарь', 'Автоэксперт',
             'Автоэлектрик', 'Агент по организации обслуживания пассажиров', 'Агент по сбыту энергии', 'Агроном',
             'Адвокат', 'Администратор', 'Актер, актриса', 'Акушер', 'Аналитик', 'Аниматор', 'Аппаратчик',
             'Арматурщик', 'Арт-директор', 'Артист', 'Архивариус', 'Архитектор', 'Ассистент', 'Асфальтобетонщик',
             'Аудитор', 'Балетмейстер', 'Банщик', 'Бариста', 'Бармен', 'Бетонщик', 'Библиотекарь', 'Биолог', 'Боец',
             'Боцман', 'Бригадир', 'Бурильщик', 'Буфетчик', 'Буфетчик судовой', 'Бухгалтер', 'Вальщик леса, лесоруб',
             'Варщик пищевого сырья и продуктов', 'Вахтер', 'Ведущий мероприятий', 'Ведущий специалист-эксперт',
             'Верстальщик', 'Весовщик', 'Взрывник', 'Видеограф', 'Визажист', 'Водитель', 'Водолаз',
             'Военнослужащий по контракту', 'Вожатый', 'Вожатый служебных собак', 'Воспитатель', 'Врач',
             'Вулканизаторщик', 'Габионщик', 'Газорезчик', 'Газосварщик', 'Гальваник', 'Гардеробщик', 'Геодезист',
             'Геолог', 'Гигиенист стоматологический', 'Гид, экскурсовод', 'Гидравлист', 'Гидрогеолог', 'Гидротехник',
             'Гладильщик', 'Горнорабочий', 'Горный мастер', 'Гример', 'Грузчик', 'Грумер', 'Гувернантка, гувернер',
             'Гуммировщик', 'Дворник', 'Дежурный бюро пропусков', 'Дежурный по переезду', 'Дезинфектор',
             'Декларант, таможенный брокер', 'Декоратор', 'Делопроизводитель', 'Детейлер', 'Дефектолог', 'Диджей',
             'Дизайнер', 'Диктор', 'Дилер', 'Директор', 'Диспетчер', 'Дневальный', 'Дознаватель', 'Докер-механизатор',
             'Докмейстер', 'Документовед', 'Домработница, домработник', 'Донкерман', 'Дорожный мастер',
             'Дорожный рабочий', 'Доярка, дояр', 'Дробильщик', 'Жаровщик', 'Жестянщик', 'Животновод', 'Жиловщик мяса',
             'Журналист', 'Заведующий', 'Загрузчик-выгрузчик', 'Закройщик', 'Замерщик', 'Заместитель', 'Заправщик АЗС',
             'Заточник', 'Зооняня, рабочий по уходу за животными', 'Зоотехник', 'Изготовитель мармелада', 'Изолировщик',
             'Инженер', 'Инкассатор', 'Инспектор', 'Инспектор службы безопасности',
             'Инспектор транспортной безопасности', 'Инструктор', 'Интервьюер', 'Интернет-маркетолог', 'Ихтиолог',
             'Кабельщик', 'Казначей', 'Кальянщик', 'Каменщик', 'Капитан', 'Кассир', 'Кастелянша, заведующий бельевой',
             'Кинолог', 'Кладовщик', 'Колорист', 'Кольщик дров', 'Комендант', 'Комплектовщик', 'Компрессорщик',
             'Кондитер', 'Консультант', 'Консьерж', 'Контролер', 'Конюх', 'Координатор', 'Копирайтер', 'Коптильщик',
             'Коренщик', 'Корреспондент', 'Косильщик', 'Косметик-эстетист', 'Косметолог', 'Костюмер', 'Котлочист',
             'Кочегар', 'Кредитный специалист', 'Кредитный эксперт', 'Кровельщик', 'Крупье', 'Кузнец', 'Кузовщик',
             'Курьер', 'Кухонный работник', 'Лаборант', 'Лепщик полуфабрикатов', 'Лифтер', 'Логист', 'Макетчик',
             'Маляр', 'Маркетолог', 'Маркировщик', 'Маркшейдер', 'Массажист', 'Мастер буровой', 'Мастер депиляции',
             'Мастер контрольный', 'Мастер лесозаготовок', 'Мастер ногтевого сервиса', 'Мастер общестроительных работ',
             'Мастер отделочных работ', 'Мастер по добыче', 'Мастер по изготовлению ключей',
             'Мастер по наращиванию волос', 'Мастер по наращиванию ресниц', 'Мастер по обработке камня',
             'Мастер по обработке рыбы', 'Мастер по перетяжке салонов автомобилей', 'Мастер по ремонту',
             'Мастер по удалению вмятин без покраски', 'Мастер по эксплуатации', 'Мастер погрузочно-разгрузочных работ',
             'Мастер производства', 'Мастер производственного обучения', 'Мастер СМР', 'Мастер татуировки',
             'Мастер участка', 'Мастер цеха', 'Мастер-бровист', 'Математик', 'Матрос', 'Машинист',
             'Медицинский представитель', 'Медицинский статистик', 'Медрегистратор', 'Медсестра, медбрат', 'Менеджер',
             'Мерчендайзер', 'Методист', 'Метролог', 'Механизатор', 'Механик', 'Микробиолог', 'Модель', 'Модельер',
             'Модератор', 'Мойщик', 'Монтажник', 'Монтер пути', 'Монтировщик сцены', 'Мотомеханик', 'Моторист',
             'Музыкальный работник', 'Музыкальный руководитель', 'Музыкант', 'Мясник', 'Наблюдатель', 'Наладчик',
             'Натурщик', 'Няня', 'Обвальщик', 'Обивщик', 'Овощевод', 'Огнеупорщик', 'Озеленитель', 'Оклейщик',
             'Оперативный дежурный', 'Оператор', 'Операционист', 'Оперуполномоченный', 'Оптик', 'Организатор',
             'Осветитель, светотехник', 'Осеменатор', 'Осмотрщик вагонов', 'Отделочник', 'Официант', 'Охотовед',
             'Охранник', 'Оценщик', 'Парикмахер', 'Парковщик', 'Пастух', 'Педагог', 'Пекарь', 'Переводчик',
             'Переплетчик', 'Пескоструйщик', 'Печатник', 'Печник', 'Пивовар', 'Плиточник', 'Плотник', 'Повар',
             'Подготовитель пищевого сырья и материалов', 'Пожарный', 'Полировщик', 'Полицейский', 'Помощник',
             'Портной', 'Постпечатник', 'Почтальон', 'Правильщик', 'Прачечник', 'Представитель банка', 'Преподаватель',
             'Пресс-секретарь', 'Прессовщик', 'Приемосдатчик груза и багажа', 'Приемщик', 'Пробоотборщик', 'Провизор',
             'Программист', 'Продавец', 'Проектировщик', 'Промоутер', 'Промышленный альпинист', 'Прораб', 'Психолог',
             'Птицевод', 'Птичница, птичник', 'Пчеловод', 'Работник производственного цеха', 'Работник торгового зала',
             'Рабочий', 'Радист', 'Рамщик', 'Раскройщик', 'Распиловщик', 'Распространитель', 'Растениевод', 'Ревизор',
             'Региональный представитель', 'Регистратор', 'Регулировщик радиоэлектронной аппаратуры',
             'Регулировщик скорости движения вагонов', 'Редактор', 'Режиссер', 'Резчик', 'Рентгенолаборант',
             'Репетитор', 'Респондент', 'Реставратор', 'Референт', 'Рефмашинист', 'Ритуальный агент',
             'Рихтовщик кузовов', 'Руководитель, начальник', 'Рыбак', 'Рыбообработчик', 'Садовник', 'Санитар',
             'Сборщик', 'Сварщик', 'Сверловщик', 'Секретарь', 'Сервисный консультант', 'Сетевязальщик', 'Сиделка',
             'Системный администратор', 'Следователь', 'Слесарь', 'Сливщик-разливщик', 'Сметчик', 'Смотритель',
             'Сомелье, кавист', 'Сопровождающий', 'Сортировщик', 'Составитель поездов', 'Составитель фарша',
             'Сотрудник линии раздачи', 'Социолог', 'Спасатель', 'Специалист аппарата мирового судьи', 'Специалист АХО',
             'Специалист информационного отдела', 'Специалист казначейства',
             'Специалист контрольно-ревизионного отдела', 'Специалист отдела безналичных расчетов',
             'Специалист отдела информатизации', 'Специалист отдела кадров',
             'Специалист отдела поддержки кредитных операций', 'Специалист отдела розничного бизнеса',
             'Специалист отдела сбыта', 'Специалист отдела технического сопровождения',
             'Специалист отдела технологического присоединения', 'Специалист отдела тылового обеспечения',
             'Специалист паспортного стола', 'Специалист по взысканию задолженности / Коллектор',
             'Специалист по госзакупкам', 'Специалист по гостеприимству',
             'Специалист по гражданской обороне и чрезвычайным ситуациям', 'Специалист по замене масла',
             'Специалист по защите информации', 'Специалист по земельным и имущественным отношениям',
             'Специалист по изготовлению мебели', 'Специалист по изготовлению наружной рекламы',
             'Специалист по изготовлению стеклопакетов', 'Специалист по информационной безопасности',
             'Специалист по качеству обслуживания', 'Специалист по коррекции фигуры',
             'Специалист по маркетинговым коммуникациям', 'Специалист по налогообложению',
             'Специалист по настройке CRM-систем', 'Специалист по обслуживанию',
             'Специалист по обслуживанию юридических лиц', 'Специалист по организации мультимодальных перевозок',
             'Специалист по отчетности', 'Специалист по охране труда', 'Специалист по оценке залогового имущества',
             'Специалист по пластиковым картам', 'Специалист по работе с детьми', 'Специалист по работе с населением',
             'Специалист по работе с поставщиками', 'Специалист по работе с семьей', 'Специалист по развал-схождению',
             'Специалист по ремонту автостекол', 'Специалист по ремонту топливной аппаратуры',
             'Специалист по ремонту трансмиссии', 'Специалист по ремонту ходовой части',
             'Специалист по рефинансированию', 'Специалист по сбору информации', 'Специалист по социальной работе',
             'Специалист по тендерам', 'Специалист по укладке тротуарной плитки, брусчатки',
             'Специалист по урегулированию убытков', 'Специалист по учебно-методической работе',
             'Специалист по химчистке', 'Специалист по электронным торгам', 'Специалист сервисного обслуживания',
             'Специалист службы безопасности', 'Специалист службы информации', 'Специалист строительного контроля',
             'Специалист технической поддержки', 'Специалист фрахтового отдела', 'Специалист юридического отдела',
             'Специалист-эксперт', 'Станочник', 'Стекольщик', 'Стивидор', 'Стилист', 'Столяр', 'Сторож',
             'Страховой агент', 'Стрелок', 'Стяжечник', 'Су-шеф', 'Судебный пристав', 'Судебный эксперт',
             'Судоводитель', 'Судовой агент', 'Судокорпусник-ремонтник', 'Судостроитель-судоремонтник',
             'Супервайзер', 'Суперинтендант', 'Сценарист', 'Сюрвейер', 'Тайный покупатель', 'Такелажник',
             'Тальман', 'Танцовщица, танцовщик', 'Телохранитель', 'Теплотехник', 'Термист',
             'Территориальный представитель', 'Тестировщик', 'Тестовод', 'Тестомес-формовщик', 'Техник',
             'Техник зубной', 'Техник-архитектор', 'Техник-лаборант', 'Технический специалист', 'Технический тренер',
             'Технолог', 'Товаровед', 'Токарь', 'Тонировщик', 'Торговый агент', 'Торговый представитель',
             'Транспортировщик', 'Тренер', 'Трубопроводчик судовой', 'Тьютор', 'Уборщик, горничная', 'Укладчик',
             'Упаковщик', 'Управляющий', 'Установщик', 'Участковый уполномоченный полиции', 'Учетчик', 'Учитель',
             'Фактуровщик', 'Фармацевт', 'Фасовщик', 'Фельдшер', 'Физик', 'Финансист', 'Финансовый консультант',
             'Фискарист', 'Флорист', 'Формовщик', 'Фотограф', 'Фрезеровщик', 'Химик', 'Хореограф', 'Хостес',
             'Художник', 'Чистильщик', 'Чокеровщик', 'Швея', 'Шиномонтажник', 'Шлифовщик', 'Штукатур', 'Штурман',
             'Эккаунт-менеджер', 'Эколог', 'Экономист', 'Экспедитор', 'Электрик', 'Электрогазосварщик',
             'Электромеханик', 'Электромонтажник', 'Электромонтер', 'Электрорадионавигатор', 'Электросварщик',
             'Электрослесарь', 'Энергетик', 'Ювелир', 'Юрисконсульт', 'Юрист']
    return profs