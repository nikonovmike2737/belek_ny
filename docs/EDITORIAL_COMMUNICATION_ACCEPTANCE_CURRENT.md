# BELEK NY: Editorial & Communication Acceptance

Статус: CURRENT
Дата аудита: 2026-09-11
Основа аудита: canonical Drive HTML/PDF и `main` SHA `9a5d1468572840cac214254214f45d3d15ca9c64` до изменения.

## 1. Методологические источники

Изучены:

- Theatre Guide `docs/THEATREGUIDE_COMMUNICATION_CANON_CURRENT.md`, ветка `r3/multi-page-runtime`;
- Theatre Guide issue #1 и комментарии о service-wide A/B/C communication gate;
- Theatre Guide issue #2 и комментарии о применении gate к Telegram flow;
- текущие BELEK NY `TEXT_STYLE_SOURCE_OF_TRUTH.md`, `PUBLIC_COPY_QA_CHECKLIST.md`, mobile/card/price/delta rules и фактический HTML/PDF.

Theatre Guide используется как методологический донор. Театральные ticket/show/age правила не переносились.

## 2. Conflict map

### Совместимо

- русский человеческий язык;
- запрет внутреннего технического и гостиничного жаргона;
- факт отдельно от оценки и неизвестности;
- доказательность цен и ключевых условий;
- запрет em dash/en dash;
- конкретика вместо рекламного тумана;
- таблицы для реального сравнения.

Решение: усилено в существующем `TEXT_STYLE_SOURCE_OF_TRUTH.md`.

### Требует адаптации

Theatre Guide ticket truth адаптирован к hotel/price truth: точный отель + категория + состав + даты + питание + валюта. Официальный факт отделён от проектной рекомендации; историческая цена отделена от текущей.

CTA methodology адаптирована к карточке отеля и внешним действиям.

### Конфликтует

Общий donor-принцип избегает `Подробнее`, если можно назвать результат конкретнее. Последняя прямая команда BELEK NY закрепляет inline toggle `Подробнее/Свернуть`. Решение: сохранить как документированное продуктовое исключение.

Старый `HOTEL_CARD_ACTIONS_AND_SITE_LINK_QA.md` требовал две кнопки и содержал compare semantics. Фактический prod и последняя команда требуют три кнопки и no-compare. Решение: старый документ синхронизирован с живым продуктом.

Старый delta-only текст можно было прочитать как запрет любой непрайсовой ручной продуктовой правки. Решение: scheduled monitor остаётся строгим no-delta gate; явная пользовательская продуктовая/редакторская правка является разрешённой содержательной дельтой после acceptance и не двигает price timestamps.

### Неприменимо сейчас

В BELEK NY нет отдельных bot/chat, onboarding, forms, settings, email и notification surfaces. Они зафиксированы как будущий backlog и должны наследовать canon при появлении.

## 3. Surface inventory

Текущий scope:

- web desktop: full page;
- web mobile: full page и sticky navigation;
- hero;
- ranking;
- 10 hotel cards, closed/open;
- hotel actions;
- prices;
- services;
- gastronomy;
- PDF download block;
- final recommendation;
- generated PDF.

Backlog при появлении: bot/chat, onboarding, forms, settings, notifications, email.

## 4. Baseline audit

### Web / static HTML

Level A: FAIL

- декоративные middle-dot separators и стрелка даты;
- много пользовательских конструкций через slash;
- stale wording `с прошлого запроса` в aria-label ценового тренда;
- продуктовые документы расходились с фактическими тремя действиями карточки.

Level B: FAIL

- часть заголовков и подзаголовков повторяла смысл соседнего блока;
- оценки местами звучали как факт без явной рамки «оценка проекта»;
- гастрономический блок говорил от первого лица;
- были длинные объяснения там, где достаточно конкретного факта и ограничения.

Level C: FAIL

- generic `Подробнее` требует отдельного обоснования как продукта, иначе нарушает общий CTA-principle;
- документация карточки противоречила фактическому flow;
- связанные web/PDF формулировки не проходили единый contextual gate.

### PDF

Level A: FAIL

- наследовал часть baseline-copy нарушений.

Level B: FAIL

- наследовал повторения и неоптимальные подписи web.

Level C: FAIL

- таблица стоимости теряла правый край на исходной print-верстке;
- легенда услуг была визуально слишком плотной;
- PDF показывал бессмысленный интерактивный summary `Открыть полный разбор +`, хотя подробности уже печатались;
- print build запрещал разрывать целые hotel cards/rows и был хрупким для полного раскрытого контента.

Final baseline result: REJECTED.

## 5. Remediation

Copy:

- hero сокращён и сфокусирован на задаче поездки;
- рейтинг явно назван оценкой проекта;
- факты и рекомендации разделены в intro/cards;
- карточки получили конкретные `Сильные стороны`, `Риски и ограничения`, `Что платно или требует проверки`;
- first-person gastro copy заменён нейтральным продуктовым голосом;
- slash constructions и декоративные separators удалены там, где они не нужны;
- `с прошлого запроса` заменено на `с прошлого обновления цен`;
- финальная рекомендация объясняет критерий каждого из трёх вариантов.

UX вместо дополнительного текста:

- сохранена binding 3-button модель и задокументировано исключение `Подробнее/Свернуть`;
- старый compare contract удалён из current card QA;
- PDF actions скрыты, а подробности печатаются как обычный контент без бессмысленного summary;
- блок цен в PDF переведён на landscape A4, чтобы 7 колонок и стрелки не обрезались и не накладывались;
- print layout услуг, гастрономии и финального выбора переработан для читаемого A4;
- whole-card/whole-row forced break-inside убран из PDF build, сохранены только безопасные локальные no-break blocks.

Данные:

- цены не менялись;
- `previous_price_update_at` не менялся;
- `current_price_update_at` не менялся;
- price trend semantics не менялись;
- ranking semantics не менялись;
- canonical Drive IDs не меняются.

## 6. Final gate

### Surface: web desktop / static HTML

Scope: full page, hero, ranking, navigation, 10 cards, prices, services, gastronomy, PDF block and final recommendation.

Level A: PASS. `scripts/validate_public_copy.py` PASS; no forbidden dashes, decorative separators, emoji, internal statuses, compare copy or stale price wording. Canonical terminology and specific PDF CTA present.

Level B: PASS. Copy review confirms user task first, fact/recommendation/unknown separation, concrete conditions and dates, neutral product voice, reduced repetition, no AI-style loops and no unsupported increase in certainty. Price/ranking facts were not changed by the editorial rewrite.

Level C: PASS. Rendered desktop review at 1440 x 1100 confirms hierarchy, navigation context, readable price table and action semantics. Card links and price data are byte-for-byte equivalent at the structured-value level to baseline; only copy/print UX changed. Image sources are unchanged.

Rendered/manual review: PASS. Chromium/Playwright rendered the production DOM/CSS/copy; embedded hotel photos were replaced only in the local screenshot harness with same-size placeholders to avoid renderer cost. Actual photo sources are unchanged and final PDF render validates them.

Unresolved items: none in current scope.
Final result: ACCEPTED

### Surface: web mobile 390

Scope: sticky navigation, canonical menu, collapsed/expanded hotel card and three-action row.

Level A: PASS. Same automated public-copy gate as desktop.

Level B: PASS. Labels stay concise and consistent: `Подробнее/Свернуть`, `Отзывы`, `Сайт отеля`; category/status emoji removed as redundant visual noise.

Level C: PASS. Rendered 390 px interaction confirms the three actions remain in one 330 px row with one-line labels; `Подробнее` opens the same card, `Свернуть` closes it; burger exposes `Рейтинг`, `Отели`, `Стоимость`, `Услуги`, `Еда`, `Рекомендация` and closes after section selection. `Подробнее` remains a documented explicit product exception.

Rendered/manual review: PASS at 390 x 1100/1200. Existing approved 390 geometry remains unchanged; final candidate interaction was re-rendered after copy remediation.

Unresolved items: none in current scope.
Final result: ACCEPTED

### Surface: PDF

Scope: all 21 pages, including all 10 hotel cards, prices, price sources, services, gastronomy and final recommendation.

Level A: PASS. PDF text contains no forbidden em/en dash, decorative separators, category/status emoji or internal service statuses. All 10 hotels and the current machine report-version marker are present.

Level B: PASS. PDF carries the same revised copy hierarchy and fact/assessment/unknown distinctions as web. No first-person gastro framing or repeated explanatory loops remain in the audited scope.

Level C: PASS. Full 150 dpi render reviewed page by page. Price section uses A4 landscape on pages 15-17; all seven price columns and arrows are visible without clipping. Services, gastronomy and shortlist return to readable portrait layout. Interactive card actions and PDF-download UI are not printed. No clipped text, overlap, broken glyphs or black boxes found.

Rendered/manual review: PASS. `pdf_preflight.py`: openable, 21 pages, not scanned, not encrypted; all-page contact review plus full-size review of the price table and dense comparison pages completed.

Unresolved items: none in current scope.
Final result: ACCEPTED

## 7. Release rule

Публикация разрешена только после фиксации A PASS + B PASS + C PASS для всех поверхностей текущего scope. При любом FAIL remediation loop продолжается.
